#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'Zexu Wang'

import requests
from lxml import html

from util.utils import get_image_data, mkdir

NORMAL_FOLDER = '/Users/joeywang/Downloads/scores/normal/'
MAIN_PAGE = 'http://www.daweijita.com/video_lesson'


def crawl(keyword='*'):
    last_page_url = \
        html.fromstring(requests.get(MAIN_PAGE).text).xpath('//*[@class="page-nav"]/a[@class="last"]/@href')[0]
    total_page = last_page_url.split('/')[-1]
    print('total page of normal: ', total_page)

    for i in range(1, int(total_page) + 1):
        page_info = requests.get(MAIN_PAGE + '/page/' + str(i)).text
        tree = html.fromstring(page_info)
        all_links_in_one_page = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/@href')
        titles = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/text()')

        for singlePage, title, j in zip(all_links_in_one_page, titles, range(1, len(all_links_in_one_page) + 1)):
            if keyword == '*' or keyword.upper() in title.upper():
                print()
                print('------------ ', title, '------------')
                print('------------ index ', j, ' of normal page ', i, '------------')
                save_scores(singlePage, title)


def save_scores(single_url, title):
    all_links_of_one_song = resolve_page(single_url)

    if not all_links_of_one_song:
        print('No scores in this song')

    for imageLink in all_links_of_one_song:
        data = get_image_data(imageLink)

        if data is not None:
            file_path = NORMAL_FOLDER + title.replace('/', '_')
            mkdir(file_path)
            image_name = imageLink.split('/')[-1]

            f = open(file_path + '/' + image_name, 'wb')
            f.write(data)
            f.close()


def resolve_page(single_url):
    page_info = requests.get(single_url).text
    tree = html.fromstring(page_info)
    image_info = tree.xpath('//*[@class="highslide-image"]/@href')

    return image_info
