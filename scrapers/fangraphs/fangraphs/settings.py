# -*- coding: utf-8 -*-

# Scrapy settings for fangraph project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fangraphs'

SPIDER_MODULES = ['fangraphs.spiders']
NEWSPIDER_MODULE = 'fangraphs.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'fangraphs (+http://www.mydomain.com)'

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'fangraphs'

DOWNLOAD_DELAY = 0.10 #2.0
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
    'fangraphs.downloadermiddleware.proxy.ProxyMiddleware': 100,
}

SPIDER_MIDDLEWARES = {
    'fangraphs.spidermiddleware.errorpage.ErrorPageMiddleware': 50,
    #'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': None,
}
