rewritefs: take back control over your dotfiles
===============================================

:date: 2019-08-17
:summary: take back control over your home folder dotfiles with rewritefs

Many of us have had the unfortunate inevitability of using a program written by
a sadistic programmer who sticks their program's files right into your neatly
organised home folder. Fortunately, some rebels against the
what-are-`XDG-directory-standards
<https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_
terrorist group have come up with clever solutions to force all of your hidden
files to stay within the bounds of your .config folder.

Inspired by the likes of Apache and nginx, `rewritefs
<https://github.com/sloonz/rewritefs>`_ uses arbitrary regex rules to rewrite
(surprise surprise) paths accessed in a mount point. Using a `FUSE
<https://en.wikipedia.org/wiki/Filesystem_in_Userspace>`_ approach, rewritefs
simply mounts a user's a folder and the rest of the functionality is invisible.

This example ruleset is provided to solve the problem of dotfiles clogging your
home directory:

.. code-block:: bbcbasic

    m#^(?!\.)# .
    m#^\.(cache|config|local)# .
    m#^\.# .config/

We have one rule per line, rewriting strings matched by the first part to the
content of the second part, with the special rule :code:`.` meaning 'do not
rewrite'. E.g. :code:`.vimrc` becomes :code:`.config/vimrc`.

To use these rules all we have to do is mount the directory, in this example
our home directory from :code:`/mnt` into :code:`/home`, i.e.:

.. code-block:: bash

    rewritefs -o config=/mnt/home/me/.config/rewritefs /mnt/home/me /home/me

It's worth spending a bit of time going through all the junk in $HOME while
setting up a ruleset, as many folders might be more appropriate going into
:code:`.cache` or :code:`.local`.

A massive plus of careful rulesetting and rewriting the appropriate files into
:code:`.config` is that you can backup or version :code:`.config` in its
entirety while putting things you don't care so much about into :code:`.cache`
or elsewhere. This is much tidier than having to deal with scripting symlinks
into :code:`$HOME` from your dotfiles repo, and more out-of-the-way than
version tracking your home directory directly.

Another nifty feature is the ability to specify rules on a per-application
basis. For example, you could use this rule to make your annoying colleague's
vim mysteriously replace the letter s for the letter z:

.. code-block:: bbcbasic

    - /^\S*vim/
    /s/ z

In such a rule, the line starting with - match the program name, and any
following lines apply only to that scope.

With great power comes great responsibility, so one must be careful with the
power of rewritefs. Despite its power, however, there do seem to be only few
real applications for such functionality. I would definitely be interested in
hearing what other use people have made for this program.
