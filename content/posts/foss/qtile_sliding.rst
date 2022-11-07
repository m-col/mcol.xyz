interactive Mac-like workspace swiping for Qtile
================================================

:date: 2022-11-07
:summary: Implementing interactive Mac-like workspace touchpad swiping for
          Qtile

I recently added support for the wlroots :code:`wlr_pointer_gestures_v1`
protocol to Qtile's Wayland backend, primarily to relay multi-finger touchpad
events to clients. In unrelated news, I started a new job this week (which I
love) and they gave me a macbook (which I don't love). Having
:code:`wlr_pointer_gestures_v1` in recent memory and enjoying the macbook's
fancy interactive touchpad gestures, I figured it would be cool to see if such
gestures can be supported by Qtile.

The result of this weekend project was this pull request:
https://github.com/qtile/qtile/pull/3960.

At the highest level, this was a two-step process:

1. Hook up touchpad events in the backend to configurables logic so that users
   can create arbitrary bindings to gestures. 'Backend' here meaning the
   :code:`libqtile.backend.wayland` module that encapsulates Qtile's
   Wayland-specific code.
2. Create user commands for 'sliding' between groups (what Qtile calls
   workspaces).

Both parts enable new functionality, but when combined we can recreate the
interactive touchpad swiping to move between groups.

Swipe bindings
--------------

Users create :code:`Drag` objects to define mouse drag bindings. As
:code:`Drag`\s are used for interactive actions such as window moving and
resizing, they have an initial one-shot command to get/set any initial state,
and another command executed upon every movement. This is pretty similar to
what swiping bindings require, so fortunately very little additional code was
needed outside of the backend for the window manager to handle bindings.

As for the input handling, most of the heavy lifting is done by the
:code:`wlroots` library, specifically its helpers that Qtile uses to set up
devices and receive input events, including multi-touch touchpad gestures.
Consequently, Qtile's swipe bindings are limited to the Wayland backend, and
are not supported under X11.

For X11, existing standalone tools such as libinput-gestures_ and touchegg_ can
be used for touchpad gestures. They generally work by listening for gesture
events on the device and then when an event of interest is made, they run some
shell command. This unfortunately means that these tools only support one-shot
commands, and not interactive commands. Perhaps it would be possible to create
a CFFI wrapper around libinput in Qtile's X backend to support interactive
gestures, but I suspect this is non-trivial (reach out if you're is interested
in looking into this!).

Example uses
------------

The new :code:`Swipe` class is pretty much the same as :code:`Drag`, except it
needs a number of fingers rather than a button name. This :code:`Drag` example
is lifted from the default config, and below it is the equivalent
:code:`Swipe`, which is demonstrated in the video.

.. code:: python

    mouse = [
        ...

        Drag(
            [mod],
            "Button1",
            lazy.window.set_position_floating(),
            start=lazy.window.get_position(),
        ),
        Swipe(
            [mod],
            3,  # 3-finger gesture
            lazy.window.set_position_floating(),
            start=lazy.window.get_position(),
        ),
    ]

.. raw:: html

   <video controls width="100%" class="align-center" src="/static/qtile-drag.webm"></video>

Taking advantage of :code:`LazyCall.when()`, e.g.
:code:`lazy.function(zoom).when(focused=Match(wm_class="firefox"))` would let
you use swipe bindings conditional upon which window is focussed. The X11 tools
mentioned above often have this feature, but this addition to Qtile is the only
way to get even one-shot gesture-bound actions working in Wayland.

Sliding between groups
----------------------

The next step was to add commands to interactively and smoothly 'slide' between
one group and the next/previous. Fundamentally this mechanism is uncoupled from
the gestures mechanism above: if this was added without the ability to have
swipe bindings, one could expect to slide between groups using a mouse dragging
action via the existing :code:`Drag` configurable.

Indeed, the current (initial) state of the PR does support this, with bindings
for drags and swipes being very similar:

.. code:: python

    Drag(
        [mod, "shift"],
        "Button1",
        lazy.screen.slide_to_group(),
        start=lazy.screen.start_slide_to_group(scale=2.5),
    ),
    Swipe(
        [],
        4,
        lazy.screen.slide_to_group(),
        start=lazy.screen.start_slide_to_group(scale=2.5),
    ),

Here is a poor quality video trying to show how it works. Note that at a few
points I lifted my hands to end the gesture before moving more than half way
towards one of the adjacent workspaces. When that happens, we return to the
start. When the gesture ends, whether we're changing to the next/prev workspace
or returning to the start, there is a smooth animation transitioning the
compositor towards that point:

.. raw:: html

   <video controls width="100%" class="align-center" src="/static/qtile-swipe.webm"></video>

Neat, huh? This was fun to implement.

What's next?
------------

The possibility for pinch gestures via a new :code:`Pinch` configurable is low
hanging fruit, though I'm unsure what commands users might bind to them.
Enabling/disabling fullscreening the current window maybe?

For the workspace animations, these could potentially be one-shot,
non-interactive commands too. This would let users bind to a key press "slide
smoothly to the next workspace", which would be a new feature for those who
don't use trackpads, and indeed some people have already expressed interest in
this.

.. _libinput-gestures: https://github.com/bulletmark/libinput-gestures
.. _touchegg: https://github.com/JoseExposito/touchegg
