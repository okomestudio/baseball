#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from collections import defaultdict
import re
from urllib import urlencode
from urlparse import urlunparse

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from fangraphs.items import BattingSplitItem, PitchingSplitItem


_NONE_VALS = ('', '- - -')

def s2type(x, factory):
    x = x.strip()
    if x.endswith('%'):
        x = x[:-1].strip()
    try:
        return factory(x)
    except:
        if x in _NONE_VALS:
            return None
        raise ValueError('cannot convert to {}: {}'
                         .format(type(factory), x))

s2int = lambda x: s2type(x, int)
s2float = lambda x: s2type(x, float)


class StatSplitsSpider(CrawlSpider):

    name = 'statsplits'
    allowed_domains = ['fangraphs.com']
    endpoint = 'http://www.fangraphs.com/statsplits.aspx'

    re_playerid = re.compile(r'.*playerid=(\d+)[!\d].*')
    
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

    def _parse_essential(self, response):
        playerid = self.re_playerid.match(response.url).group(1)
        data = defaultdict(dict)
        for i in xrange(1, 4):
            area = response.xpath('//div[@id="SeasonSplits1_dgSeason{}"]'
                                  .format(i))
            xp = area.xpath
            keys = xp('(.//thead//th/text())').extract()
            for n in xp('.//tbody/tr[not(contains(@class, "rgHeadSpace"))]'):
                tds = n.xpath('./td/text()').extract()
                data[tds[1]].update(dict((k, v) for k, v in zip(keys, tds)))
        return playerid, data

    def parse_pitching(self, response):
        playerid, data = self._parse_essential(response)
        for split, v in data.iteritems():
            item = PitchingSplitItem()
            item['playerid'] = playerid
            item['season'] = s2int(v['Season'])
            item['split'] = split
            xs = [int(x) for x in v['IP'].split('.')]
            item['ip_out'] = 3 * xs[0] + (xs[1] if len(xs) == 2 else 0)
            item['era'] = s2float(v['ERA'])
            item['tbf'] = s2int(v['TBF'])
            item['h'] = s2int(v['H'])
            item['h2'] = s2int(v['2B'])
            item['h3'] = s2int(v['3B'])
            item['r'] = s2int(v['R'])
            item['er'] = s2int(v['ER'])
            item['hr'] = s2int(v['HR'])
            item['bb'] = s2int(v['BB'])
            item['ibb'] = s2int(v['IBB'])
            item['hbp'] = s2int(v['HBP'])
            item['so'] = s2int(v['SO'])
            item['avg'] = s2float(v['AVG'])
            item['obp'] = s2float(v['OBP'])
            item['slg'] = s2float(v['SLG'])
            item['woba'] = s2float(v['wOBA'])
            item['k_per_9'] = s2float(v['K/9'])
            item['bb_per_9'] = s2float(v['BB/9'])
            item['k_per_bb'] = s2float(v['K/BB'])
            item['hr_per_9'] = s2float(v['HR/9'])
            item['k_perc'] = s2float(v['K%'])
            item['bb_perc'] = s2float(v['BB%'])
            item['k_minus_bb_perc'] = s2float(v['K-BB%'])
            item['whip'] = s2float(v['WHIP'])
            item['babip'] = s2float(v['BABIP'])
            item['lob_perc'] = s2float(v['LOB%'])
            item['fip'] = s2float(v['FIP'])
            item['xfip'] = s2float(v['xFIP'])
            item['gb_per_fb'] = s2float(v['GB/FB'])
            item['ld_perc'] = s2float(v['LD%'])
            item['gb_perc'] = s2float(v['GB%'])
            item['fb_perc'] = s2float(v['FB%'])
            item['iffb_perc'] = s2float(v['IFFB%'])
            item['hr_per_fb_perc'] = s2float(v['HR/FB'])
            item['ifh_perc'] = s2float(v['IFH%'])
            item['buh_perc'] = s2float(v['BUH%'])
            item['pitches'] = s2float(v['Pitches'])
            item['balls'] = s2float(v['Balls'])
            item['strikes'] = s2float(v['Strikes'])
            yield item

        req = Request(url=response.url.replace('position=P', 'position=PB'),
                      callback=self.parse_batting)
        yield req

    def parse_batting(self, response):
        playerid, data = self._parse_essential(response)
        for split, v in data.iteritems():
            item = BattingSplitItem()
            item['playerid'] = playerid
            item['season'] = s2int(v['Season'])
            item['split'] = split
            item['g'] = s2int(v['G'])
            item['ab'] = s2int(v['AB'])
            item['pa'] = s2int(v['PA'])
            item['h'] = s2int(v['H'])
            item['h1'] = s2int(v['1B'])
            item['h2'] = s2int(v['2B'])
            item['h3'] = s2int(v['3B'])
            item['hr'] = s2int(v['HR'])
            item['r'] = s2int(v['R'])
            item['rbi'] = s2int(v['RBI'])
            item['bb'] = s2int(v['BB'])
            item['ibb'] = s2int(v['IBB'])
            item['so'] = s2int(v['SO'])
            item['hbp'] = s2int(v['HBP'])
            item['sf'] = s2int(v['SF'])
            item['sh'] = s2int(v['SH'])
            item['gdp'] = s2int(v['GDP'])
            item['sb'] = s2int(v['SB'])
            item['cs'] = s2int(v['CS'])
            item['avg'] = s2float(v['AVG'])
            item['bb_perc'] = s2float(v['BB%'])
            item['k_perc'] = s2float(v['K%'])
            item['bb_per_k'] = s2float(v['BB/K'])
            item['obp'] = s2float(v['OBP'])
            item['slg'] = s2float(v['SLG'])
            item['ops'] = s2float(v['OPS'])
            item['iso'] = s2float(v['ISO'])
            item['babip'] = s2float(v['BABIP'])
            item['wrc'] = s2float(v['wRC'])
            item['wraa'] = s2float(v['wRAA'])
            item['woba'] = s2float(v['wOBA'])
            item['wrcp'] = s2float(v['wRC+'])
            item['gb_per_fb'] = s2float(v['GB/FB'])
            item['ld_perc'] = s2float(v['LD%'])
            item['gb_perc'] = s2float(v['GB%'])
            item['fb_perc'] = s2float(v['FB%'])
            item['iffb_perc'] = s2float(v['IFFB%'])
            item['hr_per_fb_perc'] = s2float(v['HR/FB'])
            item['ifh_perc'] = s2float(v['IFH%'])
            item['buh_perc'] = s2float(v['BUH%'])
            item['pitches'] = s2float(v['Pitches'])
            item['balls'] = s2float(v['Balls'])
            item['strikes'] = s2float(v['Strikes'])
            yield item
