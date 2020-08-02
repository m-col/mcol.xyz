xonsh shell: first week, first impressions
==========================================

:date: 2019-06-29
:summary: xonsh shell: first week, first impressions

If you've ever said "Oh boy I wish I could use all that cool pythonic syntax
and algebra in my shell!" then `xonsh <https://github.com/xonsh/xonsh>`_ is
definitely worth checking out.

For the past week or so I've been using xonsh, a "python-powered,
cross-platform, Unix-gazing shell language and command prompt" as my main
shell. Exploring it has been an adventure and I've learnt much, but after one
week I can tell I've only scratched the surface.

It is a superset of Python, extending it to include many aspects of shell
syntax and behaviour. This makes for a very powerful yet flexible and usable
language.

First let me say it is awesome and worth a play if you like Python, but,
unfortunately, it doesn't quite feel as stable as bash or zsh. However, the
`docs <https://xon.sh/>`_ and github issues are fantastic resources to
configure and extend it to be just as (if not more) usable as other shells.

powerful cli syntax
-------------------

If you've ever gone from bash to zsh, it was likely a seamless change. In
contrast, the first time playing with xonsh's syntax requires one eye on the
docs. This is understandable, as it was clearly no easy feat creating the
lovechild of bash and python. Check this out:

.. code-block:: bash

    path = $HOME + '/.xonshrc'
    if not !(test -f @(path)):
	return 'Error: %s not found.' % path

Variables are pythonic; dollar signs are not required, but they prefix
environmental variables by convention. As demonstrated above, we can modify
variables, perform tests and format strings as in python.

What's cool here are the syntax blocks we see on the second line:

- :code:`@(...)` treats its contents more like python, so @(path) expands to
  the path string.
- :code:`!(...)` treats its contents with a shell syntax. The result from a
  :code:`!(...)` block can be used in tests based on its return code, as above,
  but the object also contains the standard out and error streams, process id,
  and some other information.

This illustrates a central idea in xonsh: a contextual distinction between
python-like (*python-mode*) and shell-like (*subprocess-mode*) executions.

xonsh also uses python's logical keywords, which act as drop in replacements
for :code:`&&` and :code:`||`:

.. code-block:: bash

    a > 10 and echo "a is greater than 10"

This is only a tiny sample but you get the idea. The shell-like syntax is very
comfortable, and it feels natural to use it alongside python code.

setup
-----

Much like zsh, the first time it is run, a wizard will guide you through
initial setup and then get out of the way. This wizard generates your
:code:`~/.xonshrc` file which is run when you launch xonsh.

The first step is 'Foreign Shell Setup'. This feature aims to help users use
pre-existing bash or zsh configs in xonsh, though currently there are some
limitations. For example, imported aliases that 'cd /some/path' don't seem to
propagate their directory change to the shell. Surfing the github issues it
seems there are a couple of other minor bugs that prevent use of things like
:code:`;` or :code:`&&` in aliases.

The wizard next helps you set up other useful features and behaviour you see in
other shells:

- syntax highlighting
- command completion
- vi-mode
- prompts
- plugins

Most of these are simply controlled by variables set in your :code:`.xonshrc`.
Overall the xonsh initial setup is painless.

plugins
-------

xonsh's plugin framework allows for easy extension with xonsh or pure python
scripts called *xontribs*. Some xontribs come pre-packaged but you can download
or create more.

I was pleased to find that the zsh plugin `z <https://github.com/rupa/z>`_ had
been `ported <https://github.com/astronouth7303/xontrib-z>`_ to xonsh, and a
read of its code makes it clear that porting other zsh plugins would be
relatively straightforward.

xontribs can do anything you want, such as hooking functions to events, adding
more blocks that can be used in your prompt, adding functional aliases, you
name it.

For example, we can create new aliases like this:

.. code-block:: bash

    def _copy(args=None, stdin=None):
        """ Copy stdin or args to the clipboard """
        text = stdin.read() if stdin else ' '.join(args)
        echo -n @(text.strip()) | xclip -selection clipboard
        return

    aliases['copy'] = _copy

Aliases like this send the argument list and stdin to the function as the first
two arguments. This allows us to use shell-like syntax to call the function,
i.e.:

.. code-block:: bash

    echo 'this will be copied' | copy
    copy 'so will this'

This seems much more natural in a shell.

Setting up a comfy environment in xonsh has led to me reading all about
`prompt_toolkit <https://github.com/prompt-toolkit/python-prompt-toolkit>`_.
prompt_toolkit is a really powerful python library for controlling what appears
in the terminal window, and does the heavy lifting for xonsh when it comes to
drawing prompts, watching for key bindings, and more. For these reasons, it is
often useful to use its tools directly, rather than xonsh, to extend your xonsh
setup.

thoughts
--------

Overall I think xonsh is awesome and I'm excited to see how xonsh develops in
the future. It's a powerful concept, and the motivation appears to be there -
from both core devs and contibuting users - to iron out any issues and improve
the experience.

It's pretty cool that you can use python libraries as in python:

.. code-block:: python

    from pykeyboard import PyKeyboard

Though I haven't actually found a use for that yet!

It is usable and practical as a daily driver, so I will definitely continue to
use it and see how deep the rabbit hole goes.
