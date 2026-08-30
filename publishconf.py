#!/usr/bin/env python
# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

FEED_ATOM = "rss.xml"
FEED_DOMAIN = SITEURL

# Static files must be real copies, not symlinks, for a GitHub Pages
# deployment (the git tree pushed to gh-pages won't contain the content/
# directory the dev-mode symlinks point back into).
STATIC_CREATE_LINKS = False
