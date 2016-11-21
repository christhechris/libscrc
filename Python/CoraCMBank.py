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
        self.html = ''
        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)

    def loadurl(self):
        """Loading"""
        # url = 'http://fx.cmbchina.com/hq/'
        url = 'http://english.cmbchina.com/Rate/ForexRates.aspx'
        try:
            response = urllib.request.urlopen(url)
            self.html = response.read().decode('UTF-8')
        except BaseException:
            return False
        return True

    def lastrates(self, currency):
        """Latest FX exchange rates"""
        currencypos = self.html.find(currency)
        lbpos = self.html.find(r'Renminbi', currencypos)
        rbpos = self.html.find(r'</tr>', lbpos + 1)
        if lbpos > 0 and rbpos > 0:
            newstr = self.html[lbpos:rbpos]
            ret = re.findall(r'[0-9\.:]+', newstr)
            if ret and len(ret) == 5:
                # if ret[1] > '507.72':
                #     print('OK')
                print(ret[4] + ' ' + currency.ljust(20) +
                      ' -> (SO) = ' + ret[1] + ' (SI) = ' + ret[2])

if __name__ == '__main__':

    CORACMB = CoraCMB(debugLevel=logging.INFO)
    while True:
        if CORACMB.loadurl():
            # CURRENCYLIST = ['Australian Dollar', 'U.S. Dollar']
            CURRENCYLIST = ['Australian Dollar']
            for index in CURRENCYLIST:
                CORACMB.lastrates(index)
            # print('*' * 60)
            time.sleep(30)

