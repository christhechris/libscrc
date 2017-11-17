# -*- coding:utf-8 -*-
""" PBox WebMc API """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PBox WebMc API.
# History:  2017-07-27 V1.0 [Heyn]
#           2017-08-01 V1.1 [Heyn] New support https <verify=False>
#           2017-08-04 Wheel Ver:0.0.5 [Heyn] login\newchannel\newdevice. -> @catch_exception
#           2017-08-07 Wheel Ver:0.0.6 [Heyn]
#                            BugFix001: newchannel\newdevice\newitem return True or False.
#                            New : alterchannel() alterdevice() alteritem() lanipaddress()
#                            New : cloudaddress() download2app() reboot() newpassword()
#           2017-08-22 Wheel Ver:0.0.7 [Heyn]
#                            Modify newchannel(self, items, name='default')
#                            to     newchannel(self, items, freq=5000, name='default')
#           2017-08-23 Wheel Ver:0.0.9 [Heyn]
#                            New : Get channel id in self.login funciotn.
#                            New function : Delchannel befor Newchannel
#           2017-08-25 Wheel Ver:0.1.1 [Heyn]
#                            New : get_pansert() funciotn.
#                            TODO: get_siap()
#           2017-08-28 Wheel Ver:0.1.5 [Heyn] Optimization code.
#           2017-08-30 Wheel Ver:0.1.6 [Heyn] Optimization code msg_register()
#           2017-09-04 Wheel Ver:0.1.9 [Heyn] New add confpassword()
#           2017-09-05 Wheel Ver:0.2.1 [Heyn] Optimization code __siap() and __panasert()
#           2017-09-07 Wheel Ver:1.0.0 [Heyn] New class AESCipher for Openssl Encrypt & Decrypt
#           2017-09-07 Wheel Ver:1.0.1 [Heyn] New __getdriverinfo() \ __getbasicinfo()
#                                                 version() \ datetime()
#           2017-09-12 Wheel Ver:1.1.0 [Heyn]
#                            BugFix002 datetime() Process webmc return value |17|09|12|14|36|20
#                            New upate() \ recovery()
#
#           2017-09-13 Wheel Ver:1.1.1 [Heyn] BugFix003 Removed logging.basicConfig(xxxxxx) in __init__()
#           2017-11-13 Wheel Ver:1.1.3 [Heyn] New informations()
#           2017-11-14 Wheel Ver:1.2.0 [Heyn] Modify newchannel() params  & New save() & New load()
#           2017-11-16 Wheel Ver:1.2.1 [Heyn] New wifi() & Modify wanipaddress() & Encrypt(Decrypt) Configure file.
#           2017-11-17 Wheel Ver:1.2.2 [Heyn] Optimization code.
#

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]


import re
import json
import logging

from uuid import getnode
from uuid import UUID as key

from os import urandom
from hashlib import md5
from time import strptime
from base64 import b64encode
from base64 import b64decode
from collections import OrderedDict

import requests
from Crypto.Cipher import AES
from prettytable import  PrettyTable

#################################################
ERROR_CODE = 'ERROR'
SUCCESS_CODE = 'SUCCESS'
#################################################

HTTPS_VERIFY = False

def catch_exception(origin_func):
    """Catch exception."""
    def wrapper(self, *args, **kwargs):
        """Wrapper."""
        try:
            return origin_func(self, *args, **kwargs)
        except BaseException as msg:
            logging.warning('[ERROR] %s an exception raised. *** %s ***', origin_func, str(msg))
            return False
    return wrapper

