#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'Zexu Wang'

from urllib import error
from urllib import request
from urllib import parse
import requests
from lxml import html
import os

BASE_FOLDER = '/Users/joeywang/Downloads/chords/'


def crawlAll(pageUrl, keyword='*'):
    lastPageUrl = html.fromstring(requests.get(pageUrl).text).xpath('//*[@class="page-nav"]/a[@class="last"]/@href')[0]
    totalPage = lastPageUrl.split('/')[-1]
    print('total page: ', totalPage)

    for i in range(1, int(totalPage) + 1):
        pageInfo = requests.get(pageUrl + '/page/' + str(i)).text
        tree = html.fromstring(pageInfo)
        allLinksInOnePage = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/@href')
        titles = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/text()')

        for singlePage, title, j in zip(allLinksInOnePage, titles, range(1, len(allLinksInOnePage) + 1)):
            if keyword == '*' or keyword.upper() in title.upper():
                print('------------ ', title, '------------')
                print('------------ index ', j, ' in page ', i, '------------')
                saveScores(singlePage, title)


def saveScores(singleUrl, title):
    allScoreLinksOfOneSong = resolvePage(singleUrl)

    if not allScoreLinksOfOneSong:
        print('No scores in this song')

    for imageLink in allScoreLinksOfOneSong:
        data = getImageData(imageLink)

        if data is not None:
            filePath = BASE_FOLDER + title.replace('/', '_')
            mkdir(filePath)
            imageName = imageLink.split('/')[-1]

            f = open(filePath + '/' + imageName, 'wb')
            f.write(data)
            f.close()


def resolvePage(singleUrl):
    pageInfo = requests.get(singleUrl).text
    tree = html.fromstring(pageInfo)
    imageInfo = tree.xpath('//*[@class="highslide-image"]/@href')

    return imageInfo


def getImageData(imageUrl):
    print('image link: \'' + imageUrl + '\'')
    try:
        quote = parse.quote(imageUrl, safe='/:?=')
        return request.urlopen(quote).read()
    except error.HTTPError:
        print('get from \'' + imageUrl + '\' failed')
        return None


def mkdir(path):
    exists = os.path.exists(path)

    if not exists:
        os.mkdir(path)


if __name__ == '__main__':
    crawlAll('http://www.daweijita.com/video_lesson', 'hey hey')
