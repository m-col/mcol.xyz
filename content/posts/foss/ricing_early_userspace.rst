ricing early userspace
======================

:date: 2020-06-29
:summary: ricing the TTY

This weekend I wanted to make the boot process on my Arch Linux machine look
more consistent with the rest of its environment. A while back I configured a
quiet-boot setup to minimise unnecessary steps or messages appearing between
switching on the device and reaching the X11 desktop. The last thing that
remained in making the bootup spotless was the cryptsetup password prompt used
in early userspace to unlock my root partition. It was u g l y.

After experimenting with plymouth_ and it's various themes (which *do* look
pretty nice), the extra 5 seconds of boot time just isn't acceptable. Like,
come on, I want it to be perfect. I'm a big fan of bitmap fonts and pixel art
so I figured I could hack together some kind of text-based display for the
password prompt using symbols and `box-drawing characters`_.

Font
----

First though, I needed to change the TTY font before reaching that prompt. For
this the `arch wiki`_ had the answer ready so this was a quick job: simply
define :code:`FONT` in :code:`/etc/vconsole.conf` to the name of an available
:code:`psf` font (look inside :code:`/usr/share/kbd/consolefonts` to see
available fonts), then add :code:`consolefont` to the mkinitcpio hooks in
:code:`/etc/mkinitcpio.conf`.

Drawing the shapes
------------------

Looking deeper into `mkinitcpio hooks`_, I discovered that creating your own
hook is actually pretty straight-forward, so I got to work writing one to draw
out the console's display immediately before the password prompt. I simply had
to write a hook to print whatever I wanted and add it to my
:code:`/etc/mkinitcpio.conf`.

For a simple first-attempt interface, I decided on the message "Welcome" drawn
in big letters in my favourite font, tamzen_, with an input box drawn
underneath for when I'm asked to unlock the root partition. I figured I could
draw the big word by making "pixels" from symbols.

I got the template by screenshotting my normal xterm (also using the tamzen
font) and scaling it up:

.. image:: /static/tamzen-Welcome.png
   :alt: The word 'Welcome' in tamzen font

Following this, I typed out a bunch of :code:`echo` commands into my new hook
that would each print a single line of the console, and would together spell
"Welcome" in big letters. For this, I used pairs of block characters (i.e.
"██") as pixels to draw the word pixel-by-pixel. The input box is just an empty
rectangle frame drawn using these pixels underneath the Welcome message. Using
`ANSI escape codes`_ I could move the cursor position into the input box after
printing the display, e.g. printing :code:`"\x1b[32;96H"` will place the cursor
in the 32nd column, 96th row.

Colours
-------

Next, I needed to define the colours that all the elements should have: the
background, "Welcome", and the input box. My first instinct was to simply use
more escape codes to set the "current" terminal colour, which would look
something like this:

.. code-block:: sh
    
   # This sets the current foreground to colour 0
   COLOUR=0
   echo -en "\x1b[38;5;${COLOUR}m"

   # While this sets the current background to colour 5
   COLOUR=5
   echo -en "\x1b[48;5;${COLOUR}m"

I added lines like these in places in the pixel-drawing echo lines where the
foreground or background colour was to be changed, and it worked quite well.
However, the problem with this is that the colours that the TTY uses are
restricted to default values predefined by the linux framebuffer (which are
*not* pretty).

A quick search on changing the TTY's colours lead me to `this askubuntu
question`_ describing how to change the colours that correspond to the
consoles's 0-15 colour definitions. Based on these lines (more escape codes!) I
cobbled together some logic at the top of my hook to redefine the TTY's colour
palette using the same hexadecimal colour values I use for my X desktop, and
stripped out the previous escape codes I was using.

Great! The colours were being set!

Right as I was planning to put the colour logic into a small package, I came
across Evan Purkhiser's `mkinitcpio-colors`_, which is a more polished version
of what I would have made to set the TTY colours at boot using variables
defined in :code:`/etc/vconsole.conf`. I installed this from the AUR so that my
welcome message would use my usual terminal colour scheme.

Finishing up
------------

The output of fsck is printed out after entering the password. `Apparently`_
this can be silenced, but I preferred to simply reposition the cursor into a
second line of the inpux box so it can be printed there. For this I added a
second hook after the :code:`encrypt` hook.

This is the final version:

.. raw:: html

   <video controls width="100%" class="align-center" src="/static/boot_welcome.webm"></video>

Looking great, huh!

I've saved the two mkinitcpio hooks in a git project here_, which installed
alongside `mkinitcpio-colors`_ should be enough to recreate this bootup. I
haven't tested it with any other font sizes though, so the thought of trying it
with a different size worries me.

.. _plymouth: https://wiki.archlinux.org/index.php/Plymouth
.. _mkinitcpio-colors: https://github.com/EvanPurkhiser/mkinitcpio-colors
.. _`box-drawing characters`: https://en.wikipedia.org/wiki/Box-drawing_character
.. _tamzen: https://github.com/sunaku/tamzen-font
.. _`arch wiki`: https://wiki.archlinux.org/index.php/Linux_console#Fonts
.. _`mkinitcpio hooks`: https://wiki.archlinux.org/index.php/Mkinitcpio#HOOKS
.. _`ANSI escape codes`: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
.. _`this askubuntu question`: https://askubuntu.com/questions/147462/how-can-i-change-the-tty-colors
.. _Apparently: https://wiki.archlinux.org/index.php/Silent_boot#fsck
.. _here: /code/mkinitcpio-welcome