@catch_exception
def msg_register(method, cgi, timeout=5):
    """Message register"""
    # pylint: disable=C0301
    def decorator(func):
        """Decorator."""
        def wrapper(self, *args, **kwargs):
            """Wrapper."""
            payload = func(self, *args, **kwargs)
            header = {'Content-Type':'application/x-www-form-urlencoded',
                      'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'}
            if method == 'POST':
                # 2017-08-01 for https verify = False
                ret = self.sess.post(self.url + cgi,
                                     data=payload,
                                     headers=header,
                                     timeout=timeout,
                                     verify=HTTPS_VERIFY)
            elif method == 'GET':
                # 2017-08-01 for https verify = False
                ret = self.sess.get(self.url + cgi, headers=header, timeout=timeout, verify=HTTPS_VERIFY)
            else:
                return ERROR_CODE
            logging.debug('CGI=%s DATA=%s RET_CODE=%s TEXT=%s', cgi, str(payload), str(ret.status_code), str(ret.text))
            result = dict(result=ERROR_CODE, status='404', detail='')
            if (ret.status_code == 200) and ((SUCCESS_CODE in ret.text) or (ERROR_CODE not in ret.text)):
                # Wheel 1.1.0 BUGFIX002: datetime()
                try:
                    result['status'] = (lambda x: '0' if 'status' not in x.keys() else x['status'])(json.loads(ret.text))
                    result['result'] = ERROR_CODE if result['status'] != '0' else SUCCESS_CODE
                    result['detail'] = ret.text if SUCCESS_CODE in ret.text else json.loads(ret.text)
                except BaseException:
                    result['status'] = '0'
                    result['result'] = SUCCESS_CODE
                    result['detail'] = ret.text.strip()

                if result['result'] == ERROR_CODE:
                    logging.warning('Function = %s()  %s', func, result)
            else:
                logging.warning('Function = %s ret = %s, text = %s', func, ret, str(ret.text).strip('\n'))
            return result
        return wrapper
    return decorator

@catch_exception
def print_pretty(title):
    """Print Pretty,"""
    def decorator(func):
        """Decorator."""
        def wrapper(*args, **kwargs):
            """Wrapper."""
            table = PrettyTable(title)
            table.align[title[0]] = '1'
            table.padding_width = 1
            for item in func(*args, **kwargs):
                table.add_row(item)
            return table
        return wrapper
    return decorator


