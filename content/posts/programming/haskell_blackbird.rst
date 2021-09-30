haskell study: pointfree rules, and the blackbird
=================================================

:date: 2021-09-30
:summary: haskell study: pointfree rules, and the blackbird

Since I started learning Haskell (not too long ago) it was never really clear
to me the benefits of writing functions in a pointfree style. It seemed that
doing so for relatively simple functions that would require minimal changes
made sense, such as the example from the Haskell `pointfree wiki page`_:

.. code-block:: haskell

   sum xs = foldr (+) 0 xs
   -- and pointfree:
   sum' = foldr (+) 0

Here, all it takes to make the function pointfree is omitting the argument.
Doing so removes some visual noise but it otherwise looks identical.

The thing is, this small change -- omitting the arguments while keeping the
rest unchanged -- is often not the only thing required to rewrite a function in
a pointfree form. For this reason I haven't had much drive to use pointfree
style for most functions that I write.

What changed my mind was Amar Shah's articles titled `Point-Free or Die`_ (and
`YouTube video`_). I won't repeat
things from there (much) but I highly recommend reading those articles or
watching the video.

While all of what he says is really interesting and worth reading, the crux of
the matter is that one can learn to recognise common function shapes so that
writing them in a pointfree style simply involves using something to map a
concise pointfree form to that shape. The blackbird (or B1) combinator is the
'something' that Amar identifies as what he needs to write his function in a
clear and elegant way:

.. code-block:: haskell

   blackbird :: (c -> d) -> (a -> b -> c) -> a -> b -> d
   blackbird f g x y = f (g x y)

The shape taken by a function that would make use of the blackbird is a
function that takes two arguments (:code:`a` and :code:`b` above) and inputs
these into one function and pipes the output of that into another function.
Without using this combinator, the pointfree version is otherwise left in this
more obscure form:

.. code-block:: haskell

   func :: a -> b -> d
   func = (f .) . g

While one could argue that bringing another object into the mix complicates
things further, being aware of this and `other such combinators`_ means that
when familiar shapes appear in your functions there is a go-to combinator in
your toolbox to represent that shape. Together, these combinators account for a
wide variety of function shapes, letting us write many more functions elegantly
in pointfree style with only a little extra work.

Plus, isn't it pretty?:

.. code-block:: haskell

   (.:) = blackbird  -- A common blackbird infix operator
   func = f .: g

.. _`pointfree wiki page`: https://wiki.haskell.org/Pointfree
.. _`Point-Free or Die`: https://amar47shah.github.io/posts/2016-08-28-point-free-part-2.html
.. _`YouTube video`: https://www.youtube.com/watch?v=seVSlKazsNk
.. _`other such combinators`: https://hackage.haskell.org/package/data-aviary-0.4.0/docs/Data-Aviary-Birds.html
