# -*- coding:utf-8 -*-
""" PBox SIAP """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  SIAP Protocol.
# History:  2017/03/23 V1.0.0 [Heyn]
#           2017/12/14 V1.1.0 [Heyn] Optimization code.
#           2017/12/15 V1.1.1 [Heyn] pyinstall --onefile PBoxSIAPc.py --icon **.ico
#                                    ./PBoxSIAPc.exe -i 127.0.0.1 -p 54321 -f 5 -t 3

import time
import json
import pprint
import argparse
import requests


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
            return result
        return wrapper
    return decorator

class PBoxSIAP:
    """PBox protocol for SIAP"""

    def __init__(self, ip='127.0.0.1', port=8080, timeout=3):
        self.sess = requests.session()
        self.port = int(port)
        self.timeout = int(timeout)

        self.__datasurl = 'http://{0}:{1}/PBox/get'.format(ip, self.port)
        self.__errorurl = 'http://{0}:{1}/PBox/error'.format(ip, self.port)
        self.__itemsurl = 'http://{0}:{1}/PBox/dataitems'.format(ip, self.port)

        print('[SIAP] Server IP Address = %s:%d'%(ip, self.port))

    @catch_exception
    @msg_register('GET')
    def itemstypes(self):
        """ Get items types from server. """
        return (self.__itemsurl, '')

    @catch_exception
    @msg_register('GET')
    def getdata(self):
        """ Get data value from server. """
        return (self.__datasurl, '')

    @catch_exception
    @msg_register('POST')
    def posterror(self, num):
        """Post error message to server"""
        return (self.__errorurl, json.dumps(dict(errorCode=num)))

def main(args):
    """ Main. """
    siap = PBoxSIAP(args.ipaddr, args.port, args.timeout)
    pprint.pprint(siap.itemstypes())
    freq = int(args.frequency)

    while True:
        pprint.pprint(siap.getdata())
        time.sleep(freq)
        if freq == 0:
            break
    print(siap.posterror(1000))

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-t', '--timeout', default=3, required=False)
    PARSER.add_argument('-p', '--port', help='SIAP Server Port.', required=True)
    PARSER.add_argument('-i', '--ipaddr', help='SIAP Server IP.', required=True)
    PARSER.add_argument('-f', '--frequency', default=0, help='Frequency.', required=False)

    ARGS = PARSER.parse_args()
    main(ARGS)
