nftables as a tor and VPN killswitch
====================================

:date: 2019-05-05
:summary: nftables as a tor and VPN killswitch

Truth be told, I never got the hang of iptables. nftables has a much nicer
syntax and its improvements over iptables will lead to its dominance...
eventually.

This nftables configuration restricts outward network traffic to a locally
running tor client, running as the user :code:`tor`, and a VPN interface, as two
independent streams of traffic. This way I can allow any programs that aren't
so tor friendly to use the VPN, and everything to go through tor directly.
The whole file can be found `here <{static}/static/nftables.conf>`_.

Usually the configuration file is at :code:`/etc/nftables.conf`.

First, we need to flush any current rules:

.. code-block:: Java

    flush ruleset

Next, we create our first :code:`table`, which is of type :code:`inet`, and
named :code:`restricted`. This type means is it applies to IPv4 and IPv6 both.

.. code-block:: Java

    table inet restricted {
        chain inbound {
            type filter hook input priority 0;

Within the table, we define our first :code:`chain` with the name
:code:`input`.  We specify the chains behaviour on the first line in the chain.
This chain is of type :code:`filter`, i.e. it will filter packets. We then give
it the :code:`input` hook so it will act on incoming packets.

Priorities can be set to order the chains relative to some internal Netfilter
operations, see the `nftables wiki
<https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_priority>`_
for more info. For a non-routing setup such as this one, priority of 0 works
for everything, though it is important to note that packets will be tested
against all chains using the relevant hook.

Next is the first rule. It starts with a 'selector', which here is :code:`ct`
for connection tracking, which uses packet metainformation to match packets.

.. code-block:: Java

                ct state {established, related} accept

This rule matches packets by **state**, and matches those with state
:code:`established` or :code:`related`.

The rule ends with an action, in this case :code:`accept`. This rule will allow
incoming packets from connections we've previously established, which means
we've already allows them and they're safe. This accounts for most traffic so
is best put first.

Next, we accept packets with incoming interface name :code:`lo`, the loopback
interface, which is required for many programs to work. Simple!

.. code-block:: Java

                iifname lo accept

Next, we match packets by :code:`ip protocol`, of type :code:`icmp`. We match
these more specifically by :code:`icmp type` with type :code:`echo-request`,
and accept them. These are pings, which are fine to allow.

.. code-block:: Java

                ip protocol icmp icmp type echo-request accept
                reject with icmp type port-unreachable
            }

We end the chain by rejecting all other inputs with the 'port unreachable'
message.

We then create our output chain, another filter but this time with the
:code:`output` hook. Again, we should accept all traffic on the loopback
interface.

.. code-block:: Java

    chain outbound {
        type filter hook output priority 0;
            oifname lo accept

Now we start restricting our outward traffic. This rule matches connections
being output from my wireless interface, :code:`wlan0`, so substitute the name
of your main interface there. It accepts all traffic on this interface destined
for the address listed, for example, the VPN server you're connecting to, and
any local devices you wouldn't want to restrict.

.. code-block:: Java

    oifname wlan0 ip daddr { 123.456.789.123, 192.168.1.3 } accept
    oifname wlan0 skuid tor accept

On the second line, we allow outbound connections on the same interface where
the UID of the originating socket (:code:`skuid`) is :code:`tor`. With a local
tor client run as the user :code:`tor`, its connections will be accepted here.

.. code-block:: Java

        oifname wg0 accept
        reject
    }

It is definitely getting straightforward. Here we allow outbound connections on
the :code:`wg0` interface, which is for my wireguard VPN. If your VPN might use
a :code:`tun0` interface, in which case substitute that.

Some commercial VPNs provide a proxy within their VPN tunnels, which can be
used to further restrict what programs can can access the internet through the
VPN. To do this, add :code:`ip daddr <proxy ip>` before the accept, and make
any allowed programs use this proxy address for connections.

We then close the chain rejecting all other traffic, blocking it from leaving
your device.

.. code-block:: Java

        chain forward {
	    type filter hook forward priority 0; policy drop;
        }
    }

Lastly, as we don't need to do any forwarding of packets we can create an empty
chain with the hook :code:`forward`. This declaration also contains a default
action, with :code:`policy drop`. We then close the table with :code:`}`.

To enable this firewall, we can run this command with your config path substituted:

.. code-block:: bash

    nft -f /etc/nftables/restricted.conf

Most linux distros will package a systemd service file which can be edited and
enabled to set up this firewall at boot.

The only connections that can go out to the internet are connections on the VPN
interface and any connections that the tor client makes, which can be accessed
by programs using it as a proxy. This way we can ensure we know exactly what
connections are allowed out and all connections that leave your machine are
encrypted while in your ISP's hands.

I highly recommend the nftables wiki especially the `quickstart guide
<https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes>`_
once you're comfortable with the syntax.
