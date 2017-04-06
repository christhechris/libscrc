# -*- coding:UTF-8 -*-
""" Pbox Modbus TCP"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Modbus TCP
# History:  2017/02/14 V1.0.0[Heyn]
#           2017/03/08 V1.0.1[Heyn] Send return string.

import pymodbus
import imx6_ixora_led as led


class PboxTCP:
    """Pbox Modbus Class"""

    def __init__(self, ip='127.0.0.1', port=502):
        super(PboxTCP, self).__init__()
        self.isopened = False
        print('[Modbus TCP] %s -- %d' % (ip, port))
        try:
            pymodbus.new_tcp(ip, port)
            # set_timeout(seconds, microseconds = us)
            pymodbus.set_timeout(0, 3000000)  # default timeout=3s
            self.isopened = True
        except BaseException as err:
            led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)
            print(err)

    def __del__(self):
        self.isopened = False
        led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
        led.ioctl(led.IXORA_LED4, led.RED, led.LOW)
        pymodbus.free_tcp()

    def close(self):
        """Close Socket."""
        self.isopened = False
        pymodbus.free_tcp()

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
