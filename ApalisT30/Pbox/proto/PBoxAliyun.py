# -*- coding:UTF-8 -*-
""" PBox Aliyun API"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7
# Author:   Heyn
# Program:  Modbus RTU & TCP
# History:  2017/01/18 V1.0.0 [Heyn]
#           2017/02/14 V1.0.1 [Heyn] BaseException
#           2017/03/14 V1.0.2 [Heyn] Cloud server exception handling
#           2017/04/08 V1.0.3 [Heyn] Redesign PBoxAliyun class functions.
#           2017/04/10 V1.0.4 [Heyn] Bug fixe import imx6_ixora_led as led

# Linux or ARM Platform: You should have requests package.

import sys
import time
import json
import requests

if sys.platform == 'linux':
    import imx6_ixora_led as led

class PBoxAliyun:
    """Pbox Aliyun Class"""

    def __init__(self, ip='127.0.0.1', tablename='default', timeout=3):
        super(PBoxAliyun, self).__init__()
        self.timeout = timeout
        self.tablename = tablename
        self.createurl = 'http://' + ip + ':8080/WebApi/Create'
        self.inserturl = 'http://' + ip + ':8080/WebApi/Insert'

        self.platform = sys.platform

        print('[PboxAliyun] IP Address = %s'%ip)
        self.sess = requests.session()


    def __del__(self):
        if self.platform == 'linux':
            led.ioctl(led.IXORA_LED5, led.GREEN, led.LOW)
            led.ioctl(led.IXORA_LED5, led.RED, led.LOW)

    def create(self, items_data):
        """
            Create MySQL Table Message.
            items_data = dict(Items[ {itemName='', itemType=''}, {...}])
        """

        # create_data = {'table_name': self.table, 'items' : items_data}
        create_data = dict(table_name=self.tablename, delFlg=0, items=[])
        print('[PboxAliyun] Table Name = %s'%self.tablename)

        for items in items_data.get('Items'):
            create_data['items'].append(dict(itemName=items.get('itemName'),\
                                             itemType=items.get('itemType')))
        try:
            ret = self.sess.post(self.createurl, data=json.dumps(create_data), timeout=self.timeout)
            val = int(ret.text)
        except BaseException as err:
            val = -1
            print(err)

        if self.platform == 'linux':
            if val == 0:
                led.ioctl(led.IXORA_LED5, led.GREEN, led.HIGH)
                led.ioctl(led.IXORA_LED5, led.RED, led.LOW)
            else:
                led.ioctl(led.IXORA_LED5, led.GREEN, led.LOW)
                led.ioctl(led.IXORA_LED5, led.RED, led.HIGH)

        return val

    def insert(self, items_data):
        """
        Insert MySQL Table Message.
        items_data = [{itemName='', value=''}, {...}].
        """

        insert_dict = {'table_name': self.tablename}
        insert_dict['time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        insert_dict['items'] = items_data

        try:
            ret = self.sess.post(self.inserturl, data=json.dumps(insert_dict), timeout=self.timeout)
            val = int(ret.text)
        except BaseException as err:
            val = -1
            print(err)

        if self.platform == 'linux':
            if val == 0:
                led.ioctl(led.IXORA_LED5, led.GREEN, led.HIGH)
                led.ioctl(led.IXORA_LED5, led.RED, led.LOW)
            else:
                led.ioctl(led.IXORA_LED5, led.GREEN, led.LOW)
                led.ioctl(led.IXORA_LED5, led.RED, led.HIGH)

        return val


