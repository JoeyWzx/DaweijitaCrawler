#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

__author__ = 'Zexu Wang'

import os
from urllib import error
from urllib import parse
from urllib import request


def get_image_data(image_url):
    print('image link: \'' + image_url + '\'', end=' --> ')
    try:
        quote = parse.quote(image_url.lower(), safe='/:?=')
        data = request.urlopen(quote).read()
        print('SUCCEED')
        return data
    except error.HTTPError:
        print('FAIL')
        return None


def mkdir(path):
    exists = os.path.exists(path)

    if not exists:
        os.mkdir(path)
