writing a Python wallpaper setter for X11
=========================================

:date: 2019-11-23
:summary: writing a Python wallpaper setter for X11 

For the past few weeks I've been learning a lot about the communication
interface between the X11 server and its clients. As a devotee of Qtile_, I
have been using it as a testing ground for a number of tools that directly talk
with the X server, using the Python X bindings provided by xcffib_.

This exercise has seen me spend a fair bit of time and effort trying to 'port'
C code using XCB_ or xlib_ to xcffib equivalents. At times this is tedious - as
anybody who has written X client code will know - but I like the idea of
extending Qtile to include more features typically outside of the scope of a
standalone window-manager.

One such feature is the simple ability to set the background wallpaper. Sounds
easy, right? The X server manages the drawing of windows as regions within the
root window, which itself is handled in many ways like a normal window. The
appearance of each window (including the root window) is stored within a
pixmap, whose data can be rendered on-screen as pixels. This description is
super simplified; for a fantastic and more in-depth exploration of how this
works I recommend reading xplain_ by Jasper St. Pierre.

Setting the desktop wallpaper therefore means colouring and rendering the
pixmap for the root window of each screen. Wrapping this behaviour as an X
client: we need to open a connection to the X server, load our wallpaper image
in a form that can be painted onto a pixmap, and then perform the painting.
I've packaged what I've described here with a convenient interface here_.


wallpaper setting with xcffib
-----------------------------

Opening an X client connection is straightforward and requires the
:code:`DISPLAY` environmental variable. xcffib gives us a :code:`Connection`
object from which we can get information from the X server such as screen
setup.

.. code-block:: python
    
    import os
    import xcffib
    import cairocffi            # needed later
    import cairocffi.pixbuf     # needed later
    import xcffib.xproto        # needed later

    conn = xcffib.Connection(display=os.environ.get("DISPLAY"))
    screens = conn.get_setup().roots

Next we need to load our image. The cairocffi_ library provides Python bindings
for cairo_, a 2D graphics library that supports rendering graphics to X
pixmaps. We can load our image into what cairo calls a :code:`Surface` with:

.. code-block:: python

    with open('/path/to/image.png', 'rb') as fd:
        image, _ = cairocffi.pixbuf.decode_to_image_surface(fd.read())

As we need to paint the image to one screen at a time, we could load multiple
images and use a different image for each painting operation.

The next part performs the painting of the root pixmap to set the wallpaper.
First we must ask the server for a new resource ID and use this to create our
pixmap for the current screen. Creating the pixmap requires the colour depth of
the screen (:code:`screen.root_depth`) as well as its own ID
(:code:`screen.root`), and its dimensions:

.. code-block:: python

    screen = screens[0]
    pixmap = conn.generate_id()
    conn.core.CreatePixmap(
        screen.root_depth,
        pixmap,
        screen.root,
        screen.width_in_pixels,
        screen.height_in_pixels,
    )

We could iterate over :code:`screens` to paint each screen.

Next we need to extract from the screen its :code:`visual`, which contains
information about how it manages colour maps and depths. We need this to create
a cairo surface that is compatible with the root window, onto which we can
paint our image:

.. code-block:: python

    for depth in screen.allowed_depths:
        for visual in depth.visuals:
            if visual.visual_id == screen.root_visual:
                root_visual = visual
                break

    surface = cairocffi.xcb.XCBSurface(
        conn, pixmap, root_visual,
        screen.width_in_pixels, screen.height_in_pixels,
    )

The cairocffi API for manipulating surfaces provides us a :code:`Context` in
which to modify and use our :code:`Surface` objects (the image and pixmap
surfaces).  Surface manipulation is pretty nice, and it only takes one command
to set our image as a data source and another to paint it to the pixmap:

.. code-block:: python

    with cairocffi.Context(surface) as context:
        context.set_source_surface(image)
        context.paint()

It is at this point where we could add more image manipulations to the source
image before painting, such as stretching or tiling.

Root windows have two properties named :code:`_XROOTPMAP_ID` and
:code:`ESETROOT_PMAP_ID` which it uses to publish the root pixmap so that other
X clients can have access to the pixel data. This is used for effects such as
the pseudo-transparency feature of urxvt_. We therefore need to set these
properties using our newly painted pixmap.

The xcffib API for this might look a bit cryptic; we are passing the
property-setting mode :code:`Replace`, the root window concerned, the property
we want to change, the type of data we are passing (:code:`PIXMAP`) and lastly
the bit format, number of items and our list of items (just our pixmap):

.. code-block:: python

    conn.core.ChangeProperty(
        xcffib.xproto.PropMode.Replace,
        screen.root,
        conn.core.InternAtom(False, 13, '_XROOTPMAP_ID').reply().atom,
        xcffib.xproto.Atom.PIXMAP,
        32, 1, [pixmap]
    )
    conn.core.ChangeProperty(
        xcffib.xproto.PropMode.Replace,
        screen.root,
        conn.core.InternAtom(False, 16, 'ESETROOT_PMAP_ID').reply().atom,
        xcffib.xproto.Atom.PIXMAP,
        32, 1, [pixmap]
    )

We can then change the root window's background pixmap to our pixmap and clear
the area that contains it, which refreshes those pixels to display their new
values:

.. code-block:: python

    conn.core.ChangeWindowAttributes(
        screen.root, xcffib.xproto.CW.BackPixmap, [pixmap]
    )
    conn.core.ClearArea(
        0, screen.root,
        0, 0,           # x and y position
        screen.width_in_pixels, screen.height_in_pixels
    )

Without the :code:`ClearArea` call background pixels will only refresh when you
move a window over them, which can be a cool effect.

Lastly we should set our X client's :code:`CloseDown` mode to
:code:`RetainPermanent` to make the our changes to the root window persist
after the client closes, and then disconnect.

.. code-block:: python

    conn.core.SetCloseDownMode(xcffib.xproto.CloseDown.RetainPermanent)
    conn.disconnect()

The logic we've looked at so far is sufficient to set the X wallpaper, and can
easily be extended to apply wallpapers to multiple screens and to manipulate
our desired image before painting it the pixmap.

For example, if the dimensions of our image and screen might differ or if we
want to use only a subregion of an image, we can use cairocffi's
:code:`Context` API to change how we paint to our pixmap. The library exposes
:code:`Context.scale()` and :code:`Context.translate()` methods which can be
used right before the paint command to change how the image will map onto the
pixmap.


using a solid colour
--------------------

If we want to paint the wallpaper with a single colour instead of an image, we
can replace the call to :code:`context.set_source_surface()` with the
following, where the three arguments correspond to red, green and blue values:

.. code-block:: python

    context.set_source_rgb(1, 1, 1) 


see also
--------

I learnt a lot reading how these programs handle painting the root window:

 - xsri_
 - fvwm-root_


.. _Qtile: https://github.com/qtile/qtile
.. _xcffib: https://github.com/tych0/xcffib
.. _XCB: https://xcb.freedesktop.org/
.. _xlib: https://www.x.org/releases/current/doc/libX11/libX11/libX11.html
.. _xplain: https://magcius.github.io/xplain/article/x-basics.html
.. _here: /code/qpaper
.. _cairocffi: https://cairocffi.readthedocs.io
.. _cairo: https://www.cairographics.org/
.. _urxvt: https://software.schmorp.de/pkg/rxvt-unicode.html
.. _xsri: https://github.com/tjackson/xsri
.. _fvwm-root: https://github.com/fvwmorg/fvwm/blob/master/bin/fvwm-root.c
