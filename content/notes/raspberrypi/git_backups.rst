minimal but complete nightly backups to raspberry pi
====================================================

:date: 2019-04-25
:summary: minimal but complete nightly backups to raspberry pi

I searched far and wide for an effective backup solution for my laptop that
wasn't overkill.

When I first converted to linux I used programs like `timeshift
<https://github.com/teejee2008/timeshift>`_ and `backintime
<https://github.com/bit-team/backintime>`_ and although they worked well, I
wanted more fine grain control over what was backed up and less meat on what
should be a lightweight background process.

In my quest I stumbled upon this `Hacker News discussion
<https://news.ycombinator.com/item?id=11070797>`_ about turning your home
directory into a git working tree, where its .git folder is in some other
folder, out of the way. This setup stops your home git repo from getting in the
way of any git folders you have in your home directory, but has some problems:

- you need to remember to use the alias or folder names for this git repo to
  use the correct .git folder and working tree

- working tree changes won't get picked up by utilities like zsh prompts or
  ranger, so you might not always remember when things have changed

- to not pick up every single file in your home directory, these setups
  generally ignore untracked files. This requires you to remember to manually
  add any new config files in the future

Maybe I just have a poor memory.

A slight adjustment of this is to just use the :code:`$HOME/.config` folder for
what it was intended: storing your config files. Turning this folder into your
dotfiles repository, you can treat it as any other git repo.

Most programs can keep their configs in this folder, but the few that don't can
simply have their configs symlinked into place from the repo. This symlinking
make up the only scripting that would be required to install the repo into
another machine.

It makes sense to git track configuration files, but your photos, music and
documents? git is not going to like that. This calls for a small bit of
scripting to rsync these folders and push the .config repo to a remote
location.

First we need the location: a raspberry pi, ticking away somewhere hidden in
your flat, wired to an external hard drive. With one up and running, stick your
hard drive into the pi's :code:`/etc/fstab`:

.. code-block:: conf

    /dev/disk/by-uuid/1234-abcd /mnt/backups ext4 auto,rw,nofail,noatime,nosuid,noexec 0 0

Make sure your user has write access to the hard drive and then create the
remote repo for the configs:

.. code-block:: bash

    mkdir -m 1777 /mnt/backups/dotfiles
    cd /mnt/backups/dotfiles
    git init --bare

Make any additional folders for each folder in your home directory that will be
backed up:

.. code-block:: bash

    mkdir /mnt/backups/{documents,music,pictures}

While we're on the rasperry pi, let's configure some hard drive power
management so the hard drive spins down soon after the daily backup to save
some power. First install :code:`hdparm`, then set the power management and
spin down settings (see the `Arch wiki
<https://wiki.archlinux.org/index.php/Hdparm#Power_management_configuration>`_
for more info).

.. code-block:: bash

    apt-get install hdparm
    hdparm -B 127 /dev/disk/by-uuid/1234-abcd   # best performance permitting spin-down
    hdparm -S 241 /dev/disk/by-uuid/1234-abcd   # spin down after 30 minutes

Back on the laptop, we write the backup script, substituting where necessary:

.. code-block:: bash

    pi_IP=192.168.1.2
    pi_drive="pi@$pi_IP:/mnt/backups"

    rsyncargs="--recursive --links --times --partial --delete --compress --perms --verbose"
    
    # this environmental variable lets cron use notify-send for user ID 1000
    export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
    
    if ping $pi_IP -c 1 
    then
        notify-send "Nightly backup to pi" "Backup starting..."
    else
        notify-send "Nightly backup to pi" "Couldn't ping pi"
        exit    # exit if we can't ping the pi - are you still at work?
    fi
    
    {
        # dotfiles
        git --git-dir=$HOME/.config/.git/ --work-tree=$HOME/.config add -A
        git --git-dir=$HOME/.config/.git/ --work-tree=$HOME/.config commit -m "cron commit"
        git --git-dir=$HOME/.config/.git/ --work-tree=$HOME/.config push || errors=true
    
        # other folders
        rsync $rsyncargs \
    	--exclude=path/to/folder/you/want/to/exclude \
    	$HOME/documents/ $pi_drive/documents/ || errors=true
    
        rsync $rsyncargs $HOME/pictures/    $pi_drive/pictures/  || errors=true
        rsync $rsyncargs $HOME/music/       $pi_drive/music/     || errors=true

    # catch the output into a file in case we need it
    } | tee -a /tmp/BACKUPLOG-$(date +%y%m%d-%H%M%S)
    
    # notify with outcome
    if ${errors:-false}
    then
        notify-send "Nightly backup to pi" "Completed with error(s)"
    else
        notify-send "Nightly backup to pi" "Completed successfully."
    fi

This can easily be run by cron, e.g.:

.. code-block:: bash

    # backup nightly at 9.30 pm
    30 21 * * * $HOME/bin/nightly_backup

Now every night at 9.30 your home directory will get backed up to the raspberry
pi if you're at home. If it doesn't work for whatever reason, you'll get
notified of the error and you can check out the log in the /tmp folder.

Complement this with `etckeeper
<https://wiki.archlinux.org/index.php/etckeeper>`_ to back up system files and
this simple and lightweight setup can restore your machine in no time.
