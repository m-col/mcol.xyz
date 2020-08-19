minifying font awesome in pelican
=================================

:date: 2019-10-20
:summary: Minifying font awesome fonts and CSS in pelican state site generator

I recently incorporated `font awesome <https://fontawesome.com/>`_ glyphs into
my website in an attempt to add a touch more :fas:`eye` :fas:`candy-cane`. I
wanted to self-host them, rather than use a CDN, for the slight privacy
benefit.

Following installation, I found the generation of my site, done by `pelican
<https://blog.getpelican.com/>`_, was taking significantly longer. Perhaps I'm
crazy, but I also felt like Firefox was loading the pages for a noticably
longer few milliseconds and the change wasn't doing anything for the
perfectionist in me.

Looking at the files I had just bundled with my pages, they had added at least
200KB in webfonts (possibly more, depending on which filetype is requested) and
around 55KB in CSS to my website. And for what, the odd glyph here or there?
Most of my blog posts are less than 10KB, as is the rest of my CSS, so I
determined to find a solution to incorporate only those glyphs that I wanted to
use.

creating a pelican pugin
------------------------

The `documention
<https://docs.getpelican.com/en/stable/plugins.html#how-to-create-plugins>`_
for creating pelican plugins is useful, but I found reading existing plugins in
the `great repository <https://github.com/getpelican/pelican-plugins>`_ of
plugins much more informative.

Eventually I had put together a plugin that (so far!) appears to work wonders:
`pelican-minify-fontawesome
</code/pelican-minify-fontawesome>`_ :fas:`grin-beam`.

First, after site generation, it identifies which font awesome icons are
present by scanning the output folder and getting all HTML class attributes
that start with :code:`fa-`. The words that follow this string are the names of
the icons.

With a bit of regex magic, these icon names are then used to extract their
corresponding CSS blocks from a locally available font awesome download. These
CSS blocks are then copied into the output folder.

Extracting the glyphs from the fonts was the tricky part. FontForge advertised
Python bindings, so guided by `their docs
<https://fontforge.github.io/python.html>`_ I tried to put the logic together.
FontForge's approach to manipulating fonts did take me a while to understand,
however it does work well. This is the gist of it:

.. code-block:: python

   font = fontforge.open(font_path)
   selected = False
   for icon in icons:  # The list of icon names
       try:
           font.selection.select(("more",), icon)
           selected = True
       except ValueError:
           # icon not found in font
           pass

   if selected:
       font.selection.invert()
       font.clear()
       font.generate(output_path)

One by one, it loads each font, :code:`select`\s our desired icons that are
present in the font, and, if there are any, it inverts the selection and
deletes it. This leaves only our desired icons in the font, which is saved into
our output folder.

adding font awesome RST roles
-----------------------------

I wanted to add something extra for convenience, that is reStructuredText roles
that allow me to include font awesome fonts inline in my posts.

I added 3 roles: :code:`fas`, :code:`far`, and :code:`fab` for font awesome's
solid, regular and brands icon lists. These can be used like this:

.. code-block:: RST

   Here is the classic :fas:`blender-phone`.

Here is the classic :fas:`blender-phone`.  

result
------

Whenever I use a new icon, like the :fas:`poo-storm`, I simply use one of the
above RST roles in my draft and then pelican will include it when it copies
over font awesome's CSS and webfonts into the output folder.

Then I think about how much of my time I waste over-optimising tiny, tiny
things.
