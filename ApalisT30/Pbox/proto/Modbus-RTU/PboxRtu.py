# -*- coding:UTF-8 -*-
""" Pbox Modbus RTU"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Modbus RTU
# History:  2017/02/14 V1.0.0[Heyn]
#           2017/03/08 V1.0.1[Heyn] Send return string.

import pymodbus
import imx6_ixora_led as led


class PboxRtu:
    """Pbox Modbus Class"""

    def __init__(self, ttypath='/dev/ttymxc1'):
        super(PboxRtu, self).__init__()
        pymodbus.new_rtu(ttypath)
        # set_timeout(seconds, microseconds = us)
        pymodbus.set_timeout(0, 500000)

    def __del__(self):
        led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
        led.ioctl(led.IXORA_LED4, led.RED, led.LOW)
        pymodbus.free_rtu()

    def send(self, readlist, length=1):
        """Send Data to Device."""
        try:
            ret = pymodbus.read_registers(readlist[0:3], length)
        except BaseException as err:
            led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
            led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)
            print(err)
            return None
        else:
            led.ioctl(led.IXORA_LED4, led.RED, led.LOW)
            led.ioctl(led.IXORA_LED4, led.GREEN, led.HIGH)
        finally:
            pass
        # When the length is greater than 1, it is a string.
        # And each hexadecimal number into ASCII code
        return ret[0] if length == 1 else ''.join((lambda val: [chr(i) for i in val])(ret)).strip('\x00')
