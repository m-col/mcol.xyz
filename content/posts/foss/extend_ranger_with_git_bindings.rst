extend ranger file manager with git bindings
============================================

:date: 2019-06-02
:summary: extend ranger file manager with git bindings
:modified: 2020-08-02

This is a small but incredibly useful adjustment to the default configuration
that ships with `ranger <https://github.com/ranger/ranger>`_.

If you have never used ranger, it is a fast terminal file manager with a boat
load of useful features out of the box. You can likely get it from your
distro's repos.

One of the features it is missing, however, is functional git bindings that you
can use to manipulate your local git repositories.

On the upside, ranger is highly customisable, so these features can simply be
added into the config at :code:`$HOME/.config/ranger/rc.conf:`

.. code-block:: conf

    map bs shell git -c color.status=always status | less -r
    map bp shell git push | less -r
    map bl shell git pull | less -r
    map bd shell git diff --color=always %s | less -r
    map bD shell git diff --color=always | less -r
    map ba shell git add %s
    map bA shell git add -f %s
    map bu shell git restore --cached %s
    map br shell git restore %s
    map bm console shell git commit -m '
    map bc console shell git checkout%space

The second column is our keyboard bindings. By default the 'b' prefix is
unused, so we can stick all git-related commands to this prefix. The third
column we either have :code:`shell,` which executes the following text, or
:code:`console,` which types out the following text on ranger's command line.

The first 5 lines pipe output into :code:`less`. If we didn't do this then
ranger would steal the screen again and we wouldn't see the output from the
command. The :code:`-r` option preserves any colour in the output from the git
command when presented in less. :code:`git status` is a bit of a weird one; I
found that it needed the :code:`-c color.status=always` to output color codes,
but this seemed to be inconsistent across git versions.

Some commands contain :code:`%s`; in these lines the current file is
substituted, allowing us to interactively move around our repository
git-diffing or git-adding individual files as we need. Super useful!

The final two lines pre-fill ranger's command line so you can the continue your
commit or checkout command before executing it.

Of course, these are just the bare minimum for integrating git bindings into
ranger. Depending on your git workflow requirements you can extend or customise
these so you can glide around and play with your repos with ease.

For example we can add a quick shortcut to check out tig for a closer look at
the commit history:

.. code-block:: python

    map bt shell tig

Let me know if you use similar bindings or extend these and have found some
cool tricks!
