#!/usr/bin/env python
# -*- coding: utf-8 -*- #


from __future__ import unicode_literals
import os
import sys
sys.path.append(os.curdir)
from blogroll import BLOGROLL


SITEURL = '//'
AUTHOR = 'mcol'
SITENAME = 'mcol.xyz'
PATH = 'content'
TIMEZONE = 'UTC'
THEME = '/home/mcol/git/mcol.xyz-theme'
PAGE_PATHS = ['pages',]
ARTICLE_PATHS = ['posts',]
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
STATIC_PATHS = ['static', 'favicon.png', 'icons', 'avatar.png']
PLUGIN_PATHS = ["/home/mcol/git", "/home/mcol/git/pelican-plugins"]
PLUGINS = []
RELATIVE_URLS = True

ARCHIVES_TITLE = 'posts'
ARCHIVES_SAVE_AS = 'posts.html'
AUTHORS_SAVE_AS = ''
TAGS_SAVE_AS = ''
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
USE_FOLDER_AS_CATEGORY = True
CATEGORIES_SAVE_AS = 'categories.html'
AUTHOR_SAVE_AS = ''
DISPLAY_CATEGORIES_ON_MENU = False


# Theme
ICONS = (
    ('/icons/home.png', 'Home', '/'),
    ('/icons/git.png', 'My git repositories', '/code/'),
    ('/icons/mastodon.png', 'Me on Mastodon', 'https://fosstodon.org/@mcol rel=me'),
    ('/icons/email.png', 'Email me', 'mailto:mcol@posteo.net'),
    ('/icons/github.png', 'Me on GitHub', 'https://github.com/m-col'),
    ('/icons/liberapay.png', 'Me on Liberapay', 'https://liberapay.com/mcol'),
    ('/icons/onion.png', 'Onion service', 'http://mcolxyzogp3cy4czf52oa2svu2vjge3otm3shxmtvwshyum47sis3iid.onion'),
    ('/icons/rss.png', 'RSS feed', '/rss.xml'),
)

AVATAR = "/avatar.png"
HOME1 = "A hobbyist's notes on FOSS, linux toys and privacy tools"
HOME2 = "~ Welcome ~"
EXTRAHEAD = "<link rel=stylesheet href=/theme/css/fa.css />"
EXTRATAIL = "<script data-goatcounter=https://goat.mcol.xyz/count async src=//goat.mcol.xyz/count.js></script>"

# minify-fontawesome
PLUGINS.append("pelican-minify-fontawesome")
MINIFY_FONTAWESOME = '/home/mcol/git/mcol.xyz/fontawesome-free-5.11.2-web'


# development settings
DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
