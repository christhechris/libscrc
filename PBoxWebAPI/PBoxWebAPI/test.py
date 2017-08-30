# -*- coding:utf8 -*-
""" Test library for PBoxWebAPI """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test library for PBoxWebAPI.
# History:  2017-08-17 Wheel Ver:0.1.5 [Heyn] Initialize

import unittest
import libscrc

from PBoxWebAPI import *
# import PBoxWebAPI

class TestPBoxWebAPI(unittest.TestCase):
    """Test PBoxWebAPI.
    """

    def do_basics(self, module):
        """Test basic functionality.
        """
        ret = module.login(url='https://192.168.3.222', password='admin')
        self.assertEqual(ret, True)

        ret = module.newchannel(name='Test', items=['Modbus-TCP', '127.0.0.1', '51320', '5000'], flag=True)
        self.assertEqual(ret, True)

        ret = module.alterchannel(name='Test', items=['Modbus-TCP', '127.0.0.1', '51320', '5000'])
        self.assertEqual(ret, True)
        
        ret = module.newdevice(name='Test')
        self.assertEqual(ret, True)

        ret = module.alterdevice(name='Test')
        self.assertEqual(ret, True)
  
        ret = module.newitem(['python', 'test', '5000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0'])
        self.assertEqual(ret, True)

        self.assertEqual(module.delitems(), True)
        self.assertEqual(module.deldevice(), True)
        self.assertEqual(module.delchannel(), True)
        self.assertEqual(module.cloudaddress('47.93.79.77'), True)
        self.assertEqual(module.lanipaddress(), True)
        self.assertEqual(module.wanipaddress(dhcp='NO'), True)
        self.assertEqual(module.netswitch(), True)

    def test_basics(self):
        """Test basic functionality.
        """
        self.do_basics(PBoxWebAPI())


if __name__ == '__main__':
    unittest.main()
