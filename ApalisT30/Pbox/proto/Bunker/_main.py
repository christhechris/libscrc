# -*- coding:UTF-8 -*-
""" Main"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux
# Author:   Heyn
# Program:
# History:  2017/03/24 V1.0.0[Heyn]

import sys
import json
import time
import random
from datetime import datetime

import threading

from PboxHttp import PboxHttp
from PboxBunker import PboxBunker

def thread_http(phttp, pjson):
    """Http thread."""

    ret = phttp.insert(pjson)
    print(time.strftime("%H:%M:%S", time.localtime()), '[Bunker]ret = %d'%ret)


def main(key=0):
    """Main Function Entry."""

    phttp = PboxHttp(ip='47.93.79.77')
    bunker = PboxBunker('192.168.5.5', 2222)
    print(phttp.create(bunker.getitems()))

    while True:
        stime = datetime.utcnow()
        datajson = bunker.getdata().get('items')
        etime = datetime.utcnow()
        thd = threading.Thread(target=thread_http, args=(phttp, datajson, ))
        thd.start()
        try:
            time.sleep(5 - (etime-stime).seconds - (etime-stime).microseconds/1000000)
        except BaseException:
            pass

if __name__ == '__main__':
    # main(int(sys.argv[1]))
    main()
