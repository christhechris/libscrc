# -*- coding:utf8 -*-
""" China Merchants Bank """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  China Merchants Bank.
# History:  2016/11/10 V1.0.0[Heyn]
#           2017/10/10 V1.0.1[Heyn] Add itchat

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]


import re
import time

import urllib
import urllib.request
import urllib.parse

import itchat


class CoraCMB:
    """China Merchants Bank."""

    def __init__(self):
        super(CoraCMB, self).__init__()
        self._items = []
        self._html = self._message = ''

    def _loadurl(self):
        """Loading"""
        url = 'http://english.cmbchina.com/Rate/ForexRates.aspx'
        try:
            response = urllib.request.urlopen(url)
            self._html = response.read().decode('UTF-8')
        except BaseException:
            return False
        return True

    def lastrates(self, currency=['Australian Dollar', 'U.S. Dollar']):
        """Latest FX exchange rates"""
        if self._loadurl() is False:
            return ''
        self._message = ''
        itmegroup = re.findall(r'<tr.*?>(.*?)</tr>', self._html, re.S|re.M)
        for items in itmegroup:
            self._items = [i.replace('\r\n', '').strip(' ') for i in re.findall(r'<td.*?>(.*?)</td>', items, re.S|re.M)]
            if self._items[0] in currency:
                self._message += '{0} (SO)={1} (SI)={2} '.format(self._items[0], self._items[4], self._items[5])

        print(self._message)
        return self._message



def main():
    cmb = CoraCMB()
    itchat.auto_login(enableCmdQR=2, hotReload=True)

    while True:
        hours = time.localtime(time.time()).tm_hour
        if hours > 21 or hours < 9:
            time.sleep(60*10)
            continue

        itchat.send(cmb.lastrates(), toUserName='filehelper')
        time.sleep(60*10)

if __name__ == '__main__':
    main()
