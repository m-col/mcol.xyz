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
THEME = '/home/mcol/git/rice-theme'
PAGE_PATHS = ['pages',]
ARTICLE_PATHS = ['notes',]
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
#STATIC_PATHS = ['static', 'favicon.png']
STATIC_PATHS = ['static']
PLUGIN_PATHS = ["/home/mcol/git", "/home/mcol/git/pelican-plugins"]
PLUGINS = []
RELATIVE_URLS = True

ARCHIVES_TITLE = 'notes'
ARCHIVES_SAVE_AS = 'notes.html'
AUTHORS_SAVE_AS = ''
TAGS_SAVE_AS = ''
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
USE_FOLDER_AS_CATEGORY = True
CATEGORIES_SAVE_AS = 'categories.html'
AUTHOR_SAVE_AS = ''
DISPLAY_CATEGORIES_ON_MENU = False


# rice layout
MENUITEMS = (
    ('code', '/code'),
    ('about', '/about.html'),
    ('onion', 'http://mcolxyzogp3cy4czf52oa2svu2vjge3otm3shxmtvwshyum47sis3iid.onion'),
)

ICONITEMS = (
    ('fab fa-mastodon', 'https://fosstodon.org/@mcol" rel="me'),
    ('fas fa-envelope', 'mailto:mcol@posteo.net'),
    ('fas fa-rss', '/rss.xml'),
)

SITESUBTITLE = "A hobbyist's notes on FOSS, linux toys and privacy tools"
MENUPADTO = 8
EXTRAHEAD = """<link rel="stylesheet" href="/theme/css/fa.css" />
    <script async defer src="/matomo/404.js"></script>"""
PRIVACYPOLICY = """I collect some but very little and 100% anonymous data to get a vague
sense of what pages are visited, if any, and from what websites visitors come from. That
is its only use, and its only by me, only on my machine."""


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
