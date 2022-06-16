hacking on Qtile: painting complex borders
==========================================

:date: 2020-05-12
:summary: Extending Qtile to create funky window border decorations

The years of checking up on the unixporn subreddit has imprinted in me a want
for a unique and aesthetic desktop. One of the advantages I saw in the Qtile
window manager (while I was rapidly hopping between WMs) is how easy it is to
bend to my will, being made in Python. Recently I set out to satisfy my desire
for more than just single colour, single line window borders.

The result of this endeavour has two parts. The first is a PR_ I submitted last
week to Qtile that lets users pass their layouts a list of border colours and a
list of border widths to paint multiple borders on their windows. In my head it
was a long time coming, having nice windows like these:

.. raw:: html

    <img style="box-shadow: 10px 10px 5px black;" alt="Window with triple borders" src="/static/qtile_multi.png"/>

The code accepts any number of border colours and widths, so if you *really*
wanted to, you could have borders like these:

.. raw:: html

    <img style="box-shadow: 10px 10px 5px black;" alt="Window with a shitload of borders" src="/static/qtile_multi2.png"/>


Has user freedom come too far?

The PR also aimed to unify all border-drawing code into one callable. This
leads to the second development: you can override this callable -
:code:`xcbq.Window.paint_borders` of Qtile's X11 backend  - and replace the
border-painting logic with your wildest dreams.

Normally, this method would loop over the configured colours and widths, using
them to draw increasingly small filled rectangles centred on a pixmap that will
be used to paint the window's borders. This results in the multi-border effect
above. A function we define to override this method will therefore have access
to a list of colours, as well as the window's geometry including border width,
and a canvas - the pixmap.

The paintbrush is tycho0's xcffib_, which provides Python bindings to XCB_. The
:code:`xcffib.xproto` module gives us the functions we need to create some
shapes and paint them to our pixmap, which are reminiscent of their C
counterparts such as :code:`xcb_poly_fill_rectangle` from xcb.xproto.h.

Using this information, we can do whatever we want. A simple example would be
to draw a couple of trapeziums (trapezia_? thefreedictionary suggests either,
TIL) using :code:`xcffib.xproto.POINT` and paint them using and
:code:`FillPoly` in two of the colours. This can create this picture frame-like
appearance:

.. raw:: html

    <img style="box-shadow: 10px 10px 5px black;" alt="Window with frame" src="/static/qtile_frame.png"/>

Pretty cool, no? Maybe too simple.

With some faffing around in GIMP on a screenshot of the `Common Desktop
Environment`_ (CDE), I decoded the design for their old-school 3D borders. I'm
aware I could have hunted down the source code to find out how their borders
are drawn but where's the fun in that?

The design is largely made of 1-pixel-wide lines, so we can use
:code:`xcffib.xproto.POINT` as before to join them up, then :code:`PolyLine` to
paint them to the pixmap. With a main colour, a lighter shade and a darker
shade, we can get this result:

.. raw:: html

    <img style="box-shadow: 10px 10px 5px black;" alt="Window with triple borders" src="/static/qtile_cde.png"/>

Pretty groovy borders if you ask me, and it's a design I can use without
sacrificing a solid, modern window manager.

I've added these to my Qtile plugin repository qtools_, from which they can be
used by simply importing and enabling the borders plugin with the desired
style:

.. code-block:: python

   import qtools.borders
   borders.enable("CDE")

The plugins might also serve as a simple starting point to implement more
border designs.

I'd love to make a small library of different designs that can be used to make
borders but my own creativity is limited. Let me know if you have any design
ideas that you'd want implemented for your own Qtile config!


.. _PR: https://github.com/qtile/qtile/pull/1697
.. _xcffib: https://github.com/tych0/xcffib
.. _XCB: https://en.wikipedia.org/wiki/XCB
.. _trapezia: https://www.thefreedictionary.com/trapezia
.. _`Common Desktop Environment`: https://en.wikipedia.org/wiki/Common_Desktop_Environment
.. _qtools: /code/qtools/file/qtools/borders/borders.py.html
