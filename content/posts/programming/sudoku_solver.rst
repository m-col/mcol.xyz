solving sudoku puzzles with haskell
===================================

:date: 2022-04-03
:summary: solving sudoku puzzles with haskell

My weekend project was to implement an algorithm for solving sudoku_ puzzles,
and finally at 2am last night I had success.

Solving sudoku puzzles is a common exercise in implementing recursive
algorithms, much like the classic Fibonacci number algorithm, but unlike the
latter it involves a very deeply nested decision space. An algorithm must
traverse down an incorrect solution (exploring a given decision) in order to
determine if it is incorrect. At that point, it must backtrack_ and test out a
different decision. [1]_

This decision space can be represented as a tree, where each decision is a node
with 9 children. Each of the 9x9 cells represents one *level* of the decision
tree. The full decision tree therefore has :code:`9^81` leaves [2]_. A
backtracking algorithm scans this decision tree with brute force, checking if a
given decision is valid, and if it isn't then it prunes that decision's
subtree. If all 9 children of a node are invalid based on the puzzle's rules,
then we know that node must be invalid too, and we can prune it and test a
sibling subtree. Iterating through the tree this way, we eventually reach the
last level with our complete puzzle.

Sounds simple enough! Implementation may be another thing...

At this point if you haven't tried to implement a solution but want to give it
a go, I suggest waiting until you have before reading on.

My solution can be found at `/code/sudoku-solver`_, and looks like this while
it's running:

.. image:: /static/sudoku_solver.gif
    :alt: GIF of a puzzle being solved.

This problem sounds like a perfect fit for Haskell, like everything, but
specifically because Haskell's laziness allows us to 'pretend' to represent the
entire tree without actually requiring it ever be evaluated. For anybody who is
not familiar with Haskell, a more simple demonstration of this behaviour is
that we can use infinite lists, such as :code:`posInts = [1..]`, and things
work otherwise 'as you expect' because values are evaluated at access.

Going back to the giant decision tree, when we are making our first decision --
*"what value should we put in the first (empty) cell?"* -- we can simply map
over all of the valid options with the same decision function recursively.
Validity is determined by the known state of the puzzle (the initial values).

To illustrate, here is semi-Pythonic pseudo-code:

.. code-block:: python

    def attempt(state, cell) -> State | None:
        if is_beyond_last_cell(cell):
            # We need a way to check if the caller attempted to resolve the
            # very last cell.
            return state

        if not_empty(state[cell]):
            # This cell is filled, continue to find the next empty cell.
            return attempt(state, cell + 1)

        # Let's test values in this empty cell
        for candidate in valid_children(state, cell)
            result = attempt(candidate, cell + 1)

            if result is not None:
                # We have found the answer!
                return result

        return None

    attempt(initial_state, (1, 1))

OK, so what's going on?

1. First, we pass in the initial state -- our 9x9 grid with a small number of
   cells filled in -- and the coordinate for the first cell :code:`(1, 1)`.
2. Inside :code:`attempt`, the first thing we do is check if we've gone beyond
   the last coordinate. If we have, the parent call has filled the grid, and we
   should just return the state.
3. If that isn't the case, we check if the passed coordinate is completed. If
   it is, no problem, let's just continue to look at the next cell.
4. If our cell of interest is empty, let's get its valid children. That is, if
   we stick in the numbers 1 though 9, which candidate states don't conflict
   with existing values? Then, recurse on :code:`attempt` with those candidate
   states.
5. In the case where no children states are valid, we return :code:`None`, and
   the calling function continues its loop over sibling candidate states.

If the initial state is valid, then one series of :code:`attempt` calls will
make a path down to the final cell and we'll be left with the complete state,
which is returned all the way up the call stack!

The 'backtracking' here is implicitly encoded within the optional return type.
If a decision is made in a given stack frame and we find out that all
grandchildren are invalid, a :code:`None` is returned to us, and we continue
with a new value in the current cell. If that was the last valid candidate at
this level, this frame returns :code:`None` to backtrack to the parent.

Haskell's lazy evaluation helps us keep the code concise because we can
declaratively describe the traversal of our algorithm over the decision tree,
and then only when we ask, for instance, for the first result, does evaluation
proceed until we get it. If we asked for another result, traversal would need
to continue to the very end before it could determine that there are no more
possible results. This could be implemented in Python with generators, which
similarly defer evaluation until an item is needed.

This was one of those exercises that is really fun to reason about, and often
funny at the end when you realise the final implementation is much simpler than
many of the ideas you come up with while figuring it out. If you have any other
interesting problems I'd love to hear them so I can give them a go!

.. _sudoku: https://en.wikipedia.org/wiki/Sudoku
.. _backtrack: https://en.wikipedia.org/wiki/Backtracking
.. _`/code/sudoku-solver`: /code/sudoku-solver

-------------------------------------------------------------

.. [1] I should note that there are non-backtracking algorithms for solving
   sudoku puzzles too. See:
   https://en.wikipedia.org/wiki/Sudoku_solving_algorithms.
.. [2] That's 196627050475552913618075908526912116283103450944214766927315415537966391196809!
