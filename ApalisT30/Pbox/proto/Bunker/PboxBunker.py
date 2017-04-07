# -*- coding:UTF-8 -*-
""" PboxBunker """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  Http For Bunker.
# History:  2017/03/23 V1.0.0[Heyn]
#

import json
import requests

class PboxBunker:
    """Pbox http for bunker"""

    def __init__(self, ip='127.0.0.1', port=8080, timeout=3):
        super(PboxBunker, self).__init__()
        self.sess = requests.session()
        self.port = port
        self.timeout = timeout
        self.itemsurl = 'http://' + ip + ':%d/PBox/dataitems'%port
        self.errorurl = 'http://' + ip + ':%d/PBox/error'%port
        self.datasurl = 'http://' + ip + ':%d/PBox/get'%port
        print('[Http Bunker] Bunker IP Address = %s:%d'%(ip, port))

    def __del__(self):
        pass

    def getitems(self):
        """Get bunker items type."""

        try:
            items = self.sess.get(self.itemsurl, timeout=self.timeout)
            dictitems = json.loads(items.text, encoding='UTF-8')
        except BaseException as err:
            print('Get bunker items [%s]'%err)
            return None
        else:
            # print(dictitems)
            pass

        return dictitems

    def getdata(self):
        """Get bunker data value."""

        try:
            items = self.sess.get(self.datasurl, timeout=self.timeout)
            dictitems = json.loads(items.text, encoding='UTF-8')
        except BaseException:
            print('Get bunker data error.')
            return None
        else:
            # print(dictitems)
            pass

        return dictitems

    def posterror(self, num):
        """Post error message to bunker"""
        errdict = dict(errorCode=num)
        try:
            ret = self.sess.post(self.errorurl, data=json.dumps(errdict), timeout=self.timeout)
        except BaseException:
            print('Get bunker data error.')
            return None
        else:
            print(ret.text)
        return ret.text


# if __name__ == "__main__":
#     BUNKER = PboxBunker('192.168.3.103', 8080, 10)
#     # print(BUNKER.getitems())
#     # print(BUNKER.getdata())
#     # print(BUNKER.posterror(1000))
