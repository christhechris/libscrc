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

# (1) Limit all lines to a maximum of 79 characters


import json
import pprint
import string
import random
import argparse

from http.server import HTTPServer, BaseHTTPRequestHandler

import pandas as pd

class SiapServer:
    """ SIAP Server. """

    def __init__(self):
        self.__random = 1
        self.__jsondata = {}
        # self.alphabet = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0¡¢£¤¥¦§¨©ª«¬\xad®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþ'
        self.__alphabet = string.ascii_letters + string.digits
        self.__itemtype = ['BOOL', 'BYTE', 'WORD', 'DWORD', 'DOUBLE',
                           'FLOAT', 'INT16', 'INT32', 'STRING40']

        self.__randomdict = {'BOOL' : random.randrange(2),
                             'BYTE' : random.randint(-128, 127),
                             'WORD' : random.randint(0, 65535),
                             'DWORD' : random.randint(0, 2**32-1),
                             'INT16' : random.randint(-32768, 32767),
                             'INT32' : random.randint(-2**31, 2**31-1),
                             'FLOAT' : random.uniform(-2**128, 2**128),
                             'DOUBLE' : random.uniform(-2**256, 2**256-1),
                             'STRING40' : ''.join(random.choice(self.__alphabet) for i in range(random.randint(1, 40)))
                            }

        with open('SiapServerData.json') as ssd:
            self.__jsondata = json.loads(ssd.read())

        self.__value = pd.DataFrame(self.__jsondata['items'], columns=['itemName', 'value'])
        self.__types = pd.DataFrame(self.__jsondata['items'], columns=['itemName', 'itemType'])
        self.__random = self.__jsondata['random']

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
                self.__value.iloc[i].value = self.__randomdict[self.__types.iloc[i].itemType]
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
