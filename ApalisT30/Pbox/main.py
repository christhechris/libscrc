# -*- coding:utf-8 -*-
""" Main"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux
# Author:   Heyn
# Program:
# History:  2017/02/17 V1.0.0[Heyn]

import os
import sys
import time
import mmap
import json
import random
import subprocess

from glob import glob
from PboxXML import PboxXML
import sysv_ipc
import imx6_ixora_led as led

def main():
    """Main Function Entry."""
    process = []
    xml = PboxXML()
    xmllist = xml.get_config()
    key = random.randint(1000, 9999)
    for root, dirs, files in os.walk('./'):  # pylint: disable=W0612
        for match in glob(os.path.join(root, '_main.py')):
            for config in xmllist:
                if config['devicedriver'] in match:
                    msg = bytes(json.dumps(config), encoding="utf8")
                    key = key + 1
                    memory = sysv_ipc.SharedMemory(key, flags=sysv_ipc.IPC_CREAT, size=len(msg))
                    memory.write(msg)
                    # print(os.system('python ' + match + ' &'))
                    proc = subprocess.Popen(['python', match, str(key)])
                    process.append(proc)
                    print('process id = %d'%proc.pid)

    while True:
        #os.system('ps -ef|grep python3|grep -v grep')
        try:
            time.sleep(10)
            print('I am master!!!')
        except KeyboardInterrupt:
            led.clear()
            for proc in process:
                proc.kill()
            sys.exit()

if __name__ == '__main__':
    main()

