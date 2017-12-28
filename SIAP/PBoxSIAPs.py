# -*- coding:utf-8 -*-
""" PBox SIAP Server """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  SIAP Server.
# History:  2017/01/19 V1.0.0 [Heyn]
#           2017/10/11 V1.0.1 [Heyn]
#           2017/12/22 V1.1.0 [Heyn] Optimization code.
#           2017/12/26 V1.1.1 [Heyn] pyinstall --onefile PBoxSIAPs.py --icon **.ico
#                                    ./PBoxSIAPs.exe -i 127.0.0.1
#           2017/12/28 V1.1.2 [Heyn] Optimization code.


# (1) Limit all lines to a maximum of 79 characters


import json
import pprint
import string
import random
import argparse

from http.server import HTTPServer, BaseHTTPRequestHandler

import pandas as pd
from faker import Faker

class SiapServer:
    """ SIAP Server. """

    def __init__(self):
        self.__random = 1
        self.__jsondata = {}
        self.__fake = Faker('en_US')
        self.__randomtypes, self.__randomvalue = [], []
        self.__alphabet = string.ascii_letters + string.digits
        self.__itemtype = ['BOOL', 'BYTE', 'WORD', 'DWORD', 'DOUBLE',
                           'FLOAT', 'INT16', 'INT32', 'STRING40']
        self.__randomdict = {'BOOL' : lambda : random.randrange(2),
                             'BYTE' : lambda : random.randint(-128, 127),
                             'WORD' : lambda : random.randint(0, 65535),
                             'DWORD' : lambda : random.randint(0, 2**32-1),
                             'INT16' : lambda : random.randint(-32768, 32767),
                             'INT32' : lambda : random.randint(-2**31, 2**31-1),
                             'FLOAT' : lambda : self.__fake.pyfloat,
                             'DOUBLE' : lambda : random.uniform(-2**256, 2**256-1),
                            #  'STRING40' : lambda : self.__fake.binary(length=40).decode('UTF-8', 'ignore'),
                             'STRING40' : lambda : self.__fake.pystr(min_chars=1, max_chars=40)
                            }
        self.__titletypes = ['itemName', 'itemType']
        self.__titlevalue = ['itemName', 'value']
        try:
            with open('SiapServerData.json') as ssd:
                self.__jsondata = json.loads(ssd.read())

            self.__random = self.__jsondata['random']
            if self.__random == 0:
                self.__value = pd.DataFrame(self.__jsondata['items'], columns=self.__titlevalue)
                self.__types = pd.DataFrame(self.__jsondata['items'], columns=self.__titletypes)
            else:
                _typesize = len(self.__jsondata['randomType'])
                for index in range(self.__jsondata['maxItems']):
                    _itemname = 'PYTHON{0}'.format(index)
                    self.__randomtypes.append(dict(itemName=_itemname,
                                                   itemType=self.__jsondata['randomType'][index%_typesize]))
                    self.__randomvalue.append(dict(itemName=_itemname, value=''))
                self.__types = pd.DataFrame(self.__randomtypes, columns=self.__titletypes)
                self.__value = pd.DataFrame(self.__randomvalue, columns=self.__titlevalue)
        except BaseException as err:
            self.__random = 1
            self.__types = pd.DataFrame([dict(itemName='PYRANDOM00',
                                              itemType='STRING40')], columns=self.__titletypes)
            self.__value = pd.DataFrame([dict(itemName='PYRANDOM00',
                                              value='JSON  ERROR')], columns=self.__titlevalue)
            print(err)

    def __generate_items(self):
        """ Generate Items Types. """

        payload = dict(items=[])
        for i in range(self.__types.count()['itemName']):
            payload['items'].append(self.__types.iloc[i].to_dict())
        pprint.pprint(payload)
        return str(json.dumps(payload)).encode()

    def __generate_value(self):
        """ Generate Items Value. """
        payload = dict(items=[])
        for i in range(self.__value.count()['itemName']):
            if self.__random != 0:
                self.__value.iloc[i].value = self.__randomdict[self.__types.iloc[i].itemType]()
            payload['items'].append(self.__value.iloc[i].to_dict())
        pprint.pprint(payload)
        return str(json.dumps(payload)).encode()

    def process(self, cmd):
        """ Process Url. """

        if 'PBox/dataitems' in cmd:
            ret = self.__generate_items()
        elif 'PBox/get' in cmd:
            ret = self.__generate_value()
        else:
            ret = '[ERROR] url (ex.: https://ip:port/PBox/dataitems or get)'
        return ret

class MyHttpHandler(BaseHTTPRequestHandler, SiapServer):
    """ Panasonic SIAP Server. """
    def __init__(self, request, client_address, server):
        SiapServer.__init__(self)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def __response(self, msg):
        try:
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(msg)
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        """POST"""
        datas = self.rfile.read(int(self.headers['content-length']))
        pprint.pprint(datas.decode('UTF-8'))
        self.__response(datas)

    def do_GET(self):
        """ Override """
        self.__response(self.process(self.path))


def main(args):
    """ Main. """
    httpd = HTTPServer((args.ipaddr, int(args.port)), MyHttpHandler)
    print('Server started on {0}, port {1}.....'.format(args.ipaddr, args.port))
    httpd.serve_forever()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-i', '--ipaddr', help='Server Local IP.', required=True)
    PARSER.add_argument('-p', '--port', default=8080, help='Server Listen Port.', required=False)

    ARGS = PARSER.parse_args()
    main(ARGS)
