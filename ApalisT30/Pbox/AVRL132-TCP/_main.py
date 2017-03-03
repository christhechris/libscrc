# -*- coding:utf-8 -*-
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
from PboxRL132TCP import PboxRL132

def thread_realtime(addr):
    """Listion Port=49153 and receive RT data."""
    rtdata = PboxRL132(addr, 49153)
    while True:
        print('thread_realtime', rtdata.recv())


def main():
    """Main Function Entry."""

    addr = '192.168.5.100'

    thd = threading.Thread(target=thread_realtime, args=(addr, ))
    thd.start()


    rl132 = PboxRL132('192.168.5.102', 49153)
    while True:
        rl132.send()
        time.sleep(5)

if __name__ == '__main__':
    main()
