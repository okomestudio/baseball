#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import psycopg2
from scrapy.exceptions import DropItem

from fangraphs import items


def _create_batting_split_table(conn):
    sql = (
        "CREATE TABLE IF NOT EXISTS batting_split ("
        "  playerid INT NOT NULL,"
        "  season SMALLINT NOT NULL,"
        "  split TEXT NOT NULL,"
        "  g SMALLINT,"
        "  ab SMALLINT,"
        "  pa SMALLINT,"
        "  h SMALLINT,"
        "  h1 SMALLINT,"
        "  h2 SMALLINT,"
        "  h3 SMALLINT,"
        "  hr SMALLINT,"
        "  r SMALLINT,"
        "  rbi SMALLINT,"
        "  bb SMALLINT,"
        "  ibb SMALLINT,"
        "  so SMALLINT,"
        "  hbp SMALLINT,"
        "  sf SMALLINT,"
        "  sh SMALLINT,"
        "  gdp SMALLINT,"
        "  sb SMALLINT,"
        "  cs SMALLINT,"
        "  avg NUMERIC,"
        "  bb_perc NUMERIC,"
        "  k_perc NUMERIC,"
        "  bb_per_k NUMERIC,"
        "  obp NUMERIC,"
        "  slg NUMERIC,"
        "  ops NUMERIC,"
        "  iso NUMERIC,"
        "  babip NUMERIC,"
        "  wrc NUMERIC,"
        "  wraa NUMERIC,"
        "  woba NUMERIC,"
        "  wrcp NUMERIC,"
        "  gb_per_fb NUMERIC,"
        "  ld_perc NUMERIC,"
        "  gb_perc NUMERIC,"
        "  fb_perc NUMERIC,"
        "  iffb_perc NUMERIC,"
        "  hr_per_fb_perc NUMERIC,"
        "  ifh_perc NUMERIC,"
        "  buh_perc NUMERIC,"
        "  pitches SMALLINT,"
        "  balls SMALLINT,"
        "  strikes SMALLINT,"
        "  PRIMARY KEY (playerid, season, split)"
        ");"
    )
    conn.cursor().execute(sql)
    conn.commit()


def _create_pitching_split_table(conn):
    sql = (
        "CREATE TABLE IF NOT EXISTS pitching_split ("
        "  playerid INT NOT NULL,"
        "  season SMALLINT NOT NULL,"
        "  split TEXT NOT NULL,"
        "  ip_out SMALLINT,"
        "  era NUMERIC,"
        "  tbf SMALLINT,"
        "  h SMALLINT,"
        "  h2 SMALLINT,"
        "  h3 SMALLINT,"
        "  r SMALLINT,"
        "  er SMALLINT,"
        "  hr SMALLINT,"
        "  bb SMALLINT,"
        "  ibb SMALLINT,"
        "  hbp SMALLINT,"
        "  so SMALLINT,"
        "  avg NUMERIC,"
        "  obp NUMERIC,"
        "  slg NUMERIC,"
        "  woba NUMERIC,"
        "  k_per_9 NUMERIC,"
        "  bb_per_9 NUMERIC,"
        "  k_per_bb NUMERIC,"
        "  hr_per_9 NUMERIC,"
        "  k_perc NUMERIC,"
        "  bb_perc NUMERIC,"
        "  k_minus_bb_perc NUMERIC,"
        "  whip NUMERIC,"
        "  babip NUMERIC,"
        "  lob_perc NUMERIC,"
        "  fip NUMERIC,"
        "  xfip NUMERIC,"
        "  gb_per_fb NUMERIC,"
        "  ld_perc NUMERIC,"
        "  gb_perc NUMERIC,"
        "  fb_perc NUMERIC,"
        "  iffb_perc NUMERIC,"
        "  hr_per_fb_perc NUMERIC,"
        "  ifh_perc NUMERIC,"
        "  buh_perc NUMERIC,"
        "  pitches SMALLINT,"
        "  balls SMALLINT,"
        "  strikes SMALLINT,"
        "  PRIMARY KEY (playerid, season, split)"
        ");"
    )
    conn.cursor().execute(sql)
    conn.commit()


class FangraphsPipeline(object):

    def open_spider(self, spider):
        self._conn = psycopg2.connect('dbname=fangraphs')
        _create_batting_split_table(self._conn)
        _create_pitching_split_table(self._conn)

    def close_spider(self, spider):
        self._conn.close()

    def process_item(self, item, spider):
        if isinstance(item, items.PitchingSplitItem):
            tablename = 'pitching_split'
        elif isinstance(item, items.BattingSplitItem):
            tablename = 'batting_split'
        else:
            raise DropItem('dropping unknown item')
        d = dict(item)
        keys = d.keys()
        sql = (
            "INSERT INTO {tablename} ("+ ", ".join(keys) +")"
            "  SELECT %("+ ")s, %(".join(keys) +")s"
            "  WHERE NOT EXISTS ("
            "    SELECT 1 FROM {tablename}"
            "      WHERE playerid = %(playerid)s"
            "            AND season = %(season)s"
            "            AND split = %(split)s"
            "  );"
        ).format(tablename=tablename)
        cur = self._conn.cursor()
        try:
            cur.execute(sql, d)
        except:
            self._conn.rollback()
            raise
        else:
            self._conn.commit()
        return item
