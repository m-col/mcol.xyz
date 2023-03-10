#!/usr/bin/env python

import os
import sys
from html import escape

sys.path.append(os.curdir)
from blogroll import BLOGROLL

SITEURL = "https://mcol.xyz"
AUTHOR = "mcol"
SITENAME = "mcol.xyz"
PATH = "content"
TIMEZONE = "UTC"
THEME = "/home/mcol/git/mini-theme"
PAGE_PATHS = [
    "pages",
]
ARTICLE_PATHS = [
    "posts",
]
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
STATIC_PATHS = ["static", "favicon.png", "icons", "avatar.png", "screenshots"]
STATIC_CREATE_LINKS = True
PLUGIN_PATHS = ["/home/mcol/git", "/home/mcol/git/pelican-plugins"]
PLUGINS = []
RELATIVE_URLS = True

ARCHIVES_TITLE = "posts"
ARCHIVES_SAVE_AS = "posts.html"
AUTHORS_SAVE_AS = ""
TAGS_SAVE_AS = ""
ARTICLE_URL = "{date:%Y}/{date:%m}/{slug}.html"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{slug}.html"
USE_FOLDER_AS_CATEGORY = True
CATEGORIES_SAVE_AS = "categories.html"
AUTHOR_SAVE_AS = ""
DISPLAY_CATEGORIES_ON_MENU = False


# Theme
ONION = "http://mcolxyzogp3cy4czf52oa2svu2vjge3otm3shxmtvwshyum47sis3iid.onion"
LINKS = (
    ("mastodon", "https://fosstodon.org/@mcol", "hit me up to chat!"),
    ("email", "mailto:mcol@posteo.net", "or here, if you want"),
    ("github", "https://github.com/m-col", "this i use when i must"),
    #("blog onion", ONION, "feeling edgy and/or paranoid?"),
    ("blog RSS feed", "/rss.xml", "follow me if you'd like"),
)

ABOUT = """
<p>Welcome to my blog!</p>
<p>I'm Matt and I write about open source software that I stumble across surfing the web.</p>
<p>Some of my main interests are self-hosting, functional programming, and anything
to do with <a href=https://wiki.installgentoo.com/wiki/GNU/Linux_ricing>ricing</a> (see
mine <a href="/screenshots.html">here</a>).</p>
"""

AVATAR = "/avatar.png"
HOME1 = "One more person's notes on FOSS, code and unix toys"
HOME2 = "Welcome"
EXTRAHEAD = "<link rel=stylesheet href=/theme/css/fa.css />"
EXTRATAIL = ""
ARTICLE_FEEDBACK = """If you have any thoughts, comments, criticisms, feel free to reach
out on <a href="https://fosstodon.org/@mcol">mastodon</a> or by <a
href="mailto:mcol@posteo.net">email</a> ?????????????"""

SCREENSHOTS = reversed([escape(i) for i in os.listdir("content/screenshots")])

# minify-fontawesome
PLUGINS.append("pelican-minify-fontawesome")
MINIFY_FONTAWESOME = "/home/mcol/git/mcol.xyz/fontawesome-free-5.11.2-web"


# development settings
DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
