# -*- coding:utf8 -*-
""" PboxHttp """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Http.
# History:  2017/01/18 V1.0.0[Heyn]

import time
import json
# import urllib
# import urllib.request
import requests

#WEBSERVERCREATE = 'http://192.168.5.100:8080'
#WEBSERVERINSERT = 'http://192.168.5.100:8080'

WEBSERVERCREATE = 'http://10.194.154.212:8080/WebApi/Create'
WEBSERVERINSERT = 'http://10.194.154.212:8080/WebApi/Insert'


class PboxHttp:
    """Pbox http"""

    def __init__(self, table_name='default'):
        super(PboxHttp, self).__init__()
        self.sess = requests.session()
        self.table = table_name

    def create(self, items_data):
        """Create Table Message."""
        create_data = {'table_name': self.table, 'items' : items_data}
        print(create_data)
        ret = self.sess.post(WEBSERVERCREATE, data=json.dumps(create_data))
        # print(ret.text)
        return int(ret.text)

    def insert(self, items_data):
        """Insert Data to DataBase."""
        insert_dict = {'table_name': self.table}
        insert_dict['time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        insert_dict['items'] = items_data
        ret = self.sess.post(WEBSERVERINSERT, data=json.dumps(insert_dict))
        print(ret.text)

