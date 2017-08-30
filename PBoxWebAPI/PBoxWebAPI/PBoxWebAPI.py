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

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import re
import json
import hashlib
import logging
import collections

import requests
from prettytable import  PrettyTable

ERROR_CODE = 'ERROR'
SUCCESS_CODE = 'SUCCESS'

def catch_exception(origin_func):
    """Catch exception."""
    def wrapper(self, *args, **kwargs):
        """Wrapper."""
        try:
            return origin_func(self, *args, **kwargs)
        except BaseException as msg:
            print('[ERROR] %s an exception raised. *** %s ***'%(origin_func, str(msg)))
            return False
    return wrapper

@catch_exception
def msg_register(method, cgi):
    """Message register"""
    # pylint: disable=C0301
    def decorator(func):
        """Decorator."""
        def wrapper(self, *args, **kwargs):
            """Wrapper."""
            payload = func(self, *args, **kwargs)
            header = {'Content-Type':'application/x-www-form-urlencoded'}
            if payload is not False and method == 'POST':
                # 2017-08-01 for https verify = False
                ret = self.sess.post(self.url + cgi,
                                     data=payload,
                                     headers=header,
                                     timeout=5,
                                     verify=False)
            elif payload is not False and method == 'GET':
                # 2017-08-01 for https verify = False
                ret = self.sess.get(self.url + cgi, headers=header, timeout=3, verify=False)
            else:
                return ERROR_CODE

            result = dict(result=ERROR_CODE, status='404', detail='')
            if ('Response [200]' in str(ret)) and ((SUCCESS_CODE in ret.text) or (ERROR_CODE not in ret.text)):
                if ret.text.strip():
                    result['status'] = '0' if SUCCESS_CODE in ret.text else (lambda x: '0' if 'status' not in x.keys() else x['status'])(json.loads(ret.text))
                    result['result'] = ERROR_CODE if result['status'] != '0' else SUCCESS_CODE
                    result['detail'] = ret.text if SUCCESS_CODE in ret.text else json.loads(ret.text)
                else:
                    result['result'] = SUCCESS_CODE
                    result['status'] = '0'
                    result['detail'] = ''

                if result['result'] == ERROR_CODE:
                    logging.error('Function = %s()  %s', func, result)
            else:
                logging.error('Function = %s ret = %s, text = %s', func, ret, str(ret.text).strip('\n'))

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

