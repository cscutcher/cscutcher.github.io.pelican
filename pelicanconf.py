#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Scutcher'
SITENAME = u'Pure Wild Animal Craziness'
SITEURL = 'http://www.ninebysix.co.uk'
DEFAULT_LANG = u'en'
TIMEZONE = 'Europe/London'

PATH = 'content'
STATIC_PATHS = ['images', 'CNAME']


DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['./pelican-plugins']
# Define plugins as we go
PLUGINS = []

TYPOGRIFY = True

# More specific category detection
USE_FOLDER_AS_CATEGORY = False
PATH_METADATA = '(?P<category>[^/]+).*'

# Don't use caches. Won't work for travis anyway
CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False

# Use relative links when building locally
import os
if os.environ.get('USER', None) == 'cscutcher':
    RELATIVE_URLS = True

###############################################################################
# archives                                                                    #
###############################################################################
# Setup archive pages
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%b}/index.html'

###############################################################################
# feeds                                                                       #
###############################################################################
FEED_DOMAIN = SITEURL

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category/%s.atom.xml'
TAG_FEED_ATOM = 'feeds/tag/%s.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/category/%s.rss.xml'
TAG_FEED_RSS = 'feeds/tag/%s.rss.xml'

TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

##############################################################################
# md_inline_extension                                                        #
##############################################################################
PLUGINS.append('md_inline_extension')
MD_INLINE = {
}


###############################################################################
# interlinks                                                                  #
###############################################################################
PLUGINS.append('interlinks')
INTERLINKS = {
    'wikipedia_en': 'http://en.wikipedia.org/wiki/',
    'wiki': 'http://en.wikipedia.org/wiki/',
    'github': 'https://github.com/',
    'githubp': 'https://github.com/cscutcher',
}

###############################################################################
# filetime_from_git                                                           #
###############################################################################
PLUGINS.append('filetime_from_git')
GIT_SHA_METADATA = True
GIT_GENERATE_PERMALINK = True
GIT_HISTORY_FOLLOWS_RENAME = True

###############################################################################
# permalinks                                                                  #
###############################################################################
PLUGINS.append('permalinks')

###############################################################################
# render_math                                                                 #
###############################################################################
PLUGINS.append('render_math')

###############################################################################
# liquid_tags                                                                 #
###############################################################################
PLUGINS.extend([
    'liquid_tags.img',
    'liquid_tags.video',
    'liquid_tags.youtube',
    'liquid_tags.vimeo',
    'liquid_tags.include_code',
])

###############################################################################
# Theme config                                                                #
###############################################################################
THEME = 'pure-single'
SOCIAL = (
    ('github', 'https://github.com/cscutcher'),
    ('linkedin', 'https://uk.linkedin.com/in/cscutcher'),
    ('google-plus', 'https://plus.google.com/+ChrisScutcher'),
    ('steam', 'https://steamcommunity.com/id/zoolie/')
)

MENUITEMS = (
    ('Blog', 'category/blog'),
    ('Snippets', 'category/snippets'),
    ('About', 'pages/about_me'),
)

# Blogroll
LINKS = ()

COVER_IMG_URL = '/images/cover_img.png'
PROFILE_IMG_URL = '/images/avatar.jpeg'
TAGLINE = 'Personal Homepage of Chris Scutcher, Esq.'
ENABLE_GOOGLE_COMMENTS = True

MD_EXTENSIONS = [
    'fenced_code',
    'codehilite(css_class=highlight)',
    'extra',
    'admonition',
    'toc',
]
