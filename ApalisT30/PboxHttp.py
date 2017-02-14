# -*- coding:utf8 -*-
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

# DBCREATEURL = 'http://192.168.5.100:8080'
# DBINSERTURL = 'http://192.168.5.100:8080'

DBCREATEURL = 'http://10.194.154.212:8080/WebApi/Create'
DBINSERTURL = 'http://10.194.154.212:8080/WebApi/Insert'


class PboxHttp:
    """Pbox http"""

    def __init__(self, table_name='default', timeout=3):
        super(PboxHttp, self).__init__()
        self.sess = requests.session()
        self.table = table_name
        self.timeout = timeout

    def create(self, items_data):
        """Create Table Message."""
        create_data = {'table_name': self.table, 'items' : items_data}
        try:
            ret = self.sess.post(DBCREATEURL, data=json.dumps(create_data), timeout=self.timeout)
        except BaseException:
            return -1
        return int(ret.text)

    def insert(self, items_data):
        """Insert Data to DataBase."""
        insert_dict = {'table_name': self.table}
        insert_dict['time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        insert_dict['items'] = items_data
        try:
            ret = self.sess.post(DBINSERTURL, data=json.dumps(insert_dict), timeout=self.timeout)
        except BaseException:
            return -1
        return int(ret.text)

