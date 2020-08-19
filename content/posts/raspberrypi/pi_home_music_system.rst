music that follows you around the house: part 1. streaming to multiple players
==============================================================================

:date: 2019-09-21
:summary: music that follows you around the house: part 1.

Often when I come across an amazing new record I'll play it on repeat all day,
every day for a week or two. My laptop's speakers are pretty decent, but
unfortunately they don't levitate nearby as I move around my home. Though that
is a problem I don't intend to solve, I figure the next best thing is have one
device stream music all around my home, but have it playing only in the room
that I am in.

This post is the first step on the way to set up this system. The aim for the
final setup is to have three parts:

* A central music server that has local access to my music library.
* Playback clients that, when somebody is in the room, play the music through connected speakers.
* Control clients that use the `MPD protocol
  <https://www.musicpd.org/doc/html/protocol.html>`_ to control playback from
  any other device on the network (i.e. PCs and phones).

I opted to use Raspberry Pis for the server and playback clients, for ease of
use and low energy consumption. By the end, playback clients will (hopefully)
be able to fully disconnect their speakers from the power when they are not
playing.


the music server
----------------

Starting with a pi that we can access over SSH, we need to give it access to
our music library (remember to stick the storage disk into :code:`/etc/fstab`
with auto-mounting) and install mpd:

.. code-block:: bash

    apt-get install mpd

Next, we need to configure mpd to stream its music throughout the local
network. There are a number of ways to do this, each with their pros and cons.
The most straightforward method is to use mpd's built-in httpd server.

To enable this, we need to add the following settings to :code:`/etc/mpd.conf`
(or alternatively :code:`$HOME/.config/mpd/mpd.conf`):

.. code-block:: bash

    music_directory "/path/to/music"
    db_file         "/path/to/database"
    log_file        "syslog"
    state_file      "/path/to/state_file"

    audio_output {
        type        "httpd"
        name        "Raspberry Pi Music Server"
        encoder     "flac"
        format      "44100:16:1"
        always_on   "yes"       # Stay connected to clients when music stops
        tags        "yes"       # Also stream tags
        port        "8000"
        max_clients "0"         # Allow unlimited clients
    }

    bind_to_address "any"   # allow remote access
    port            "6600"
    restore_paused  "yes"
    auto_update     "yes"
    user            "pi"    # run as user rather than root

This configuration makes mpd output audio via http on port 8000. Playback
clients can then listen in on this stream and play it on connected speakers.

On port 6600 we have the usual mpd protocol communication with the server,
which we can use to control music playback.

I've used :code:`encoder "flac"` for lossless streaming, though other options
can be used (`described here
<https://www.musicpd.org/doc/html/plugins.html#encoder-plugins>`_).

mpd is packaged with a systemd service that works well to manage its process
and logging. By using :code:`user "pi"` above we can take advantage of the
preconfigured sandboxing settings in this service by enabling it as is, before
the process is transferred to a non-root user. Enable it with:

.. code-block:: bash

    systemctl enable --now mpd.service

If we didn't use :code:`/etc/mpd.conf` and instead wanted to use a different
config file, we must change this line in :code:`/etc/default/mpd` to add the
config's path:

.. code-block:: bash

    MPDCONF=/etc/mpd.conf

Now on to the clients.


playback clients
----------------

mpd also works great for playing back http streams, so my playback clients are
also all Raspberry Pis with the mpd service enabled.

However, on these guys we need to configure the mpd config differently:

.. code-block:: bash

    bind_to_address "127.0.0.1"
    log_file        "syslog"
    state_file      "/path/to/state_file"

    audio_output {
        type        "alsa"
        device      "hw:0,0"
        name        "speaker"
    }

    restore_paused  "no"
    auto_update     "no"

We don't need remote access to mpd on these clients, as they just relay
whatever is being played from the main server. As we aren't managing a library
with this mpd instance we don't need to specify any paths for the music
directory or database. For this same reason we don't need to enable
auto_update. We also don't want to restore mpd into a paused state, because we
want to use only the main server to control playback.

With this audio_output configuration, music is output through the headphone
jack using alsa and out to speakers.

To make these clients listen to the http stream coming from the main server,
simply add its URL to the client's playlist and enable repeat. We can do this
using mpc:

.. code-block:: bash

    apt-get install mpc
    mpc repeat 1
    mpc add http://<server ip address>:8000

Now they'll stay connected to the http stream, playing it non-stop, so pausing
the main server's mpd pauses playback by all clients.

control clients
---------------

These clients are other devices we have on the network that we want to use to
control playback, such as phones or laptops. To do this, we communicate with
the main server using the MPD protocol to tell it what to do. Changes to
playback are propagated to the playback clients that are listening in on the
http stream.

To control the music, we simply need an mpd client pointed at the music serving
pi. My favourite client is ncmpcpp, which can be installed from most distro
package managers onto your PC. Using these arguments we can control the server:

.. code-block:: bash

    ncmpcpp --host <server ip address> --port 6600

I have not yet tested out many mpd clients so I will save that for a later
post. ncmpcpp is great for controlling the music from my PC, but if guests
wanted to control the music then a web interface served up from the main
raspberry pi might be a more convenient way for them to control it.

With the playback clients listening to the http stream, when we start playback
from the main server and if we haven't had any bad luck then we should be
hearing the music play!

If you don't hear anything playing from the pi's speakers, try with this line
added to :code:`/boot/config.txt`:

.. code-block:: bash

    dtparam=audio=on


next steps
----------

* Fade in/out volume as somebody walks in/out of each room.
* Explore different mpd client options.
* Address possible future issues with synchronisation of multiple players. If
  this becomes an issue, I may look into alternatives to the httpd output, such
  as the `real-time transport protocol
  <https://en.wikipedia.org/wiki/Real-time_Transport_Protocol>`_ via PulseAudio
  or VLC, or the more purpose-built server `snapcast
  <https://github.com/badaix/snapcast>`_.

In any case, the steps in this post alone are enough to set up a sweet remote
controlled speaker system!
