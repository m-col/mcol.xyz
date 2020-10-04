bye cgit, hello stagit
======================

:date: 2020-10-04
:summary: Not long ago I migrated my code hosting from a gitea instance to
          cgit, but now that's been replaced by stagit

It was only around 2 months ago when I `replaced my gitea instance`_ with cgit_,
but now I've replaced it with an even simpler alternative: stagit_.

cgit, as per the name, is an application that uses `Common Gateway Interface`_
(CGI) to serve dynamically generated web pages displaying information about the
remote git repositories on your server. The CGI approach lets cgit check for
updates to repositories when pages are requested in order to update these pages
and its cache.

stagit, on the other hand, is a command that generates static HTML pages from a
repository just once when called. This reduces load on the server, as the pages
can then be served directly without any dynamic page generation. The author has
a blog post with some more information here_.

As the scope of stagit is limited to generation of HTML pages, any requests on
the server from git commands -- i.e. fetching or pushing -- must be handled by
something else if they are to be supported. For this I am using
git-http-backend_, to which nginx forwards requests that contain specific query
strings.


git hooks and regeneration
--------------------------

But how to update the pages? As stagit is a simple command invoked just to
create new pages, it needs to called when git repositories are updated. For
this, we can write a simple post-receive hook and link it into each of our
repositories. Something like this, where our repos are in :code:`/var/git` and
the output HTML files are saved into :code:`/var/www/code`:

.. code-block:: sh

    # /var/git/<repo>/hooks/post-receive.d/update-stagit
    REPO=$(pwd)
    REPONAME=$(basename $REPO)
    cd /var/www/code/$REPONAME || cd /var/www/code/${REPONAME//.git} || exit 1
    stagit $REPO
    stagit-index /var/git/* > /var/www/code/index.html

This will be executed at the end of every :code:`git push` that updates the
repository, regenerating both the index page and the pages that pertain to the
that repository.


ordering the index page
-----------------------

You'll notice in the above snippet that there is a dedicated command for
generating the index page, :code:`stagit-index`. The order of the repos on the
index page is determined by the order of the arguments passed to this. To order
these by most recent commit, I made a quick Python wrapper:

.. code-block:: python

    # stagit-index.py
    import git
    import subprocess
    from pathlib import Path

    REPOS = []
    COMMAND = ["/usr/local/bin/stagit-index"]

    for path in Path("/var/git").glob('**/objects'):
        REPOS.append(
            (git.Repo(path.parent).head.commit.committed_date, path.parent)
        )

    COMMAND.extend([x for _, x in sorted(REPOS, key=lambda i: i[0], reverse=True)])
    subprocess.call(COMMAND)

Then all I need to do is run this little script and the index page will display
the repositories with the most recent updates first.


hacking the source
------------------

As the source code is neat and simple, it's very easy to make changes to
customise the behaviour. For example, I wanted every page to use the same
global stylesheet, rather than using a hard-coded path beside the given page. I
also removed the "Owner" column from the index page. Changes such as these --
essentially modifying the HTML template used -- are unfortunately impossible
with cgit, although some larger forges such as gitea do have full HTML template
systems.

Indeed, reading the source code it is clear that it would not be too difficult
to create a similar program that does exactly what you want. Though, if a
similar program took advantage of an HTML templating engine, then hacks such as
these may no longer be necessary. That would be more flexible... but where's
the fun in that?


.. _replaced my gitea instance: {filename}/posts/foss/bye_gitea_hello_cgit.rst
.. _cgit: https://git.zx2c4.com/cgit
.. _stagit: https://git.codemadness.org/stagit
.. _Common Gateway Interface: https://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _here: https://codemadness.org/stagit.html
.. _git-http-backend: https://git-scm.com/docs/git-http-backend
