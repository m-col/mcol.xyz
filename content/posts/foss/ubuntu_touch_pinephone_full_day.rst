a full day test-driving ubuntu touch on the pinephone
=====================================================

:date: 2020-08-09
:summary: a full day test-driving ubuntu touch on the pinephone


My desk has had the Braveheart Edition of the `Pinephone
<https://wiki.pine64.org/index.php/PinePhone>`_ progressively gathering dust,
only seeing attention with a monthly flash of `Ubuntu Touch
<https://ubuntu-touch.io>`_ and a quick play around to check out the current
state. This week I reached the tipping point where UT finally had decent
performance and I was feeling particularly annoyed at my crappy android LG
phone, so yesterday I installed all the apps I might need with the intent of
spending my Sunday using only the pinephone. This is my experience from that
day.


11:00
-----

*100% charge*

Bluetooth won't turn off so hopefully that won't be too much of a power drain.
I need to leave wifi on - as i do with my "current" phone - but I only ever
turn 4G on when I need it (which is not often). Camera isn't working on UT yet.

Sending and receiving Signal messages works great with `Axolotl
<https://axolotl.chat/>`_, but it doesn't seem to read contact information from
the Contacts app, so at the minute I'm just seeing phone numbers and hoping I
don't message the wrong person. It also doesn't support push notifications or
phone calls :fas:`sad-tear`.


12:00
-----

*94% charge*

I have spent maybe 10 minutes with the screen on doing some light messaging
with Axolotl, sent a few texts, and checked Slack :fas:`grimace` using a web
app created by `Martin Kozub <https://zubozrout.cz>`_. If the battery indicator
is reliable then it should be able to last the day unless I start blasting
`tunes <https://asiwyfa.bandcamp.com/album/heirs-2>`_.


13:00
-----

*93% charge*

OK I'm starting to get a bit suspicious about the battery indicator.


14:30
-----

*75% charge*

This is probably the first time I've taken my pinephone outside, and I am at
the top of Arthur's Seat (Edinburgh). What I *wanted* to do was use this
opportunity to use location tracking with the GPS to find myself on the map,
take a screenshot of that working, and include that here. Instead, I just spent
20 minutes trying to get `uNav <https://github.com/costales/unav>`_ and `Pure
Maps <https://github.com/rinigus/pure-maps>`_ to find my location but neither
could do it. Also, neither asked me for permission to access GPS data so I
don't think they got very far in that endeavor.

So, no screenshot of a nice successful GPS usage, and of course no photos from
the camera, so instead have this nice photo taken by my girlfriend of Dunsapie
Loch at the bottom of Arthur's Seat:

.. image:: /static/dunsapie_loch.jpg
    :width: 80%
    :alt: Dunsapie Loch in Edinburgh

Oh, and, while I was bumbling around trying to get either of these apps to do
the right thing, UT locked me out of the phone and refused to present a
keyboard for pin entry, so I had to do a hard reset.


16:00
-----

*50% charge*

Considering how much I was faffing around trying to get the map to work, which
used plenty of data over 4G with the screen on maximum brightness, I am pretty
happy with a half-full battery after 5 hours.
 

Back at home
------------

Toward the lower end of the battery's capacity draining seemed to speed up,
even when idle:

* 18:00: 40% charge
* 18:15: 33% charge
* 18:30: 20% charge

Then I sat browsing reddit for 30 minutes or so using `Quickddit
<https://github.com/accumulator/Quickddit>`_, finally getting a 'Low Battery'
notification at 7pm with 9% battery. This prompted me to stop wasting my time
on reddit and put the phone down. When I checked it again 10 minutes later it
was dead.


Closing Thoughts
----------------

All in all, I got a decent bit of use out it, and I definitely used it more
than I would normally use my phone. In total it lasted around 8 hours.
Considering what it has been like in the past, this is a pretty big improvement
and definitely makes me more excited for how things can be. Of course, some
pinephone-specific things need to be worked out, such as the camera and GPS -
though these may be specific to Ubuntu Touch as I think others working on other
OSes have got the camera working.

The app ecosystem for UT has also grown considerably in the past few months,
and I'm amazed that I can send and receive Signal messages. I couldn't get any
of the WhatsApp clients from the Open Store to work but clearly that must be a
sign.

Although there are a number of big annoyances, UT on the pinephone has (for me)
reached the point where I would happily use it over android, so I think for the
time being I will keep trying to use it daily. I will, however, shift a bit of
focus onto `Mobian <https://mobian-project.org>`_ and maybe give that a whirl.
