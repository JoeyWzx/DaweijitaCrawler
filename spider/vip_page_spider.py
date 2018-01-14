#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'Zexu Wang'

import itertools

import requests
from lxml import html

from util.utils import get_image_data, mkdir

VIP_FOLDER = '/Users/joeywang/Downloads/scores/vip/'
MAIN_PAGE = 'http://www.daweijita.com/vip'


def crawl(keyword='*'):
    last_page_url = \
        html.fromstring(requests.get(MAIN_PAGE).text).xpath('//*[@class="page-nav"]/a[@class="page"]/@href')[-1]
    total_page = last_page_url.split('/')[-1]
    print('total page of vip: ', total_page)

    for i in range(1, int(total_page) + 1):
        page_info = requests.get(MAIN_PAGE + '/page/' + str(i)).text
        tree = html.fromstring(page_info)
        all_links_in_one_page = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/@href')
        titles = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/text()')

        for singlePage, title, j in zip(all_links_in_one_page, titles, range(1, len(all_links_in_one_page) + 1)):
            if keyword == '*' or keyword.upper() in title.upper():
                print()
                print('------------ ', title, '------------')
                print('------------ index ', j, ' of vip page ', i, '------------')
                save_scores(singlePage, title)


def save_scores(single_url, title):
    vip_link = get_possible_vip_link(single_url)

    for image_index in range(1, 20):
        full_link = vip_link.split('.gif')[0] + '_' + str(image_index) + '.gif'
        data = get_image_data(full_link)

        if data is not None:
            file_path = VIP_FOLDER + title.replace('/', '_')
            mkdir(file_path)
            image_name = full_link.split('/')[-1]

            f = open(file_path + '/' + image_name, 'wb')
            f.write(data)
            f.close()
        else:
            if image_index == 1:
                correct_link = loop_date_to_get_link(full_link, title)
                if correct_link is not None:
                    vip_link = correct_link[:-6] + ".gif"
            else:
                break


def loop_date_to_get_link(full_link, title):
    for i, j in itertools.product(range(2010, 2018), range(1, 13)):
        slices = full_link.split('/')
        full_link = '/'.join((slices[0], slices[1], slices[2], str(i), str('%02d' % j), slices[-1]))
        print('looping', end=' ... ')
        data = get_image_data(full_link)

        if data is not None:
            file_path = VIP_FOLDER + title.replace('/', '_')
            mkdir(file_path)
            image_name = full_link.split('/')[-1]

            f = open(file_path + '/' + image_name, 'wb')
            f.write(data)
            f.close()

            return full_link


def get_possible_vip_link(single_url):
    page_info = requests.get(single_url).text
    tree = html.fromstring(page_info)
    possible_link = tree.xpath('//*[@class="highslide-image"]/img/@data-original')[-1]

    return possible_link.replace('fufei', 'tab', 1).split('_guita')[0]
