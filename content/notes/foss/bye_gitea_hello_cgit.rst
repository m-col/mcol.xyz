bye gitea, hello cgit
=====================

:date: 2020-08-02
:summary: After a few months of running a gitea instance on my website, the
          headache of putting up with it's sluggishness became too strong and I
          needed to replace it with someone less heavy.

After a few months of running a gitea_ instance on my website, the headache of
putting up with it's sluggishness became too strong and I needed to replace it
with someone less heavy.

Before I had set up gitea, I read briefly about cgit_ and, although it
certainly looked attractive as a minimal, functional git server, gitea swayed
me with the (long ongoing) discussion about federation between gitea instances.
Federation between instances (and between gitea and gitlab instances, which has
also been brought up) would be a real game-changer in the code-forge world. I
don't deny that the practicality of github's interface has huge advantages;
bringing that interface along with the graphical pull request and CI toolbox
into the fediverse will definitely be a great thing to see. However this
discussion has so far yielded very little, so despite my crossed fingers it is
not currently a feature.

Without federation in sight, I was using gitea as a single-user github
substitute. The problem here is that these services are by design multi-user.
For a single-user instance, pull requests and profile pages become redundant,
all webpages and URLs concerning my repositories had to include my username,
and very little of this can be compromised on. I appear to not be the only one
expressing these woes - Jake Bauer has talked about his similar migration from
gitea to cgit on paritybit.ca_.

Moving to cgit was similar in experience to a well-made desktop program: a
simple runtime config, a comprehensive man page, and a straight forward way to
run it. After setting up the standard way (i.e. following the `arch wiki
page`_) and giving the manual a once-over, it just needed some tweaks to the
default CSS.

The most striking improvement has the page-loading time, particularly after
cgit has built up it's cache.

On the index page, cgit can order repositories by age which is nice - however
the dates all seemed to say the same thing. cgit seemed to be getting it's
timestamps from the filesystem directly, so running this inside each repository
was enough to change the timestamps on each file in a repository to that of the
latest commit:

.. code-block:: sh

    find . -type f -execdir touch -md "`git log -1 --pretty=format:"%ad" --date=iso`" {} \;

I also wanted to set up write access, so that I can git push over HTTP as I do
when pulling. cgit doesn't actually support this feature; this is with good
reason, as git itself provides the means to do this using git-http-backend_.
This can be used by an nginx server by adding a new location block as a sibling
to the one proxying requests to cgit. In case this is of use to anyone else who
uses cgit, here are my current read and write nginx location blocks:

.. code-block:: sh

    # This block normally passes read requests to cgit
    location ~ ^/code(?:/(.*))?$ {

        # These if statements redirect write requests to the block below
        if ($arg_service = git-receive-pack) {
            rewrite /code/(.*) /git-write/$1 last;
        }
        if ($uri ~ ^/code/.*/git-receive-pack$) {
            rewrite /code/(.*) /git-write/$1 last;
        }

        include                 fastcgi_params;
        fastcgi_param           SCRIPT_FILENAME /usr/lib/cgit/cgit.cgi;
        fastcgi_split_path_info ^(/code/?)(.+)$;
        fastcgi_param           PATH_INFO       $fastcgi_path_info;
        fastcgi_param           QUERY_STRING    $args;
        fastcgi_param           HTTP_HOST       $server_name;
        fastcgi_pass            unix:/run/fcgiwrap.socket;
    }

    # This block passes authenticated write requests to git-http-backend
    location ~ /git-write/(.*) {
        internal;
        auth_basic_user_file    /etc/nginx/htaccess/git;
        fastcgi_pass            unix:/run/fcgiwrap.socket;
        include                 fastcgi_params;
        fastcgi_param           SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
        fastcgi_param           GIT_HTTP_EXPORT_ALL "";
        fastcgi_param           GIT_PROJECT_ROOT /var/git;
        fastcgi_param           PATH_INFO /$1;
        fastcgi_param           REMOTE_USER $remote_user;
        client_max_body_size 0;
    }

With this setup, I can use :code:`git push` and it will let me update the
remote repository after prompting for the username and password stored in
:code:`/etc/nginx/htaccess/git`.

So far I am loving cgit for what it is: a way to organise, view and display my
projects without any unneeded features, and importantly without the need to go
into the web interface to modify any repo information, as repo metadata is
stored inside it's folder on the server.

I'm surprised I don't see more people using cgit, though I expect that as time
goes on and federation in code-forges becomes more of a thing that these more
sophisticated platforms will become more popular. Until then, I'm very pleased
with cgit.

.. _gitea: https://gitea.io
.. _cgit: https://git.zx2c4.com/cgit
.. _`arch wiki page`: https://wiki.archlinux.org/index.php/cgit
.. _git-http-backend: https://git-scm.com/docs/git-http-backend
.. _paritybit.ca: https://www.paritybit.ca/blog/switching-to-cgit
