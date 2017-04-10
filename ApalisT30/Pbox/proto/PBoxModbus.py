# -*- coding:UTF-8 -*-
""" pyBox Modbus"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7
# Author:   Heyn
# Program:  Modbus RTU & TCP
# History:  2017/02/14 V1.0.0 [Heyn]
#           2017/03/08 V1.0.1 [Heyn] Send return string.
#           2017/04/07 V1.0.2 [Heyn] Redesign PBoxModbus class functions.
#           2017/04/10 V1.0.3 [Heyn] Bug fixe import imx6_ixora_led as led

# Windows(X86) Platform: You should have modbus.dll and pymodbus.pyd
# Linux or ARM Platform: You should have modbus.so  and pymodbus.cpython-35m-arm-linux-gnueabihf.so

import sys
import pymodbus

if sys.platform == 'linux':
    import imx6_ixora_led as led

class PBoxModbus:
    """Pbox Modbus Class"""

    def __init__(self):
        super(PBoxModbus, self).__init__()
        self.isopened = False
        self.platform = sys.platform

    def __del__(self):
        self.isopened = False
        pymodbus.free_tcp()
        if self.platform == 'linux':
            led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
            led.ioctl(led.IXORA_LED4, led.RED, led.LOW)

    def newtcp(self, addr='127.0.0.1', port=502):
        """New TCP for Modbus."""

        print('[Modbus TCP] IP=%s:%d'%(addr, port))
        try:
            self.isopened = pymodbus.new_tcp(addr, port)
        except BaseException as err:
            self.isopened = False
            print(err)

        if (self.platform == 'linux') and (self.isopened is False):
            led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)

        return self.isopened

    def newrtu(self, dev='/dev/ttymxc1'):
        """New RTU for Modbus."""

        print('[Modbus RTU] Port=%s'%(dev))
        try:
            self.isopened = pymodbus.new_rtu(dev)
        except BaseException as err:
            self.isopened = False
            print(err)

        if (self.platform == 'linux') and (self.isopened is False):
            led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)

        return self.isopened

    def settimeout(self, sec=0, msc=500):
        """
            sec: second.
            msc: millisecond seconds.
        """
        # set_timeout(seconds, microseconds = us)
        pymodbus.set_timeout(sec, msc)  # default timeout=500ms

    def setslave(self, addr=1):
        """Set modbus slave address."""
        if self.isopened is False:
            return None

        ret = False
        try:
            ret = pymodbus.set_slave(addr)
        except BaseException as err:
            print(err)
        return ret

    def readstring(self, readlist, size=1):
        """
            Read String from Device.
            readlist = [function code, address, data type]
        """
        if self.isopened is False:
            return None

        try:
            ret = pymodbus.read_registers(readlist[0:3], size)
        except BaseException as err:
            if self.platform == 'linux':
                led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
                led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)
            print(err)
            return None
        else:
            if self.platform == 'linux':
                led.ioctl(led.IXORA_LED4, led.RED, led.LOW)
                led.ioctl(led.IXORA_LED4, led.GREEN, led.HIGH)
            else:
                pass

        # And each hexadecimal number into ASCII code
        return ''.join((lambda v: [chr(i) for i in v])(ret)).strip('\x00')

    def readregs(self, readlist, size=1):
        """
            Read Data from Device.
            readlist = [function code, address, data type]
        """
        if self.isopened is False:
            return None

        try:
            retlist = pymodbus.read_registers(readlist[0:3], size)
        except BaseException as err:
            if self.platform == 'linux':
                led.ioctl(led.IXORA_LED4, led.GREEN, led.LOW)
                led.ioctl(led.IXORA_LED4, led.RED, led.HIGH)
            print(err)
            return None
        else:
            if self.platform == 'linux':
                led.ioctl(led.IXORA_LED4, led.RED, led.LOW)
                led.ioctl(led.IXORA_LED4, led.GREEN, led.HIGH)
            else:
                pass

        return retlist


# if __name__ == '__main__':
#     MODBUS = PBoxModbus()
#     print(MODBUS.newtcp())
#     print(MODBUS.readregs([3, 1, 'U16']))

