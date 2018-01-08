# -*- coding:utf-8 -*-
""" PBoxIF for Alicloud """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PBox interface (Https or http).
# History:  2017/01/18 V1.0.0 [Heyn]
#           2017/02/14 V1.0.1 [Heyn] BaseException
#           2017/03/14 V1.0.2 [Heyn] Cloud server exception handling
#           2018/01/03 V1.1.0 [Heyn] New https AUTH and Optimization code.


import time
import json
import uuid
import logging
import requests
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3 import disable_warnings


def catch_exception(origin_func):
    """Catch exception."""
    def wrapper(self, *args, **kwargs):
        """Wrapper."""
        try:
            return origin_func(self, *args, **kwargs)
        except BaseException as msg:
            logging.error('[ERROR] %s an exception raised. *** %s ***', origin_func, str(msg))
            return False
    return wrapper

def msg_register(method):
    """Message register"""
    # pylint: disable=C0301
    def decorator(func):
        """Decorator."""
        def wrapper(self, *args, **kwargs):
            """Wrapper."""
            url, payload = func(self, *args, **kwargs)
            header = {'Content-Type':'application/x-www-form-urlencoded',
                      'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

            if method == 'POST':
                ret = self.sess.post(url, data=payload, headers=header, timeout=self.timeout, verify=False)
            elif method == 'GET':
                ret = self.sess.get(url, headers=header, timeout=self.timeout, verify=False)
            else:
                return 'ERROR'

            result = ''
            if ret.status_code == 200:
                try:
                    result = json.loads(ret.text, encoding='UTF-8')
                except BaseException:
                    result = ret.text.strip()
            else:
                result = 'ERROR'
                logging.debug(ret.status_code)
            return result
        return wrapper
    return decorator

class PBoxIF:
    """ PBox Interface. """

    def __init__(self,
                 ip='127.0.0.1',
                 port=8443,
                 mode='https',
                 pboxid=(uuid.UUID(int=uuid.getnode()).hex[-12:]).upper(),
                 deviceid='PYTHON'):

        self.__tablename = 'table_{0}_{1}'.format(pboxid, deviceid)
        self.__createurl = '{0}://{1}:{2}/WebApi/Create'.format(mode, ip, port)
        self.__inserturl = '{0}://{1}:{2}/WebApi/Insert'.format(mode, ip, port)
        self.__getimeurl = '{0}://{1}:{2}/WebApi/Time'.format(mode, ip, port)

        logging.info('[PBoxIF] TableName = %s', self.__tablename)
        logging.info('[PBoxIF] IPAddress = %s:%d', ip, port)

    @catch_exception
    def synctime(self):
        """ Insert values to table
            @retvalue: -1 or -2 Failed
                       >0 Success
                        1 Data error
        """
        cloudtime = msg_register('POST')(lambda x, y: y)(self, (self.__getimeurl, ''))
        if len(str(cloudtime)) < 13:
            logging.error('SYNC time failed......')
            return time.localtime()

        return time.localtime(int(str(cloudtime)[:-3]))

    @catch_exception
    @msg_register('POST')
    def create(self, types, delflag=1):
        """ Create Table Message.
            @params: types = [dict(itemName='PYTHON08', itemType='STRING40')]
                     delflag: 1 -> Delete DB table.
                              0 -> Do not delete DB table.
            @retvalue: -1 Failed
                        0 Success
                        1 Data error
        """
        if not isinstance(types, list):
            raise TypeError('create(types) Parameter must be list type.')
        itemslist = [dict(itemName='StatisticTime', itemType='STRING40')] + types
        table = dict(table_name=self.__tablename,
                     delFlg=delflag,
                     items=itemslist)
        logging.debug(table)
        return (self.__createurl, json.dumps(table))

    @catch_exception
    @msg_register('POST')
    def insert(self, value):
        """ Insert values to table
            @params: value = [dict(itemName='PYTHON08', value='Hello')]
            @retvalue: -1 Failed
                        0 Success
                        1 Data error
        """
        if not isinstance(value, list):
            raise TypeError('insert(value) Parameter must be list type.')
        hours = int(time.strftime("%H", time.localtime()))
        itemslist = [dict(itemName='StatisticTime', value='%02d:00-%02d:00'%(hours, hours+1))] + value
        values = dict(table_name=self.__tablename,
                      time=time.strftime("%Y%m%d %H:%M:%S", time.localtime()),
                      items=itemslist)
        logging.debug(values)
        return (self.__inserturl, json.dumps(values))

class PBoxHttp(PBoxIF):
    """ PBox HTTP. """

    def __init__(self,
                 ip='127.0.0.1',
                 port=8080,
                 pboxid=(uuid.UUID(int=uuid.getnode()).hex[-12:]).upper(),
                 deviceid='PYTHON',
                 timeout=5):

        PBoxIF.__init__(self, ip, port, 'http', pboxid, deviceid)
        self.timeout = int(timeout)
        self.sess = requests.session()

class PBoxHttps(PBoxIF):
    """ PBox HTTPs. """

    def __init__(self,
                 ip='127.0.0.1',
                 port=8443,
                 pboxid=(uuid.UUID(int=uuid.getnode()).hex[-12:]).upper(),
                 deviceid='PYTHON',
                 timeout=5):

        PBoxIF.__init__(self, ip, port, 'https', pboxid, deviceid)
        self.timeout = int(timeout)

        disable_warnings()    # 2017-08-01 for https verify = False
        self.sess = requests.session()
        self.sess.auth = HTTPDigestAuth('admin', 'admin') # 2018/01/03 V1.1.0

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    # CCC = PBoxHttp(ip='127.0.0.1')
    # print(CCC.synctime())
    # print(CCC.create([dict(itemName='PYTHON08', itemType='STRING40')], 1))
    # print(CCC.insert([dict(itemName='PYTHON08', value='Hello')]))

    SSS = PBoxHttps(ip='127.0.0.1')
    print(SSS.create([dict(itemName='PYTHON08', itemType='STRING40')], 0))
    while True:
        print(SSS.insert([dict(itemName='PYTHON08', value='Hello')]))
        print(SSS.synctime())
