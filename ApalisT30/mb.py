# -*- coding:utf8 -*-
""" FP7 """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:
# History:  2017/01/18 V1.0.0[Heyn]

import sys
import time
import random
import threading

from PboxXML import PboxXML
from PboxHttp import PboxHttp
from PboxMbus import PboxMbus

from ImxLED import ImxLED


def thread_http(phttp, pjson):
    """Http thread."""
    # ret = -1
    # while ret == -1:
    #     ret = phttp.insert(pjson)
    # print(ret)
    print('Http Server = %d  >> '%phttp.insert(pjson) + time.strftime("%H:%M:%S", time.localtime()))

def main():
    """Main funciotn."""
    led1 = ImxLED('LED1')
    led1.start()

    xml = PboxXML()
    phttp = PboxHttp(xml.device_name())
    ret = phttp.create(xml.items_info())
    if ret == -1:
        print('Connect http server faild.')
        sys.exit()

    pmodbus = PboxMbus()
    cmds = xml.dataitem()
    print(cmds)

    # CMDS = [[3, 1, 'D32', 'TEST1'],
    #         [3, 10, 'U16', 'TEST2'],
    #         [3, 12, 'S16', 'TEST3'],
    #         [3, 20, 'F16', 'TEST4'],
    #         [1, 1, 'B08', 'TEST5'],
    #         [1, 1, 'B08', 'TEST6'],
    #         [4, 0, 'U32', 'TEST7'],
    #         [4, 0x07D0, 'S32', 'TEST8']]

    datadict = {}
    datajson = []

    while True:
        datajson.clear()
        for cmd in cmds:
            datadict['itemName'] = cmd[3]
            #datadict['value'] = pmodbus.send(led1, cmd, 1)
            print(str(pmodbus.send(led1, cmd, 1)) + ' - ', end='')
            datadict['value'] = random.randint(0, 999)
            datajson.append(datadict.copy())
        print('')
        thd = threading.Thread(target=thread_http, args=(phttp, datajson, ))
        thd.start()
        time.sleep(5)


if __name__ == '__main__':
    main()
