ubuntu-touch on the pinephone: first impressions
================================================

:date: 2020-02-11
:summary: My first impression of testing ubuntu-touch on the pinephone
          BraveHeart release

My Braveheart edition PinePhone_ arrived a couple of days after a *long*
journey and I've finally got some time to play with it. The first thing I
wanted to do was test drive ubuntu-touch_, the mobile version of Ubuntu
maintained by the `UBports community`_, and I figured I'd write about my
experiences.


interface and responsiveness
----------------------------

My expectations were sensibly quite low given that it's still early days for
the pinephone, but I've got to say, I was pleasantly surprised by how
responsive and un-frustrating the UI is at this stage.

The keyboard, which sometimes was an issue for me when I tested postmarketOS_,
works 99% perfectly. There does appear to be a minor bug where keyboard sounds,
when enabled in the settings, are only triggered on the first key press after
the keyboard is opened. A low priority bug to be sure.

The app draw - displayed when swiping in from the left of the screen - feels
intuitive and looks great. Much more convenient access to apps than android
has. Swiping in the from the right of the screen gives a view of all running
apps, allow you to swipe them up to close them. These two very gesture-based
features are smooth and responsive and don't feel clunky at all.

.. image:: /static/UT_pinephone.jpg
    :width: 60%
    :align: center
    :alt: ubuntu-touch on pinephone: view of running apps

Dragging the bar at the top of the screen down (although *not* swiping down
from off the top of the screen) dispays a number of informational tabs much
like in android and iOS. There has been a little :fas:`envelope` icon on the
bar since it first booted suggesting a notifications pending, but the
notifications tab is pretty convinced that that is not the case.

.. raw:: html

   <video controls width="60%" class="align-center" src="/static/UT_pinephone.webm"></video>


hardware
--------

Much of the hardware is perfectly under control:

 - The volume buttons do indeed change the volume.
 - The lock/power button locks the screen, and turns it back on again.
 - Screen brightness control works.

But some is not:

 - Wifi appears to connect and work beautifully initially, but then fails.
   There is a working fix for when it does, however (discussion on `ubports
   <https://forums.ubports.com/topic/3791/wifi-issues-on-pinephone-braveheart/8>`_
   and `pine64 <https://forum.pine64.org/showthread.php?tid=8969>`_).
 - The *Rotation Lock* setting appears to do nothing; perhaps the gyro doesn't
   quite work yet.
 - Currently pinephone ubuntu-touch is stuck in headphone mode, and has other
   issues with the speakers (`pine64 discussion
   <https://forum.pine64.org/showthread.php?tid=8923>`_).
 - There also appears to be a an issue with the battery usage, that `others
   have also experienced`_, though this does appear to be an issue that can be
   fixed by software changes (fortunately!).


software
--------

It does seem pretty strange, SSH-ing into and exploring a phone from my
computer. Using apt to install tor or vim or whatever the hell I want. On my
phone. That novelty is yet to wear off.

A dozen or so apps came pre-installed with ubuntu-touch, and more can be
downloaded from the *OpenStore*. Many of these are simple web-apps, which has
enabled a huge range of 'apps' to be created already. Though some are buggy
(unsurprising, considering the webpages they display probably weren't designed
with this in mind), they do serve as stepping stones between having no apps and
eventually having native apps :fas:`praying-hands`.

We are in the midst of an incredibly exciting time for linux smart phones, and
I can't wait to see what the next few months bring us. I'm sure very soon we
will have all the necessary components of the pinephone working smoothly, and
once people make that transition to using it as a(n imperfect, yet functional)
daily driver, the new apps and functionality will hopefully boom.


.. _PinePhone: https://wiki.pine64.org/index.php/PinePhone
.. _ubuntu-touch: https://ubuntu-touch.io
.. _`UBports community`: https://ubports.com
.. _postmarketOS: https://postmarketos.org
.. _`others have also experienced`: https://forum.pine64.org/showthread.php?tid=9063
