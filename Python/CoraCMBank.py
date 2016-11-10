# -*- coding:utf8 -*-
""" China Merchants Bank """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  China Merchants Bank.
# History:  2016/11/10 V1.0.0[Heyn]

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]


import os
import re
import time
import logging

import urllib
import urllib.request
import urllib.parse

class CoraCMB:
    """China Merchants Bank."""

    def __init__(self, debugLevel=logging.WARNING):
        super(CoraCMB, self).__init__()

        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)

    def loadurl(self):
        """Loading"""
        url = 'http://fx.cmbchina.com/hq/'
        response = urllib.request.urlopen(url)
        html = response.read().decode('UTF-8')

        start_index = html.find(r'澳大利亚元')
        stop_index = html.find(r'澳大利亚元', start_index + 1)
        newstr = html[start_index:stop_index]
        regx = r'[0-9\.:]+'
        ret = re.findall(regx, newstr)
        print(ret[6] + ' AUD -> (SO) = ' + ret[2] + ' (SI) = ' + ret[4])

        start_index = html.find(r'美元')
        stop_index = html.find(r'美元', start_index + 1)
        newstr = html[start_index:stop_index]
        regx = r'[0-9\.:]+'
        ret = re.findall(regx, newstr)
        print(ret[6] + ' USD -> (SO) = ' + ret[2] + ' (SI) = ' + ret[4])
        print('*'*40)

        # print(ret)


if __name__ == '__main__':

    while True:
        CORACMB = CoraCMB(debugLevel=logging.INFO)
        CORACMB.loadurl()
        time.sleep(30)
