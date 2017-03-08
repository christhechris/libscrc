# -*- coding:utf-8 -*-
""" PboxHttp """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Http.
# History:  2017/01/18 V1.0.0[Heyn]
#           2017/02/14 V1.0.1[Heyn] BaseException

import time
import json
import requests

import imx6_ixora_led as led

class PboxHttp:
    """Pbox http"""

    def __init__(self, ip='127.0.0.1', table_name='default', timeout=3):
        super(PboxHttp, self).__init__()
        self.sess = requests.session()
        self.table = table_name
        self.timeout = timeout
        self.createurl = 'http://' + ip + ':8080/WebApi/Create'
        self.inserturl = 'http://' + ip + ':8080/WebApi/Insert'
        print('[Modbus TCP] Cloud IP Address = %s'%ip)

    def __del__(self):
        led.ioctl(led.IXORA_LED5, led.GREEN, led.LOW)
        led.ioctl(led.IXORA_LED5, led.RED, led.LOW)

    def create(self, items_data):
        """Create Table Message."""
        # create_data = {'table_name': self.table, 'items' : items_data}
        create_data = dict(table_name=self.table, items=[])

        print('[Modbus TCP] Cloud Table Name = %s'%self.table)
        for items in items_data.get('Items'):
            create_data['items'].append(dict(itemName=items.get('itemName'),\
                                             itemType=items.get('itemType')))

        try:
            ret = self.sess.post(self.createurl, data=json.dumps(create_data), timeout=self.timeout)
        except BaseException:
            led.ioctl(led.IXORA_LED5, led.RED, led.HIGH)
            return -1
        else:
            led.ioctl(led.IXORA_LED5, led.GREEN, led.HIGH)
        return int(ret.text)

    def insert(self, items_data):
        """
        Insert Data to DataBase.
        items_data type is list.
        """

        insert_dict = {'table_name': self.table}
        insert_dict['time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        insert_dict['items'] = items_data

        try:
            ret = self.sess.post(self.inserturl, data=json.dumps(insert_dict), timeout=self.timeout)
        except BaseException:
            led.ioctl(led.IXORA_LED5, led.GREEN, led.LOW)
            led.ioctl(led.IXORA_LED5, led.RED, led.HIGH)
            return -1
        else:
            led.ioctl(led.IXORA_LED5, led.RED, led.LOW)
            led.ioctl(led.IXORA_LED5, led.GREEN, led.HIGH)
        return int(ret.text)
