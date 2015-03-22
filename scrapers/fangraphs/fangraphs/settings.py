#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

BOT_NAME = 'fangraphs'

SPIDER_MODULES = ['fangraphs.spiders']
NEWSPIDER_MODULE = 'fangraphs.spiders'

USER_AGENT = 'fangraphs scraper'

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'fangraphs'

DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
    'fangraphs.downloadermiddleware.proxy.ProxyMiddleware': 100,
}

SPIDER_MIDDLEWARES = {
    'fangraphs.spidermiddleware.errorpage.ErrorPageMiddleware': 50,
    #'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': None,
}

ITEM_PIPELINES = {
    'fangraphs.pipelines.FangraphsPipeline': 200,
}
