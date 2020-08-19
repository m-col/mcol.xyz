a quick and dirty permissions container
=======================================


:date: 2020-03-29
:summary: A quick and dirty permissions container for a single program


Although the vast majority of the software installed on my Linux daily driver
is fully free and open source, and in general is trustworthy, over time I've
had to make use of some programs that are closed source and created by entities
who I wouldn't want to trust on my system.

The quick and easy (lazy) solution I've opted for is to give these programs
their own user and home directory and access to my normal user's X session.

For example, we can create a user and home directory for steam (as root):

.. code-block:: sh

   useradd --create-home steam

We probably want our normal user to be able to launch the program with its user
without needing to enter a password every time. To do this, we need to add a
line equivalent to this to our sudoers rules:

.. code-block:: sh

   mcol ALL=(steam) NOPASSWD: /usr/bin/steam

If we were to launch it now, it wouldn't have access to the running X session
owned by our normal user. We can use :code:`xhost` to give the new steam user
access to the X session. This is best wrapped in a script that looks like:

.. code-block:: sh

   #!/usr/bin/env bash
   xhost +SI:localuser:steam
   sudo --set-home -u steam /usr/bin/steam $@

I call this script :code:`steam` and put it in a folder on my path inside my
home folder. This way, I can just execute :code:`steam` as my normal user and
the program runs as expected in my X session, but its permissions keep it
restricted to its own home folder.

This setup also lets us set firewall rules specific to the program, as nftables
and iptables support the configuration of rules that match a user's UID. For
example, if we wanted nftables to block connections from steam that weren't
going through a VPN we could add this line to our outbound chain:

.. code-block:: sh

   oifname $vpn_interface skuid steam accept
   oifname != $vpn_interface skuid steam reject

Simple and great for those who wear tinfoil hats!
