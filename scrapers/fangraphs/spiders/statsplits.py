#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from urllib import urlencode
from urlparse import urlunparse

from scrapy.contrib.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider


class StatSplitsSpider(CrawlSpider):

    name = 'statsplits'
    allowed_domains = ['fangraphs.com']
    endpoint = 'http://www.fangraphs.com/statsplits.aspx'

    def __init__(self, *args, **kwargs):
        super(StatSplitsSpider, self).__init__(*args, **kwargs)

        playerids = []
        if 'playerid' in kwargs:
            playerids.append(kwargs['playerid'])

        inputfile = kwargs.get('inputfile')
        if inputfile:
            with open(inputfile) as f:
                playerids.extend([line.strip() for line in f])

        season = kwargs.get('season', 2014)

        urls = []
        for playerid in playerids:
            query = [
                ('playerid', playerid),
                ('season', season),
            ]
            url = urlunparse(
                ('http', 'www.fangraphs.com', '/statsplits.aspx', '',
                 urlencode(query), '')
            )
            urls.append(url)

        self.start_urls = urls

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        title = response.xpath('//head//title/text()').extract()[0].strip()
        self.log('Page title: ' + title)
        #self.log('here:' + response.url)
        #self.log('body:' + response.body)
        return None
