#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from scrapy.contrib.spidermiddleware.httperror import HttpError


class ErrorPageMiddleware(object):

    def process_spider_input(self, response, spider):
        if 'generalerror.aspx' in response.url:
            raise HttpError(response, 'Ignoring general error page')
