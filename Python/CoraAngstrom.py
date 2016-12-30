# -*- coding:utf8 -*-
""" Cora Angstrom."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  CoraAngstrom.
# History:  2016/12/29


import os
import re
import urllib
import urllib.request
import urllib.parse

BASE_URL = 'http://feeds.angstrom-distribution.org/'
BASE_DIR = 'D://feeds.angstrom-distribution.org//'


class CoraAngstrom:
    """Download files(*.ipk) from http://feeds.angstrom-distribution.org/"""

    def __init__(self):
        self.base_url = BASE_URL

    def __get_html(self, url):
        """Get html from {url}"""
        response = urllib.request.urlopen(url)
        return response.read().decode('UTF-8')

    def get_tags(self, url):
        """"Get other links"""

        # <html>
        # <head><title>Index of /</title></head>
        # <body bgcolor="white">
        # <h1>Index of /</h1><hr><pre><a href="../">../</a>
        # <a href="feeds/">feeds/</a>                            17-Nov-2016 08:12  -
        # <a href="nightlies/">nightlies/</a>                    17-Dec-2014 06:30  -
        # </pre><hr></body>
        # </html>

        html = self.__get_html(url)
        re_tags = '<a href=\\"(.+?)\\">(.+?)</a>\\W.*?(\\d{2}-[A-Za-z]{3}-\\d{4}\\W\\d{2}:\\d{2})\\W+?(.+?)'
        pattern = re.compile(re_tags)
        ret = pattern.findall(html)
        url_list = []
        for index in range(0, len(ret)):
            url_list.append(BASE_URL + ret[index][1])
            # print(BASE_URL + ret[index][1])
        return url_list

    def get_ipk(self, url, name):
        """Download *.IPK from {url}"""
        save_path = BASE_DIR + name
        # os.path.exists('d:/assist')
        # os.path.isfile('d:/assist/getTeacherList.py')
        # os.makedirs('d:/assist/set')
        # os.path.exists('d:/assist/set')
        urllib.request.urlretrieve(url, save_path)


if __name__ == '__main__':
    URLS = CoraAngstrom()
    # HTMLS = URLS.get_html(BASE_URL)
    # print(URLS.get_tags(HTMLS))
    turls = []
    turls = URLS.get_html(BASE_URL)
    for i in range(0, 1):
        # for url in URLS.get_tags(HTMLS):
        turls = URLS.get_html(turls)
        print(turls)

    # URL = 'http://feeds.angstrom-distribution.org/feeds/v2016.06/ipk/glibc/armv7at2hf-neon/base/'
    # RESPONSE = urllib.request.urlopen(URL)
    # HTML = RESPONSE.read().decode('UTF-8')
    # DOWNLOAD_URL = 'http://feeds.angstrom-distribution.org/feeds/v2016.06/ipk/glibc/armv7at2hf-neon/base/a52dec-doc_0.7.4-r4_armv7at2hf-neon-vfpv4.ipk'
    # urllib.request.urlretrieve(DOWNLOAD_URL, 'd://a52dec-doc_0.7.4-r4_armv7at2hf-neon-vfpv4.ipk')
