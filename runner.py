#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'Zexu Wang'

from spider.normal_page_spider import crawl as normal_crawl
from spider.vip_page_spider import crawl as vip_crawl


def crawl(keyword='*'):
    normal_crawl(keyword)
    vip_crawl(keyword)


if __name__ == '__main__':
    crawl()
