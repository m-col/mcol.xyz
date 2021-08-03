Qtile: A Wayland Compositor
===========================

:date: 2021-08-03
:summary: Qtile: A Wayland Compositor

What is this? Qtile? A Wayland compositor? Wut? You're reading right my dudes,
now it is one. Since way before I joined the core Qtile dev team over a year
ago there has been a vague drift in the codebase moving the X11-specific code
into a :code:`backend` module with the aim of abstracting away the interface
the WM makes with the X server. The idea was that other backends could be
implemented and use the same higher-level management of windows, screens,
groups (virtual desktops), the status bar, etc. Over the past few months I've
been working on the first non-X11 backend: a Wayland compositor.

This backend -- which was part of the latest release a few weeks ago (0.18.0)
-- uses the Python CFFI wrapper around `wlroots
<https://github.com/swaywm/wlroots>`_ created by flacjacket, `pywlroots
<https://github.com/flacjacket/pywlroots>`_.  This in turn uses `pywayland
<https://github.com/flacjacket/pywayland>`_ also written by Sean. Through
pywlroots, Qtile gets access to the amazing work put in by the wlroots guys to
make constructing a compositor straight forward and hassle-free.

With the latest releases of the three projects above, launching Qtile as a
Wayland compositor is as simple as running the following from a TTY:

.. code-block:: python

   qtile start --backend wayland

With it fired up, the first thing to notice is.... nothing!

.. image:: /static/qtile_backend_wayland.png
   :alt: My Qtile desktop under the Wayland backend

\

.. image:: /static/qtile_backend_x11.png
   :alt: My Qtile desktop under the X11 backend

So what are we looking at here? These two screenshots are my desktop running
using the Wayland backend (top) and the X11 backend (bottom). Ignoring the
difference in terminal (foot and xterm), everything else is the same. The same
bar (Qtile's own bar), the same window borders, and (you'll have to take my
word for it), the same keybinding and mouse behaviour.

But why? Other than the totally valid reason of "it's awesome", I was getting
sick of the visual glitches and imperfection that inevitably come with X, and
this backend gives us pixel-perfect rendering [1]_. And testing them out one
after the other it is certainly noticable. We also get nice things like easier
to control clients (on the dev side *and* user side), `fewer buggy or slightly
misunderstood interfaces <https://github.com/qtile/qtile/issues/2404>`_, but I
don't need to supplement the many articles online about why Wayland is A Good
Thing.

Writing the backend was a great opportunity to refactor some of the code and
really isolate and modularise the X11-specific parts as these are not used when
ran for Wayland. It also helped shape the base classes required to create
further backends. Based on their signatures, one can implement custom backends
to handle whatever input-output setup one wants, be it a web-based compositor
like `Greenfield <https://github.com/udevbe/greenfield>`_ or a VR desktop
environment à la `Safespaces
<https://arcan-fe.com/2018/03/29/safespaces-an-open-source-vr-desktop/>`_.

I've got it running. What now?
------------------------------

The first thing some people will notice when running a Wayland Qtile for the
first time is that suddenly half of their programs no longer work. Many popular
programs run on X only and alternatives need to be found. This can be as simple
as replacing dmenu with `bemenu <https://github.com/Cloudef/bemenu>`_. Some
fine people have collected links to alternatives for popular programs, so if
this is what you want then check out `Are We Wayland Yet?
<https://arewewaylandyet.com/>`_ and natpen on GitHub's `Awesome Wayland
<https://github.com/natpen/awesome-wayland>`_ page.

Some programs, such as Firefox or GTK and Qt-based programs, require
environmental variables to be set for them to use their Wayland backend. For
more info check out this page on the `Sway wiki
<https://github.com/swaywm/sway/wiki/Running-programs-natively-under-wayland>`_.

Many other compositors, such as Sway, support compatibility with X-only windows
via the XWayland tool. This essentially serves as an X server that lets the
compositor handle the pixel buffers of all the X clients so it can embed them
within the Wayland desktop environment as regular windows. People who might
want to use this in Qtile are unfortunately out of luck, as XWayland support is
not implemented, and I am in favour of deferring its implementation
indefinitely as it would introduce much more complexity to the code for what is
ultimately a temporary workaround.

Input configuration
-------------------

The X server reads config files from :code:`/etc/X11/xorg.conf.d` to use when
configuring input devices managed via libinput. With many things, this becomes
the responsibility of the Wayland compositor. Currently there is no common
interface or configuration that can be shared between compositors, meaning each
compositor has to manually deal with libinput configuration itself. I *have*
implemented this in `this <https://github.com/qtile/qtile/pull/2548>`_ pull
request, but I agree with the consensus that this feels wrong to have within
Qtile. Sway does something similar; configuring libinput devices itself (with
identical config options to X or that Qtile PR).

It's a bad situation, but currently using the commit from that PR [2]_ is the
only alternative to getting used to your input devices' default settings. My
fingers and toes are crossed that a plug-and-play implementation comes onto the
Wayland scene with a config that all compositors could use.

But but... my dear drop shadows!
--------------------------------

In Wayland Qtile *is* the compositor so there can be no standalone compositing
manager like under X. If you use `picom <https://github.com/yshui/picom>`_ then
you need not worry about screen tearing at all, and transparency works native
and out-of-the-box. Window drop shadows, however, are something that would need
manual implementation within Qtile. In part I am hoping that somebody comes
along and decides to hack away at a plugin for Qtile that will do this, because
I do think drop shadows are out of the scope of Qtile proper. Alternatively if
the wlroots people decide it's worth making this a trivial job for compositors
then that would be even better. Either way, shadows are currently not possible.

A note about the Systray
------------------------

The crusty old Systray interface from X11 uses a very X-specific window
embedding protocol and as a result can't be supported outside of X (and even
with XWayland, it would only provide a systray interface for the X clients).

Instead, the desktop-agnostic `Status Notifier Item
<https://freedesktop.org/wiki/Specifications/StatusNotifierItem/>`_ dbus
interface provides a protocol through which clients can specify icons and
context menus for sticking in a system tray. This has roots in KDE's move to
Wayland and has been adopted by many other Wayland servers as well as many
client applications. Currently elParaguayo is `working on a widget
<https://github.com/qtile/qtile/pull/2601>`_ that will provide this systray
implementation, though this is a work in progress.

A couple remaining odd jobs
---------------------------

There are still some TODOs that need working on to make everybody happy:

 - Drag-and-drop
 - The configure-ack-configure dance with clients to get atomic layout changes and window resizes
 - Proper DPI and output scaling support
 - Lock-screen management - `ongoing discussion
   <https://github.com/swaywm/wlroots/issues/2706>`_ within wlroots is still
   deciding on how this should work in Wayland

-------------------------------------------------------------

.. [1] To be precise, it provides the *potential* for pixel-perfect rendering.
   This requires a back-and-forth sync between the server and clients when
   geometry is going to change, but this is not yet fully implemented in Qtile
   so when you resize a bunch of windows at the same time (e.g. moving a split
   in a tiled layout) they all move at the same time, but don't resize at the
   same time.

.. [2] Really I should extract the logic from that PR and put it into a
   standalone Python file that people can import into their configs and use
   that way. At least, until a better solution appears.