BLOCK_SIZE = 16  # Bytes
class AESCipher:
    # pylint: disable=C0301
    # pylint: disable=C0325
    """ Implement openssl compatible AES-256 CBC mode encryption/decryption
        This module provides encrypt() and decrypt() functions that are compatible with the openssl algorithms.
    """

    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3.5 and PyCrypto 2.6.1.
    """
    def __init__(self, key):
        self.__key = md5(key.encode('UTF-8')).hexdigest()
        self.__pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        self.__unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def __get_key_and_iv(self, password, salt, klen=32, ilen=16, msgdgst='md5'):
        """
        Derive the key and the IV from the given password and salt.
        @param password  The password to use as the seed.
        @param salt      The salt.
        @param klen      The key length.
        @param ilen      The initialization vector length.
        @param msgdgst   The message digest algorithm to use.
        """
        # equivalent to:
        #   from hashlib import <mdi>  as mdf
        #   from hashlib import md5    as mdf
        #   from hashlib import sha512 as mdf

        mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
        password = password.encode('UTF-8', 'ignore')

        try:
            maxlen = klen + ilen
            keyiv = mdf(password + salt).digest()
            tmp = [keyiv]
            while len(tmp) < maxlen:
                tmp.append(mdf(tmp[-1] + password + salt).digest())
                keyiv += tmp[-1]  # append the last byte
            key = keyiv[:klen]
            ivt = keyiv[klen:klen+ilen]
            return key, ivt
        except UnicodeDecodeError:
            return None, None


    def encrypt(self, plaintext):
        """ Encrpyt plaintext.
            #echo 'This is plain text !' | openssl aes-256-cbc -e -k password | openssl base64 -e
            U2FsdGVkX1/6LeCeSdQh2qXEV76f48q2uWkNJdlt73vol+Eg9BUpfZ24yD8QymTv
        """
        salt = urandom(8)
        key, ivt = self.__get_key_and_iv(self.__key, salt, msgdgst='md5')
        if key is None or ivt is None:
            return None

        plaintext = self.__pad(plaintext)
        cipher = AES.new(key, AES.MODE_CBC, ivt)
        openssl_ciphertext = b'Salted__' + salt + cipher.encrypt(plaintext)
        return b64encode(openssl_ciphertext)

    def decrypt(self, ciphertext):
        """ Decrypt ciphertext.
            #echo 'U2FsdGVkX1/6LeCeSdQh2qXEV76f48q2uWkNJdlt73vol+Eg9BUpfZ24yD8QymTv' | openssl aes-256-cbc -d -k password -base64
            This is plain text !
        """
        ciphertext = b64decode(ciphertext)
        assert(ciphertext[:8] == b'Salted__')
        salt = ciphertext[8:16]

        key, ivt = self.__get_key_and_iv(self.__key, salt, msgdgst='md5')
        if key is None or ivt is None:
            return None
        cipher = AES.new(key, AES.MODE_CBC, ivt)
        return self.__unpad(cipher.decrypt(ciphertext[16:])).decode('UTF-8')

class PBoxWebAPI:
    """PBox WebMc API Class."""
    # pylint: disable=C0301
    # pylint: disable=too-many-instance-attributes

    def __init__(self, url='https://192.168.3.111'):
        self.url = url + '/cgi-bin/'
        requests.packages.urllib3.disable_warnings()    # 2017-08-01 for https verify = False
        self.sess = requests.session()
        self.__token = '200'
        self.saveinfo = dict()
        self.username = self.password = self.passwordmd5 = 'admin'
        self.pboxinfo = self.driverinfo = self.basicinfo = None
        self.jcid = self.jdid = dict(id='0') # JSON Channel ID & JSON Device ID.

    @msg_register('POST', 'Login.cgi')
    def __logininit(self, username='admin', password='admin'):
        """
            Login init.
            @param username  The username to use as login.
            @param password  The password to use as login.
        """
        params = OrderedDict()
        params['UserName'] = self.username = username
        params['PassWord'] = self.passwordmd5 = md5(password.encode('UTF-8')).hexdigest()

        self.password = password
        return params

    @msg_register('POST', 'Verifypasswd.cgi')
    def __loginverify(self):
        """Login Verify"""

        params = OrderedDict(TokenNumber=self.__token)
        params['UserName'] = self.username
        params['PassWord'] = self.passwordmd5
        return params

    @catch_exception
    def login(self, url='http://192.168.3.111', username='admin', password='admin'):
        """ WebMc Login
            @param url       url for device. ex: https://ipaddress or http://ipaddress
            @param username  The username to use as login.
            @param password  The password to use as login.
            2017-08-03 V1.2 [Heyn] New url params
        """
        self.url = url + '/cgi-bin/'
        ret = self.__logininit(username=username, password=password)
        if ERROR_CODE in ret.get('result', ERROR_CODE):
            if ret.get('status') == '300':
                self.__token = ret['detail']['token']
                return True
            return False

        self.__token = ret['detail']['token']
        if ERROR_CODE in self.__loginverify().get('result', ERROR_CODE):
            return False

        self.__getsetupinfo()
        self.__getdriverinfo()

        logging.info('PBox Channel ID %s', self.jcid)
        logging.info('PBox Devices ID %s', self.jdid)
        return True

    @catch_exception
    def __parseinfo(self):
        """ Parse setupinfo & . """
        if self.__getsetupinfo() is False:
            return False

        modeldict = self.pboxinfo.get('pboxsetup', {}).get('model', {})

        if self.jcid['id'] != '0':
            self.saveinfo.update(CHLName=modeldict.get('_name', None))
            self.saveinfo.update(CHLFreq=modeldict.get('_freq', None))
            self.saveinfo.update(CHLConf=modeldict.get('_config', None))

        if self.jdid['id'] != '0':
            self.saveinfo.update(DEVName=modeldict.get('device', {}).get('_name', ''))
            itemslist = []
            for item in modeldict.get('device', {}).get('commDataItems', [''])[0].get('dataItem', []):
                itemslist.append([item['_name'], item['_alias'], item['_freq'], item['_type'], item['_rw'], item['_report'], item['_config']])
            self.saveinfo.update(DataItems=itemslist)

        if self.__getbasicinfo() is False:
            return False

        self.saveinfo.update(BaseInfo=self.basicinfo.get('Pbox', {}))
        return True

    @catch_exception
    def __getsetupinfo(self):
        """Get PBox Configure Information"""
        ret = msg_register('GET', 'Pboxgetsetupinfo.cgi')(lambda x, y: y)(self, None)
        if SUCCESS_CODE in ret.get('result', ERROR_CODE):
            self.pboxinfo = ret.get('detail')
            self.jcid = dict(id=self.pboxinfo.get('pboxsetup', {}).get('model', {}).get('_id', '0'))
            self.jdid = dict(id=self.pboxinfo.get('pboxsetup', {}).get('model', {}).get('device', {}).get('_id', '0'))
            return True
        return False

    @catch_exception
    def __getdriverinfo(self):
        """Get PBox Driver Information."""
        ret = msg_register('GET', 'Pboxgetdriverinfo.cgi')(lambda x, y: y)(self, None)
        if SUCCESS_CODE in ret.get('result', ERROR_CODE):
            self.driverinfo = ret.get('detail')
            return True
        return False

    @catch_exception
    def __getbasicinfo(self):
        """Get PBox Basic Information
        {'Pbox': {'NetworkInfo': {'localip': '192.168.3.222',
                                  'Gateway': {'_gateway': '192.168.3.1',
                                              '_mask': '255.255.255.0',
                                              '_dns': '1.1.1.1',
                                              '_dhcp': 'YES',
                                              '_ip': '10.194.148.181'},
                                  'Wifi': {'_gateway': '192.168.2.1',
                                           '_mask': '255.255.0.0',
                                           '_dns': '2.2.2.2',
                                           '_dhcp': 'NO',
                                           '_ip': '11.124.134.178'},
                                  'Mode': 'gateway'},
                 'BasicInfo': {'HardwareModel': '20170830',
                               'SerialNumber': '00142d4d0198\n',
                               'AgentVersion': '20170830',
                               'SoftVersion': '20170830'},
                 'Wifi': {'SSID': 'TP-LINK_3G_PBOX'},
                 'CloudInfo': {'Address': '47.93.79.77'}}}
        """
        ret = msg_register('GET', 'Pboxgetbasicinfo.cgi')(lambda x, y: y)(self, None)
        if SUCCESS_CODE in ret.get('result', ERROR_CODE):
            self.basicinfo = ret.get('detail')
            return True
        return False

    def version(self):
        """Get PBox software and hardware informations.
        @retvalue: {'SoftVersion': '20170830', 'HardwareModel': '20170830', 'SerialNumber': '00142d4d0198\n', 'AgentVersion': '20170830'}
        """
        if self.__getbasicinfo() is False:
            return None
        return self.basicinfo.get('Pbox', None).get('BasicInfo', None)

    @catch_exception
    def newchannel(self, items, freq=10000, name='default', flag=True):
        """ PBox new a channel.
            @param items
                ['Modbus-RTU', '/dev/ttymxc1', '9600', 'None', '8', '1', '1000']
                ['Modbus-TCP', '192.168.3.1', '54321', '1000']
                ['Panasert-COM', '/dev/ttymxc1', '4800', 'None', '7', '1', '1000', '0']
                ['Panasert-TCP', '192.168.3.1', '54321', '1000']
                ['Siap', '192.168.3.1', '54321', '10000']
            Wheel V1.2.0 later:
                ['Modbus-RTU', '232', '9600', 'None', '8', '1', '1000']
                ['Modbus-RTU', '485', '9600', 'None', '8', '1', '1000']
                ['Modbus-RTU', '422', '9600', 'None', '8', '1', '1000']

            @param flag
                flag = True  -> Delete channel
                flag = False -> Don't delete channel
        """

        self.__getsetupinfo()
        if flag is True and re.match(r'1|2', self.jcid['id']) and self.delchannel() is False:
            return False

        payload = ['TokenNumber=' + self.__token,
                   'ChannelName=' + name,
                   'ChannelConf=' + ';'.join(items),
                   'DeviceCFreq=' + str(freq)]

        ret = msg_register('POST', 'AddChannel.cgi')(lambda x, y: '&'.join(y))(self, payload)
        if ERROR_CODE in ret.get('result', ERROR_CODE):
            return False

        self.jcid = ret.get('detail', dict(id='0'))
        logging.debug('PBox New Channel ID=%s', self.jcid)

        return re.match('^[A-Za-z]', name) is not None

    @catch_exception
    def alterchannel(self, items, freq=10000, name='default'):
        """ PBox alter a channel.
            @param items
                ['Modbus-RTU', '/dev/ttymxc1', '9600', 'None', '8', '1', '1000']
                ['Modbus-TCP', '192.168.3.1', '54321', '1000']
                ['Panasert-COM', '/dev/ttymxc1', '4800', 'None', '7', '1', '1000', '0']
                ['Panasert-TCP', '192.168.3.1', '54321', '1000']
                ['Siap', '192.168.3.1', '54321', '10000']

        History : 2017-08-30 V1.1 [Heyn] New deviceCFreq params for siap protocol
        """

        payload = ['TokenNumber=' + self.__token,
                   'ChannelName=' + name,
                   'ChannelID=' + self.jcid['id'],
                   'ChannelConf=' + ';'.join(items),
                   'DeviceCFreq=' + str(freq)]

        ret = msg_register('POST', 'AlterChannel.cgi')(lambda x, y: '&'.join(y))(self, payload)
        logging.debug('PBox Alter Channel ID=%s', self.jcid)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def newdevice(self, name='default'):
        """PBox New Device."""
        params = OrderedDict(TokenNumber=self.__token)
        params['DeviceName'] = name
        params['ChannelID'] = self.jcid['id']
        params['DeviceIP'] = '0.0.0.0'

        ret = msg_register('POST', 'AddDevice.cgi')(lambda x, y: y)(self, params)
        if ret.get('result') is ERROR_CODE:
            return False

        self.jdid = ret.get('detail', dict(id='0'))
        logging.debug('PBox New Device ID=%s', self.jdid)
        # return re.match('^[A-Za-z]', name) is not None
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def alterdevice(self, name='default'):
        """ PBox Alter Device Name.
            @param name     Device name.
        """
        params = OrderedDict(TokenNumber=self.__token)
        params['DeviceName'] = name
        params['ChannelID'] = self.jcid['id']
        params['DeviceID'] = self.jdid['id']
        ret = msg_register('POST', 'AlterDevice.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def delchannel(self):
        """PBox Delete Channel"""
        params = OrderedDict(TokenNumber=self.__token)
        params['DelChannelID'] = self.jcid['id']
        ret = msg_register('POST', 'DeleteChannel.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def deldevice(self):
        """Delete Device."""
        params = OrderedDict(TokenNumber=self.__token)
        params['DelChannelID'] = self.jcid['id']
        params['DelDeviceID'] = self.jdid['id']
        ret = msg_register('POST', 'DeleteDevice.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def newitem(self, items):
        """ PBox New Items
            @param name     Modbus RTU : item=['python', 'test', '5000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0']
        """
        params = [self.__token, self.jdid['id']]
        params.extend(items)

        ret = msg_register('POST', 'AddDataitem.cgi')(lambda x, y: '&'.join(y))(self, list(map(lambda x: 'item=%s'%x, params)))
        # +-----------------------------------------------------------------------------------------------+
        # |                                  True & False Table                                           |
        # +                                -----------------------                                        +
        # |      [WebMc] : Error=0   OK=1    [Name] : Digital=1 Char=0   [Alias] : Digital=1 Char=0       |
        # |                                                                                               |
        # +----------------------+--------+----------------------+--------+----------------------+--------+
        # | WebMc | Name | Alias | Result | WebMc | Name | Alias | Result | WebMc | Name | Alias | Result |
        # +----------------------+--------+----------------------+--------+----------------------+--------+
        # |   0   |   0  |   0   |  False |   0   |   0  |   1   |  True  |   0   |   1  |   0   |  True  |
        # +----------------------+--------+----------------------+--------+----------------------+--------+
        # |   0   |   1  |   1   |  True  |   1   |   0  |   0   |  True  |   1   |   0  |   1   |  False |
        # +----------------------+--------+----------------------+--------+----------------------+--------+
        # |   1   |   1  |   0   |  False |   1   |   1  |   1   |  False |   -   |   -  |   -   |   -    |
        # +----------------------+--------+----------------------+--------+----------------------+--------+
        # return (ret.get('result') == SUCCESS_CODE) ^ ((re.match('^[A-Za-z]', items[0]) is None) or (re.match('^[A-Za-z]', items[1]) is None))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def alteritem(self, items, itemid=None):
        """ PBox Alter Item
            eg.
            Modbus RTU : item=['python', 'test', '5000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0']
            itemid = item id
        """

        params = [self.__token, self.jdid['id']]
        params.extend(items)
        params.extend([itemid['id']])  # DataItem ID

        ret = msg_register('POST', 'AlterDataitem.cgi')(lambda x, y: '&'.join(y))(self, list(map(lambda x: 'item=%s'%x, params)))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def delitems(self):
        """PBox Delelte Items"""
        info = msg_register('GET', 'Pboxgetsetupinfo.cgi')(lambda x, y: y)(self, None)
        if ERROR_CODE in info.get('result', ERROR_CODE):
            return False

        self.pboxinfo = info.get('detail')
        iids = []
        for _, item in enumerate(self.pboxinfo['pboxsetup']['model']['device']['commDataItems'][0]['dataItem']):
            iids.append(item.get('_id'))

        payload = ['TokenNumber=' + self.__token, 'DelItemsID=' + ','.join(iids), 'DelDeviceID=' + self.jdid['id']]
        ret = msg_register('POST', 'DeleteDataitem.cgi')(lambda x, y: y)(self, '&'.join(payload))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def cloudaddress(self, addr='47.93.79.77'):
        """Setting Cloud IP Address"""
        ret = msg_register('POST', 'CloudServerConfig.cgi')(lambda x, y: y)(self, 'TokenNumber=%s&Address=%s'%(self.__token, addr))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def download2app(self):
        """Exe configuration."""
        params = OrderedDict(TokenNumber=self.__token)
        params['LoadDataUp'] = '1'
        ret = msg_register('POST', 'LoadData.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    def __generate_encryption_pwd(self, pwd='P@ssw0rd'):
        """"""
        params = OrderedDict(TokenNumber=self.__token)
        params['OldPassword'] = md5(self.password.encode('UTF-8')).hexdigest()

        # token_md5 = md5(self.__token.encode('UTF-8')).hexdigest()
        # def __encryption(pwd, token):
        #     for xxx in pwd:
        #         tmp = ord(xxx)
        #         for yyy in token:
        #             tmp = tmp ^ (ord(yyy) >> 2)
        #         yield chr(tmp)

        # newpwd = b64encode(bytes(''.join([x for x in __encryption(pwd, token_md5)]), encoding='UTF-8'))

        newpwd = AESCipher(self.__token).encrypt(pwd)

        params['NewPassword'] = params['ConfirmPassword'] = str(newpwd, encoding='UTF-8')
        return params

    @catch_exception
    def newpassword(self, newpassword='P@ssw0rd'):
        """1st Change Password"""
        params = self.__generate_encryption_pwd(newpassword)
        ret = msg_register('POST', 'Changeinitialpsswd.cgi')(lambda x, y: y)(self, params)

        if ERROR_CODE in ret.get('result', ERROR_CODE):
            logging.warning('%s -- %s', params, newpassword)
            return False
        return True

    @catch_exception
    def confpassword(self, newpassword='P@ssw0rd'):
        """Configure login password"""
        params = self.__generate_encryption_pwd(newpassword)
        ret = msg_register('POST', 'PasswordConfig.cgi')(lambda x, y: y)(self, params)

        if ERROR_CODE in ret.get('result', ERROR_CODE):
            logging.warning('%s -- %s', params, newpassword)
            return False
        return True

    @catch_exception
    def lanipaddress(self, ipaddr='192.168.0.1'):
        """Change LAN IP Address."""
        params = OrderedDict(TokenNumber=self.__token)
        params['IPAddress'] = ipaddr
        ret = msg_register('POST', 'LocalIPConfig.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def wanipaddress(self, waninfo):
        """ Change WAN IP Address.
            @param waninfo = {  '_mask' = '255.255.255.0',
                                '_dns': '192.168.0.1',
                                '_dhcp': 'NO',
                                '_ip': '192.168.0.1',
                                '_gateway': '192.168.1.1'
                             }
        """
        params = OrderedDict(TokenNumber=self.__token)
        params['NetMode'] = 'gateway'
        params['DHCPMode'] = waninfo['_dhcp'].upper()
        if params['DHCPMode'] == 'NO':
            for item in ['_ip', '_mask', '_gateway', '_dns']:
                params[item] = waninfo.get(item)

        ret = msg_register('POST', 'IPConfig.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def netswitch(self, mode='gateway'):
        """Switch gateway 4G or wifi."""
        params = OrderedDict(TokenNumber=self.__token)
        params['NetMode'] = params['ModeType'] = mode if mode in ('gateway', '4G', 'wifi') else 'gateway'
        ret = msg_register('POST', 'SwitchInfo.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def reboot(self):
        """Exec configuration."""
        params = OrderedDict(TokenNumber=self.__token)
        params['restart'] = 'restart'
        ret = msg_register('POST', 'RebootArm.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @msg_register('POST', 'RefreshDataitem.cgi')
    def __siap(self):
        """SIAP DataItems."""
        params = OrderedDict(TokenNumber=self.__token)
        params['item'] = 'liaoCang'
        return params

    @msg_register('POST', 'Pboxgetseriadata.cgi', 20)
    def __panasert(self):
        """Panasonic Sert DataItems."""
        params = OrderedDict(TokenNumber=self.__token)
        params['item'] = 'panasert'
        return params

    @catch_exception
    def get_siap(self):
        """Get SIAP DataItems."""
        dataitems = self.__siap()
        return dataitems['detail']['items'] if SUCCESS_CODE in dataitems.get('result', ERROR_CODE) else []

    @catch_exception
    def get_pansert(self):
        """Get Panasonic Sert(TCP or Serial) DataItems."""
        dataitems = self.__panasert()
        return dataitems['detail']['items'] if SUCCESS_CODE in dataitems.get('result', ERROR_CODE) else []

    @catch_exception
    def datetime(self, token=200):
        """ Get system date and time.
            @retvalue   time.struct_time(tm_year=2017, tm_mon=9, tm_mday=11, tm_hour=15, tm_min=22, tm_sec=37, tm_wday=0, tm_yday=254, tm_isdst=-1)
        """
        params = OrderedDict(TokenNumber=self.__token if token == 200 else token)
        params['up'] = ''
        ret = msg_register('POST', 'Timeget.cgi')(lambda x, y: y)(self, params)
        return strptime(ret['detail'].strip(), '|%Y|%m|%d|%H|%M|%S')

    @catch_exception
    def update(self):
        """Firmware Update."""
        params = OrderedDict(TokenNumber=self.__token)
        params['update'] = 'restart'
        ret = msg_register('POST', 'Firmwareupdate.cgi')(lambda x, y: y)(self, params)
        logging.debug('WebMc Firmwareupdate.cgi %s', str(ret))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def recovery(self):
        """ System recovery
            @retvaule   <Response [200]> TEXT=Sun Oct  1 00:00:00 HKT 2017
        """
        params = OrderedDict(TokenNumber=self.__token)
        params['update'] = 'restart'
        try:
            ret = msg_register('POST', 'Recovery.cgi')(lambda x, y: y)(self, params)
        except BaseException:
            return True
        logging.debug('WebMc Recovery.cgi = %s', str(ret))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def informations(self):
        """ Get PBox Basic Informations. """
        params = dict()
        params.update(Protocol=self.pboxinfo.get('pboxsetup', {}).get('model', {}).get('_config', 'None'))
        logging.info('PBox information %s', params)
        return params

    @catch_exception
    def save(self, path):
        """Save PBox configure file."""
        if self.__parseinfo() is False:
            return False

        ciphertext = AESCipher(key(int=getnode()).hex[-12: ]).encrypt(json.dumps(self.saveinfo))
        with open(path, 'w') as fds:
            fds.write(str(ciphertext, 'UTF-8'))
        return True

    def _runload(self, strmsg, func, *args):
        if func(*args):
            logging.info(strmsg + ' Success ')
        else:
            logging.info(strmsg + ' Failure ')

    @catch_exception
    def load(self, path):
        """Load PBox configure file."""
        plaintext = "{}"
        with open(path, 'r') as fds:
            plaintext = AESCipher(key(int=getnode()).hex[-12: ]).decrypt(fds.read())

        loaddict = dict()
        loaddict = json.loads(plaintext)

        if len(loaddict) == 0:
            return False

        self._runload('[*] Load Channel Name ...', self.newchannel, loaddict['CHLConf'].split(';'), loaddict['CHLFreq'], loaddict['CHLName'])
        self._runload('[*] Load Device Name ...', self.newdevice, loaddict['DEVName'])
        for item in loaddict['DataItems']:
            self._runload('[*] Load Item Name ...' + str(item), self.newitem, item)

        netinfo = loaddict.get('BaseInfo', {}).get('NetworkInfo', {})
        self._runload('[*] Load Cloud Address ...', self.cloudaddress, loaddict['BaseInfo']['CloudInfo']['Address'])
        self._runload('[*] Load PBox Net Mode ...', self.netswitch, netinfo.get('Mode', '4G'))
        self._runload('[*] Load LAN Setting ...', self.lanipaddress, netinfo.get('localip', '192.168.0.1'))
        self._runload('[*] Load WAN Setting ...', self.wanipaddress, netinfo['Gateway'])
        # TODO
        # Can't get wifi password from webmc
        self._runload('[*] Load WiFi Setting ...', self.wifi, loaddict['BaseInfo']['Wifi']['SSID'], 'WIFIPassWord', netinfo['Wifi'])

        return True

    @catch_exception
    def wifi(self, ssid, wpwd, wifinfo):
        """ Wi-Fi Setting.
            [TODO: Can't get wifi password from webmc]
            @param wifinfo = {  '_mask' = '255.255.255.0',
                                '_dns': '192.168.0.1',
                                '_dhcp': 'NO',
                                '_ip': '192.168.0.1',
                                '_gateway': '192.168.1.1'
                             }
        """
        params = OrderedDict(TokenNumber=self.__token)
        params.update(zip(['SSID', 'WPWD', 'NetMode', 'DHCPMode', 'SSIDHide'], [ssid, wpwd, 'wifi', wifinfo['_dhcp'].upper(), '1']))
        if params['DHCPMode'] == 'NO':
            for item in ['_ip', '_mask', '_gateway', '_dns']:
                params[item] = wifinfo.get(item)
        ret = msg_register('POST', 'Pboxwificonnect.cgi', 12)(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False
