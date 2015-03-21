#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from scrapy import Field, Item


class BattingSplitItem(Item):

    playerid = Field()
    season = Field()
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
    hr_per_fb_perc = Field()
    ifh_perc = Field()
    buh_perc = Field()
    pitches = Field()
    balls = Field()
    strikes = Field()


class PitchingSplitItem(Item):

    playerid = Field()
    season = Field()
    split = Field()
    ip_out = Field()
    era = Field()
    tbf = Field()
    h = Field()
    h2 = Field()
    h3 = Field()
    r = Field()
    er = Field()
    hr = Field()
    bb = Field()
    ibb = Field()
    hbp = Field()
    so = Field()
    avg = Field()
    obp = Field()
    slg = Field()
    woba = Field()
    k_per_9 = Field()
    bb_per_9 = Field()
    k_per_bb = Field()
    hr_per_9 = Field()
    k_perc = Field()
    bb_perc = Field()
    k_minus_bb_perc = Field()
    whip = Field()
    babip = Field()
    lob_perc = Field()
    fip = Field()
    xfip = Field()
    gb_per_fb = Field()
    ld_perc = Field()
    gb_perc = Field()
    fb_perc = Field()
    iffb_perc = Field()
    hr_per_fb_perc = Field()
    ifh_perc = Field()
    buh_perc = Field()
    pitches = Field()
    balls = Field()
    strikes = Field()
