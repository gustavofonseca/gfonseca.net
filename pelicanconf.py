#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gustavo Fonseca'
SITENAME = u'Gustavo Fonseca'
SITEURL = ''
GITHUB_URL = 'http://github.com/gustavofonseca/'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

# Blogroll
LINKS = None

# Social widget
SOCIAL = (('github', 'http://github.com/gustavofonseca/'),
          ('twitter', 'http://twitter.com/gustavonseca/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# URL Pattern
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

