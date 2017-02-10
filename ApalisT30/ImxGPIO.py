# -*- coding:utf8 -*-
""" Apalis T30 GPIO."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: i.mx6 ARMv7
# Author:   Heyn
# Program:  ImxGPIO.
# History:  2017/02/09

import time
import os.path

class ImxGPIO:
    """Apalis T30 GPIO Class."""

    def __init__(self, port='2', path='/sys/class/gpio'):
        super(ImxGPIO, self).__init__()
        self.path = path
        export_file = open(path + '/export', 'w')
        unexport_file = open(path + '/unexport', 'w')

        export_exists = os.path.isdir(path+'/gpio' + port)
        if export_exists and False:
            unexport_file.write(port)
            unexport_file.flush()

        if not export_exists or False:
            export_file.write(port)
            export_file.flush()

        directionfile = open(path + '/gpio' + port + '/direction', 'w')
        directionfile.write("out")
        directionfile.flush()

        self.value = open(path + '/gpio' + port + '/value', 'w')

    def __del__(self):
        self.low()

    def high(self):
        """ GPIO out high"""
        self.value.write("1")
        self.value.flush()

    def low(self):
        """ GPIO out low"""
        self.value.write("0")
        self.value.flush()

if __name__ == "__main__":
    GPIO = ImxGPIO('2')
    GPIO6 = ImxGPIO('6')
    while True:
        GPIO.high()
        GPIO6.high()
        time.sleep(500/1000.0)
        GPIO.low()
        GPIO6.low()
        time.sleep(500/1000.0)

