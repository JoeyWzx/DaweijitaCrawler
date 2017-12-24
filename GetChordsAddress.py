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


def crawlAll(pageUrl):
    for i in range(1, 8):
        pageInfo = requests.get(pageUrl + '/page/' + str(i)).text
        tree = html.fromstring(pageInfo)
        allLinksInOnePage = tree.xpath('//*[@class="widget-content"][1]/ul/li/h2/a/@href')

        for singlePage in allLinksInOnePage:
            saveChords(singlePage)


def saveChords(singleUrl):
    title, imageInfo = resolvePage(singleUrl)
    filePath = BASE_FOLDER + title.replace('/', '_')
    mkdir(filePath)

    for info in imageInfo:
        saveImage(filePath, info)


def resolvePage(singleUrl):
    pageInfo = requests.get(singleUrl).text
    tree = html.fromstring(pageInfo)
    imageInfo = tree.xpath('//*[@class="highslide-image"]/@href')
    title = tree.xpath('//h1[@class="post-title"]/text()')[0]
    return title, imageInfo


def saveImage(path, imageUrl):
    data = getImageData(imageUrl)

    if data is not None:
        imageName = imageUrl.split('/')[-1]
        f = open(path + '/' + imageName, 'wb')
        f.write(data)
        f.close()


def getImageData(imageUrl):
    print('try to get image of: \'' + imageUrl + '\'')
    try:
        quote = parse.quote(imageUrl, safe='/:?=')
        return request.urlopen(quote).read()
    except error.HTTPError:
        print('get from \'' + imageUrl + '\' failed')
        return None


def mkdir(path):
    exists = os.path.exists(path)
    if not exists:
        print('create folder', path)
        os.mkdir(path)


if __name__ == '__main__':
    # saveChords('http://www.daweijita.com/78177.html')
    print(crawlAll('http://www.daweijita.com/video_lesson'))
    # saveImage('/Users/joeywang/Downloads/chords/【￥49】《大伟流行弹唱精选吉他谱集》',
    #           'http://cdn.daweijita.com/2016/12/5周年书籍宝贝页面_03.gif')
