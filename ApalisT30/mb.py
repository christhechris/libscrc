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
import pymodbus

from PboxHttp import PboxHttp
from ImxLED import ImxLED
from PbXML import PbXML

def caller(led, readlist, length=1):
    """Modbus"""
    msg = 'Code = ' + str(readlist[0]) + ' Addr = %4d' % (readlist[1]) + '  =>  '
    ret = 0
    try:
        ret = pymodbus.read_registers(readlist[0:3], length)
        msg += str(ret)
        led.normal()
        print(msg)
    except BaseException as err:
        led.error()
        print(err)
        return ret

    return ret

if __name__ == '__main__':
    LED1 = ImxLED('LED1')
    LED1.start()

    XML = PbXML()
    HTTP = PboxHttp(XML.device_name())
    ret = HTTP.create(XML.items_info())
    if ret == -1:
        sys.exit()
    print(pymodbus.new_rtu('/dev/ttymxc1'))

    CMDS = XML.dataitem()
    print(CMDS)

    # CMDS = [[3, 1, 'D32', 'TEST1'],
    #         [3, 10, 'U16', 'TEST2'],
    #         [3, 12, 'S16', 'TEST3'],
    #         [3, 20, 'F16', 'TEST4'],
    #         [1, 1, 'B08', 'TEST5'],
    #         [1, 1, 'B08', 'TEST6'],
    #         [4, 0, 'U32', 'TEST7'],
    #         [4, 0x07D0, 'S32', 'TEST8']]

    DATADICT = {}
    JSON_DATA = []

    while True:
        JSON_DATA.clear()
        for cmd in CMDS:
            DATADICT['itemName'] = cmd[3]
            # DATADICT['value'] = caller(LED1, cmd, 1)[0]
            DATADICT['value'] = random.randint(-1000, 1000)
            JSON_DATA.append(DATADICT.copy())
        HTTP.insert(JSON_DATA)
        time.sleep(5)
