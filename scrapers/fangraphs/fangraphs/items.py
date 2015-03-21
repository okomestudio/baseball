# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class FangraphItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BattingSplitItem(Item):

    playerid = Field()
    split = Field()
    g = Field()
    ab = Field()
    pa = Field()
    h = Field()
    h1 = Field()
    h2 = Field()
    h3 = Field()
    hr = Field()
    r = Field()
    rbi = Field()
    bb = Field()
    ibb = Field()
    so = Field()
    hbp = Field()
    sf = Field()
    sh = Field()
    gdp = Field()
    sb = Field()
    cs = Field()
    avg = Field()
    bb_perc = Field()
    k_perc = Field()
    bb_per_k = Field()
    obp = Field()
    slg = Field()
    ops = Field()
    iso = Field()
    babip = Field()
    wrc = Field()
    wraa = Field()
    woba = Field()
    wrcp = Field()
    gb_per_fb = Field()
    ld_perc = Field()
    gb_perc = Field()
    fb_perc = Field()
    iffb_perc = Field()
    hr_per_fb = Field()
    ifh_perc = Field()
    buh_perc = Field()
    pitches = Field()
    balls = Field()
    strikes = Field()
