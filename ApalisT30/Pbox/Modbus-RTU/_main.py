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
from datetime import datetime

import sysv_ipc
import threading


from PboxRtu import PboxRtu
from PboxHttp import PboxHttp

def thread_http(phttp, pjson):
    """Http thread."""
    ret = phttp.insert(pjson)
    print(time.strftime("%H:%M:%S", time.localtime()), '[modbus rtu]ret = %d'%ret)


def main(key=0):
    """Main Function Entry."""
    # print('key = %d'%key)
    memory = sysv_ipc.SharedMemory(key)
    msgdict = json.loads(bytes.decode(memory.read()).strip('\0'))

    pmodbus = PboxRtu()
    phttp = PboxHttp(ip=msgdict['Pbox']['CloudInfo'], table_name=msgdict['table_name'])
    phttp.create(msgdict)

    datadict = {}
    datajson = []
    while True:
        stime = datetime.utcnow()
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
        etime = datetime.utcnow()

        try:
            time.sleep(1 - (etime-stime).seconds - (etime-stime).microseconds/1000000)
        except BaseException:
            pass

if __name__ == '__main__':
    main(int(sys.argv[1]))
