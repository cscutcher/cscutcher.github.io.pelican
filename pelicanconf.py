#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Scutcher'
SITENAME = u'Pure Wild Animal Craziness'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/cscutcher'),
    ('LinkedIn', 'https://uk.linkedin.com/in/cscutcher'),
    ('Google+', 'https://plus.google.com/+ChrisScutcher'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['filetime_from_git']

TYPOGRIFY = True

# Setup archive pages
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%b}/index.html'

# More specific category detection
USE_FOLDER_AS_CATEGORY = False
PATH_METADATA = '(?P<category>[^/]+).*'
