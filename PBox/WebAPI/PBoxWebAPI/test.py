# -*- coding:utf-8 -*-
""" Test library for PBoxWebAPI """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test library for PBoxWebAPI.
# History:  2017-08-17 Wheel Ver:0.1.5 [Heyn] Initialize
#           2017-11-16 Wheel Ver:1.2.1 [Heyn] Modfiy wanipaddress()


import unittest
from PBoxWebAPI import PBoxWebAPI

class TestPBoxWebAPI(unittest.TestCase):
    """Test PBoxWebAPI.
    """

    def do_basics(self, module):
        """Test basic functionality.
        """
        ret = module.login(url='https://192.168.0.1', password='admin')
        self.assertEqual(ret, True)

        ret = module.newpassword('admin')
        self.assertEqual(ret, True)

        ret = module.confpassword('admin')
        self.assertEqual(ret, True)

        ret = module.newchannel(name='Test', items=['Modbus-TCP', '127.0.0.1', '51320', '5000'], flag=True)
        self.assertEqual(ret, True)

        ret = module.alterchannel(name='Test', items=['Modbus-TCP', '127.0.0.1', '51320', '5000'])
        self.assertEqual(ret, True)

        ret = module.newdevice(name='Test')
        self.assertEqual(ret, True)

        ret = module.alterdevice(name='Test')
        self.assertEqual(ret, True)

        ret = module.newitem(['python', 'test', '10000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0'])
        self.assertEqual(ret, True)

        self.assertEqual(module.delitems(), True)
        self.assertEqual(module.deldevice(), True)
        self.assertEqual(module.delchannel(), True)
        self.assertEqual(module.cloudaddress('47.93.79.77'), True)
        self.assertEqual(module.lanipaddress(), True)
        self.assertEqual(module.wanipaddress({'_dhcp':'NO', '_ip':'10.10.10.10', '_mask':'255.255.255.0', '_gateway':'10.10.10.1', '_dns':'8.8.8.8'}), True)
        self.assertEqual(module.netswitch(), True)

        print(module.version())
        print(module.datetime())

        ret = module.update()
        self.assertEqual(ret, False)

        #ret = module.recovery()
        #self.assertEqual(ret, True)

    def test_basics(self):
        """Test basic functionality.
        """
        self.do_basics(PBoxWebAPI())


if __name__ == '__main__':
    unittest.main()
