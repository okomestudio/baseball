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
        "  avg REAL,"
        "  PRIMARY KEY (playerid, season, split)"
        ");"
    )
    conn.cursor().execute(sql)
    conn.commit()


class FangraphsPipeline(object):

    def open_spider(self, spider):
        self._conn = psycopg2.connect('dbname=fangraphs')
        _create_batting_split_table(self._conn)

    def close_spider(self, spider):
        self._conn.close()

    def process_item(self, item, spider):
        if isinstance(item, items.PitchingSplitItem):
            raise DropItem('dropping pitching item')

        spider.log(str(dict(item)))
        
        sql = (
            "INSERT INTO batting_split"
            " (playerid, season, split, avg) VALUES"
            " (%(playerid)s, %(season)s, %(split)s, %(avg)s);"
        )
        cur = self._conn.cursor()
        try:
            cur.execute(sql, dict(item))
        except:
            self._conn.rollback()
            raise
        else:
            self._conn.commit()
        return None
