#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import random


proxies = os.environ['PROXIES'].split(',') if 'PROXIES' in os.environ else []


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        if len(proxies):
            request.meta['proxy'] = ''.join(['http://',
                                             random.choice(proxies)])
