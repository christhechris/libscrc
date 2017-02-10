# -*- coding:utf8 -*-
""" FP7 """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:
# History:  2017/01/18 V1.0.0[Heyn]

import json
import urllib
import urllib.request
import requests

import time
import pymodbus

from ImxLED import ImxLED
from PbXML import PbXML

URL = 'http://192.168.5.100:8080'

def caller(led, readlist, length=1):
    """Modbus"""
    msg = 'Code = ' + str(readlist[0]) + ' Addr = %4d' % (readlist[1]) + '  =>  '

    try:
        msg += str(pymodbus.read_registers(readlist, length))
        led.normal()
        print(msg)
    except BaseException as err:
        led.error()
        print(err)
        return msg + str(err) + '\r\n'

    return msg + '\r\n'

if __name__ == '__main__':
    LED1 = ImxLED('LED1')
    LED1.start()
    XML = PbXML()
    print(pymodbus.new_rtu('/dev/ttymxc1'))

    SERVERS = requests.session()
    DICTS = {'FP7-MODBUS-RTU': '0'}

    #CMDS = [[3, 1, 'D32'], [3, 10, 'U16'], [3, 12, 'S16'], [3, 20, 'F16'], [
    #    1, 1, 'B08'], [1, 1, 'B08'], [4, 0, 'U32'], [4, 0x07D0, 'S32']]
    CMDS = XML.dataitem()
    while True:
        JSON_DATA = ''
        for cmd in CMDS:
            JSON_DATA += caller(LED1, cmd, 2)
        #DICTS['FP7-MODBUS-RTU'] = data
        #r = SERVERS.post(URL, data = json.dumps(DICTS))
        time.sleep(2)
