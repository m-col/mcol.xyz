mpop and msmtp: a minimalist match made in heaven
=================================================

:date: 2019-05-28
:summary: mpop and msmtp: a minimalist match made in heaven

Like many sane people, I have a soft spot for little C programs with little
config files that do exactly what they do and nothing else. `Martin Lambers'
<https://marlam.de/>`_ POP3 and SMTP clients, `mpop <https://marlam.de/mpop/>`_
and `msmtp <https://marlam.de/msmtp/>`_, are perfect examples.

In my quest for a minimal and straight forward setup, these bad boys have
become my daily email handlers, with :code:`mpop` downloading my emails into a
Maildir at :code:`~/.mail`, :code:`mutt` being a mostly offline interface to
deal with all the crap people send me, and :code:`msmtp` as the backend to send
mail from mutt.

mpop can be run as a cronjob, downloading mail every 30 minutes, leaving no
trace on the remote server (if I trust my provider, that is).

setup
-----

mpop and msmtp can be installed from your distributions repos via the usual
route.

Both programs have sane defaults that would work well for a standard user, so
the configuration files are very few lines and take only a minute to write.

On top of that, they both share a chunk of code and its corresponding options,
resulting in a good bit of the two files sharing lines.

My config for mpop, for example, is simply:

.. code-block:: haskell

    defaults
    uidls_file "~/.config/mpop/uidls_%U_at_%H"
    tls on
    tls_starttls off
    
    account posteo
    host "posteo.de"
    user "<myemailaddress>"
    passwordeval "gpg --no-tty -q -d --for-your-eyes-only ~/.mail/posteo.gpg"
    delivery maildir "~/.mail/posteo/INBOX"
    port 995

Compared to my nearly identical msmtp config:

.. code-block:: haskell

    defaults
    auth on
    tls on
    tls_starttls off

    account posteo
    host "posteo.de"
    user "<myemailaddress>"
    from "<myemailaddress>"
    passwordeval "gpg --no-tty -q -d --for-your-eyes-only ~/.mail/posteo.gpg"
    port 465

The first 4 lines of each are the defaults, which apply to all email accounts
that are set up. The second block is therefore my first account, in this case
just named :code:`posteo` for my provider. Everything is simple and self
explanatory.  Of note though is the passwordeval lines, which is simply a shell
line executed that should give you the password for that account, in this case
taking it from my gpg-agent.

torifying
---------

Both programs can be run straight through Tor with no trouble at all, just
stick this into the defaults sections:

.. code-block:: haskell

    proxy_host localhost
    proxy_port 9050

After 2 minutes of setup, these programs can work in the background and never
ask for your attention again.
