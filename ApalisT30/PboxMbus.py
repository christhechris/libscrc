# -*- coding:utf8 -*-
""" Pbox Modbus """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Modbus.
# History:  2017/02/14 V1.0.0[Heyn]

import pymodbus
from ImxLED import ImxLED

class PboxMbus:
    """Pbox Modbus Class"""

    def __init__(self, ttypath='/dev/ttymxc1'):
        super(PboxMbus, self).__init__()
        pymodbus.new_rtu(ttypath)

    def send(self, led, readlist, length=1):
        """Send Data to Device."""
        msg = 'Code = ' + str(readlist[0]) + ' Addr = %4d' % (readlist[1]) + '  =>  '
        try:
            ret = pymodbus.read_registers(readlist[0:3], length)
            msg += str(ret)
            led.normal()
        except BaseException as err:
            led.error()
            print(err)
            return -1

        return ret[0]
