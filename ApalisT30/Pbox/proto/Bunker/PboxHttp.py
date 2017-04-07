# -*- coding:utf-8 -*-
""" PboxHttp """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  Http.
# History:  2017/01/18 V1.0.0[Heyn]
#           2017/02/14 V1.0.1[Heyn] BaseException
#           2017/03/14 V1.0.2[Heyn] Cloud server exception handling

import time
import json
import uuid
import requests


class PboxHttp:
    """Pbox http"""

    def __init__(self, ip='127.0.0.1', table_name='PYTHON', timeout=3):
        super(PboxHttp, self).__init__()
        self.sess = requests.session()
        self.table = table_name + str(uuid.UUID(int=uuid.getnode()).hex[-12:]).upper()
        self.timeout = timeout
        self.createurl = 'http://' + ip + ':8080/WebApi/Create'
        self.inserturl = 'http://' + ip + ':8080/WebApi/Insert'
        print('[Bunker] Cloud IP Address = %s'%ip)

    def __del__(self):
        pass

    def create(self, items_data):
        """Create Table Message."""
        # create_data = {'table_name': self.table, 'items' : items_data}
        create_data = dict(table_name=self.table, delFlg=0, items=[])

        print('[Bunker] Cloud Table Name = %s'%self.table)

        for items in items_data.get('items'):
            checktype = items.get('itemType')
            if checktype == 'BOOL':
                checktype = 'INT16'
            create_data['items'].append(dict(itemName=items.get('itemName'),\
                                             itemType=checktype))
        try:
            ret = self.sess.post(self.createurl, data=json.dumps(create_data), timeout=self.timeout)
            val = int(ret.text)
        except BaseException:
            return -1
        else:
            pass

        if val == -1:
            pass
        return val

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
            val = int(ret.text)
        except BaseException:
            return -1
        else:
            pass

        if val == -1:
            pass

        return val
