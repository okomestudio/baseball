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


class StandardHitting(Item):

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
