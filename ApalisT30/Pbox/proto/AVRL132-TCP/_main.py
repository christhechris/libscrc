# -*- coding:UTF-8 -*-
"""
NM-EJA5A NM-EJA6A AV132
NM-EJR5A NM-EJR6A RL132
"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:
# History:  2017/03/03 V1.0.0[Heyn]

import json
import sys
import threading
import time
from datetime import datetime

import sysv_ipc
from PboxHttp import PboxHttp
from PboxRL132TCP import PboxRL132

def thread_http(phttp, pjson):
    """Http thread."""
    ret = phttp.insert(pjson)

    print(time.strftime("%H:%M:%S", time.localtime()), '[http <modbus tcp>]ret = %d'%ret)
    # print(pjson)

def thread_realtime(addr):
    """Listion Port=49153 and receive RT data."""
    rtdata = PboxRL132()
    while True:
        if rtdata.open(addr, 49153) is True:
            break
        else:
            time.sleep(1)

    while True:
        print('thread_realtime', rtdata.recv())


def main(key=0):
    """Main Function Entry."""

    msgdict = {}
    memory = sysv_ipc.SharedMemory(key)
    msgdict = json.loads(bytes.decode(memory.read()).strip('\0'))


    addr = msgdict['config'].split(';')[1]

    phttp = PboxHttp(ip=msgdict.get('Pbox').get('CloudInfo'), table_name=msgdict.get('table_name'))
    print(phttp.create(msgdict))
    # print(addr)
    # thd = threading.Thread(target=thread_realtime, args=(addr, ))
    # thd.start()

    rl132 = PboxRL132()

    while True:
        if rl132.open(addr, 49153) is True:
            break
        else:
            time.sleep(1)

    while True:
        stime = datetime.utcnow()
        if rl132.isopened is False:
            time.sleep(1)
            rl132.open(addr, 49153)
            continue

        datajson = rl132.send('C1M000', msgdict.get('Items'))

        if len(datajson):
            thd = threading.Thread(target=thread_http, args=(phttp, datajson, ))
            thd.start()
        etime = datetime.utcnow()

        try:
            time.sleep(5 - (etime-stime).seconds - (etime-stime).microseconds/1000000)
        except BaseException:
            pass

if __name__ == '__main__':
    main(int(sys.argv[1]))