class PBoxWebAPI:
    """PBox WebMc API Class."""
    # pylint: disable=C0301
    # pylint: disable=too-many-instance-attributes

    def __init__(self, url='http://192.168.3.111', debugLevel=logging.ERROR):
        self.url = url + '/cgi-bin/'
        requests.packages.urllib3.disable_warnings()    # 2017-08-01 for https verify = False
        self.sess = requests.session()
        self.__token = '200'
        self.username = self.password = self.passwordmd5 = 'admin'
        self.pboxinfo = None
        self.jcid = self.jdid = dict(id='0') # JSON Channel ID & JSON Device ID.

        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)

    @msg_register('POST', 'Login.cgi')
    def __logininit(self, username='admin', password='admin'):
        """Login."""

        pwdmd5 = hashlib.md5()
        pwdmd5.update(password.encode('UTF-8'))
        params = collections.OrderedDict()
        params['UserName'] = self.username = username
        params['PassWord'] = self.passwordmd5 = pwdmd5.hexdigest()
        return params

    @msg_register('POST', 'Verifypasswd.cgi')
    def __loginverify(self):
        """Login Verify"""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['UserName'] = self.username
        params['PassWord'] = self.passwordmd5
        return params

    @catch_exception
    def login(self, url='http://192.168.3.111', username='admin', password='admin'):
        """ WebMc Login
            2017-08-03 V1.2 [Heyn] New url params
        """
        self.url = url + '/cgi-bin/'
        ret = self.__logininit(username=username, password=password)
        if ERROR_CODE in ret.get('result', ERROR_CODE):
            return False

        self.__token = ret['detail']['token']
        if ERROR_CODE in self.__loginverify().get('result', ERROR_CODE):
            return False

        # Get PBox Configure Information.
        ret = msg_register('GET', 'Pboxgetsetupinfo.cgi')(lambda x, y: y)(self, None)
        if SUCCESS_CODE in ret.get('result', ERROR_CODE):
            self.pboxinfo = ret.get('detail')
            self.jcid = dict(id=self.pboxinfo.get('pboxsetup', {}).get('model', {}).get('_id', '0'))
            self.jdid = dict(id=self.pboxinfo.get('pboxsetup', {}).get('model', {}).get('device', {}).get('_id', '0'))

        logging.info('PBox Channel ID %s', self.jcid)
        logging.info('PBox Devices ID %s', self.jdid)
        return True

    @catch_exception
    def newchannel(self, items, freq=10000, name='default', flag=True):
        """ PBox new a channel.
        Items params:
            ['Modbus-RTU', '/dev/ttymxc1', '9600', 'None', '8', '1', '1000']
            ['Modbus-TCP', '192.168.3.1', '54321', '1000']
            ['Panasert-COM', '/dev/ttymxc1', '4800', 'None', '7', '1', '1000', '0']
            ['Panasert-TCP', '192.168.3.1', '54321', '1000']
            ['Siap', '192.168.3.1', '54321', '10000']
        """

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
        Items params:
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
        params = collections.OrderedDict(TokenNumber=self.__token)
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
        """PBox Alter Device Name."""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['DeviceName'] = name
        params['ChannelID'] = self.jcid['id']
        params['DeviceID'] = self.jdid['id']
        ret = msg_register('POST', 'AlterDevice.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def delchannel(self):
        """PBox Delete Channel"""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['DelChannelID'] = self.jcid['id']
        ret = msg_register('POST', 'DeleteChannel.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def deldevice(self):
        """Delete Device."""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['DelChannelID'] = self.jcid['id']
        params['DelDeviceID'] = self.jdid['id']
        ret = msg_register('POST', 'DeleteDevice.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def newitem(self, items):
        """ PBox New Item
            eg.
            Modbus RTU : item=['python', 'test', '5000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0']
        """
        params = [self.__token, self.jdid['id']]
        params.extend(items)

        ret = msg_register('POST', 'AddDataitem.cgi')(lambda x, y: '&'.join(y))(self, list(map(lambda x: 'item=%s'%x, params)))
# +-----------------------------------------------------------------------------------------------+
#                                   True & False Table
#                                 -----------------------
#       [WebMc] : Error=0   OK=1    [Name] : Digital=1 Char=0   [Alias] : Digital=1 Char=0
#
# +----------------------+--------+----------------------+--------+----------------------+--------+
# | WebMc | Name | Alias | Result | WebMc | Name | Alias | Result | WebMc | Name | Alias | Result |
# +----------------------+--------+----------------------+--------+----------------------+--------+
# |   0   |   0  |   0   |  False |   0   |   0  |   1   |  True  |   0   |   1  |   0   |  True  |
# +----------------------+--------+----------------------+--------+----------------------+--------+
# |   0   |   1  |   1   |  True  |   1   |   0  |   0   |  True  |   1   |   0  |   1   |  False |
# +----------------------+--------+----------------------+--------+----------------------+--------+
# |   1   |   1  |   0   |  False |   1   |   1  |   1   |  False |       |      |       |        |
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
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['LoadDataUp'] = '1'
        ret = msg_register('POST', 'LoadData.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def newpassword(self, newpassword='000000'):
        """Change Password"""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['OldPassword'] = self.password
        md5 = hashlib.md5()
        md5.update(newpassword.encode('UTF-8'))
        params['NewPassword'] = self.passwordmd5 = md5.hexdigest()
        params['ConfirmPassword'] = self.passwordmd5
        ret = msg_register('POST', 'PasswordConfig.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def lanipaddress(self, ipaddr='192.168.3.222'):
        """Change LAN IP Address."""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['IPAddress'] = ipaddr
        ret = msg_register('POST', 'LocalIPConfig.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def wanipaddress(self, dhcp='YES', ipaddr='192.168.3.77', netmask='255.255.255.0', gateway='192.168.3.1'):
        """Change WAN IP Address."""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['NetMode'] = 'gateway'
        params['DHCPMode'] = dhcp.upper()
        if dhcp.upper() == 'NO':
            params['IPAddress'] = ipaddr
            params['SubnetMask'] = netmask
            params['Gateway'] = gateway
            params['DNSAddress'] = '8.8.8.8'

        ret = msg_register('POST', 'IPConfig.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def netswitch(self, mode='gateway'):
        """Switch gateway 4G or wifi."""
        params = collections.OrderedDict(TokenNumber=self.__token)
        params['NetMode'] = params['ModeType'] = mode if mode in ('gateway', '4G', 'wifi') else 'gateway'
        ret = msg_register('POST', 'SwitchInfo.cgi')(lambda x, y: y)(self, params)
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @catch_exception
    def reboot(self):
        """Exec configuration."""
        ret = msg_register('POST', 'RebootArm.cgi')(lambda x, y: y)(self, collections.OrderedDict(TokenNumber=self.__token, restart='restart'))
        return True if SUCCESS_CODE in ret.get('result', ERROR_CODE) else False

    @msg_register('POST', 'RefreshDataitem.cgi')
    def __siap(self):
        """SIAP DataItems."""
        return collections.OrderedDict(TokenNumber=self.__token, item='liaoCang')

    @msg_register('POST', 'Pboxgetseriadata.cgi')
    def __panasert(self):
        """Panasonic Sert DataItems."""
        return collections.OrderedDict(TokenNumber=self.__token, item='panasert')

    @catch_exception
    def get_siap(self):
        """Get SIAP DataItems."""
        dataitems = self.__siap()
        return dataitems['detail'] if SUCCESS_CODE in dataitems.get('result', ERROR_CODE) else []

    @catch_exception
    def get_pansert(self):
        """Get Panasonic Sert(TCP) DataItems."""
        dataitems = self.__panasert()
        return dataitems['detail'] if SUCCESS_CODE in dataitems.get('result', ERROR_CODE) else []
