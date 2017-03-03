# -*- coding:utf8 -*-
""" Main"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux
# Author:   Heyn
# Program:
# History:  2017/02/17 V1.0.0[Heyn]

import sys
import json
import time
import random
import sysv_ipc
import threading

from PboxTCP import PboxTCP
from PboxHttp import PboxHttp

def thread_http(phttp, pjson):
    """Http thread."""
    ret = phttp.insert(pjson)
    print(time.strftime("%H:%M:%S", time.localtime()), '[http <modbus tcp>]ret = %d'%ret)


def main(key=0):
    """Main Function Entry."""
    # print('key = %d'%key)
    memory = sysv_ipc.SharedMemory(key)
    msgdict = json.loads(bytes.decode(memory.read()).strip('\0'))

    pmodbus = PboxTCP(msgdict['config'].split(';')[1])
    while True:
        if pmodbus.isopened is True:
            break
        else:
            time.sleep(10)

    phttp = PboxHttp(ip=msgdict['Pbox']['CloudInfo'], table_name=msgdict['table_name'])
    phttp.create(msgdict)

    datadict = {}
    datajson = []
    while True:
        datajson.clear()
        for cmd in msgdict['Items']:
            datadict['itemName'] = cmd['itemName']
            datadict['value'] = pmodbus.send(cmd['itemValue'], 1)
            if datadict['value'] is None:
                break
            datadict['value'] = random.randint(0, 900)
            datajson.append(datadict.copy())

        if len(datajson):
            thd = threading.Thread(target=thread_http, args=(phttp, datajson, ))
            thd.start()
        time.sleep(1)

if __name__ == '__main__':
    main(int(sys.argv[1]))
