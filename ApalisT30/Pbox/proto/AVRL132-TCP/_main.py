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

import time
import threading
from datetime import datetime
from PboxRL132TCP import PboxRL132

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


def main():
    """Main Function Entry."""

    addr = '192.168.5.100'

    # thd = threading.Thread(target=thread_realtime, args=(addr, ))
    # thd.start()

    rl132 = PboxRL132()

    while True:
        if rl132.open('192.168.5.104', 49153) is True:
            break
        else:
            time.sleep(1)

    while True:
        stime = datetime.utcnow()
        if rl132.isopened is False:
            time.sleep(1)
            rl132.open('192.168.5.104', 49153)
            continue
        rl132.send()
        etime = datetime.utcnow()

        try:
            time.sleep(5 - (etime-stime).seconds - (etime-stime).microseconds/1000000)
        except BaseException:
            pass

if __name__ == '__main__':
    main()
