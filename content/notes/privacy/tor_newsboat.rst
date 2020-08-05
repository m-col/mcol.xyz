read news and reddit anonymously with tor and newsboat
======================================================

:date: 2019-04-21
:summary: read news and reddit anonymously with tor and newsboat

ncurses based programs can be a bit hit-or-miss but newsboat is one of the
kings.

`newsboat <https://newsboat.org/>`_ is an RSS reader, and as far as I'm
concerned, a reddit interface, as you can turn any reddit feed into an RSS
feed. Just stick something like this into your :code:`~/.config/newsboat/urls`
file:

.. code-block:: conf

    https://www.reddit.com/r/onions/new/.rss?sort=new  "~/r/onions"

Each time your run newsboat you'll get posts to that subreddit sorted by new -
easy subscription without going near a web browser.

The key to torifying newsboat is its socks5 proxy, which is enabled with these
config settings in :code:`~/.config/newsboat/config`:

.. code-block:: conf

    use-proxy yes
    proxy-type socks5h
    proxy 127.0.0.1:9050

The proxy IP and port of course must correspond to the socks5 proxy set up in
your torrc config. The **h** in :code:`socks5h` is important - this makes tor
do all its own DNS resolutions so they aren't leaking out the usual route.

You can take the functionality to the next level by opening any feed items in
tor-browser directly from newsboat, too. First, stick this into your newsboat
config:

.. code-block:: bash

    browser "nohup tor-browser --allow-remote %u > /dev/null 2>&1 &"

and set the setting :code:`browser.tabs.loadDivertedInBackground` in
tor-browser's :code:`about:config` to false. This allows feed items to be
opened from newsboat when hitting :code:`o` without tor-browser stealing focus.

nohup is needed so tor-browser can stay alive even after your close newsboat,
if newsboat opened it. :code:`--allow-remote` will launch tor-browser and allow
it to receive remote commands to open urls as we are doing here. If
tor-browser, with this option, is already running then the url will be opened
in that instance but newsboat will stay focussed. The rest of the line sends
all output to oblivion and backgrounds the command so that it doesn't disrupt
your newsboating.

With this setup I just open newsboat once a day and give it a couple minutes to
update its feeds while I do something else. Then I can quickly comb through
everything, opening anything I want to read more about in tor-browser as I go
and deleting the rest.
