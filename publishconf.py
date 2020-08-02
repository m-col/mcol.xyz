#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

FEED_ATOM = 'rss.xml'
FEED_DOMAIN = ""

# css-html-js-minify
PLUGINS.append("css-html-js-minify")
