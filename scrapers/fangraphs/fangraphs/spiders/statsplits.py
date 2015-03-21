#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from collections import defaultdict
import re
from urllib import urlencode
from urlparse import urlunparse

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
from scrapy.http import Request

from fangraphs.items import BattingSplitItem


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

        years = kwargs.get('years', '2014')
        
        urls = []
        for playerid in playerids:
            for season in years.split(','):
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
        if re.search(r'(\?|&)position=P(&|$)', response.url):
            return self.parse_pitching(response)
        else:
            return self.parse_batting(response)

    def parse_pitching(self, response):
        title = response.xpath('//head//title/text()').extract()[0].strip()
        #self.log('P: ' + title)
        for i in xrange(1):
            item = BattingSplitItem()
            yield item

        req = Request(url=response.url.replace('position=P', 'position=PB'),
                      callback=self.parse_batting)
        yield req

    def parse_batting(self, response):
        playerid = re.match(r'.*playerid=(\d+)[!\d].*', response.url).group(1)
        
        data = defaultdict(dict)
        for i in xrange(1, 4):
            area = response.xpath('//div[@id="SeasonSplits1_dgSeason{}"]'
                                  .format(i))
            xp = area.xpath
            keys = xp('(.//thead//th/text())').extract()
            for n in xp('.//tbody/tr[not(contains(@class, "rgHeadSpace"))]'):
                tds = n.xpath('./td/text()').extract()
                data[tds[1]].update(dict((k, v) for k, v
                                         in zip(keys[2:], tds[2:])))
       
        for split, v in data.iteritems():
            item = BattingSplitItem()
            item['playerid'] = playerid
            item['split'] = split
            item['g'] = int(v['G'])
            item['ab'] = int(v['AB'])
            item['pa'] = int(v['PA'])
            item['h'] = int(v['H'])
            item['h1'] = int(v['1B'])
            item['h2'] = int(v['2B'])
            item['h3'] = int(v['3B'])
            item['hr'] = int(v['HR'])
            item['r'] = int(v['R'])
            item['rbi'] = int(v['RBI'])
            item['bb'] = int(v['BB'])
            item['ibb'] = int(v['IBB'])
            item['so'] = int(v['SO'])
            item['hbp'] = int(v['HBP'])
            item['sf'] = int(v['SF'])
            item['sh'] = int(v['SH'])
            item['gdp'] = int(v['GDP'])
            item['sb'] = int(v['SB'])
            item['cs'] = int(v['CS'])
            item['avg'] = float(v['AVG'])
            item['bb_perc'] = float(v['BB%'][:-2])
            item['k_perc'] = float(v['K%'][:-2])
            item['bb_per_k'] = float(v['BB/K'])
            item['obp'] = float(v['OBP'])
            item['slg'] = float(v['SLG'])
            item['ops'] = float(v['OPS'])
            item['iso'] = float(v['ISO'])
            item['babip'] = float(v['BABIP'])
            item['wrc'] = float(v['wRC'])
            item['wraa'] = float(v['wRAA'])
            item['woba'] = float(v['wOBA'])
            item['wrcp'] = float(v['wRC+'])
            item['gb_per_fb'] = float(v['GB/FB'])
            item['ld_perc'] = float(v['LD%'][:-2])
            item['gb_perc'] = float(v['GB%'][:-2])
            item['fb_perc'] = float(v['FB%'][:-2])
            item['iffb_perc'] = float(v['IFFB%'][:-2])
            item['hr_per_fb'] = float(v['HR/FB'][:-2])
            item['ifh_perc'] = float(v['IFH%'][:-2])
            item['buh_perc'] = float(v['BUH%'][:-2])
            item['pitches'] = float(v['Pitches'])
            item['balls'] = float(v['Balls'])
            item['strikes'] = float(v['Strikes'])
            yield item
