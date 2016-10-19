# -*- coding:utf8 -*-
""" XiaoMi Router """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  XiaoMi Router Control.
# History:  V1.0.0 2016/10/18  [Router: R1D  ROM: 2.6.10]
#           V1.0.1 2016/10/19  New addredirect function

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import os
import re
import json
import time
import random
import logging
import platform
import requests
from Crypto.Hash import SHA


class MiWiFi:
    """XiaoMi Router"""

    def __init__(self, debugLevel=logging.WARNING):
        super(MiWiFi, self).__init__()
        self.host = '192.168.0.1'
        self.stok = None
        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)
        # logging.basicConfig(
        # level=debugLevel, format=formatopt, filemode='w',
        # filename='logging.log')

    def connect(self, host='localhost', pwdtext='admin'):
        """ Get MiWiFi Router token.
        Argument(s):
                    pwdtext : Mi Router's passwords.
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """
        self.host = host

        request = requests.get('http://' + self.host +
                               '/cgi-bin/luci/web/home')
        key = re.findall(r'key: \'(.*)\',', request.text)[0]
        mac = re.findall(r'deviceId = \'(.*)\';', request.text)[0]

        url = 'http://' + self.host + '/cgi-bin/luci/api/xqsystem/login'
        nonce = "0_" + mac + "_" + \
            str(int(time.time())) + "_" + str(random.randint(1000, 10000))
        pwd = SHA.new()
        pwd.update(pwdtext.encode() + key.encode())

        pwdsha = SHA.new()
        pwdsha.update(nonce.encode() + pwd.hexdigest().encode())
        pwdshahex = pwdsha.hexdigest()
        data = {
            "logtype": 2,
            "nonce": nonce,
            "password": pwdshahex,
            "username": "admin"
        }
        response = requests.post(url=url, data=data, timeout=5)
        resjson = json.loads(response.content.decode())
        if resjson['code'] == 0:
            self.stok = resjson['token']
            return True
        else:
            return False

    def addredirect(self, proto=1, sport=54321, dip='192.168.0.100', dport=12345):
        """ Add a port redirect to router.
        Argument(s):
                    proto : 1 = TCP PROTOCOL
                            2 = UDP PROTOCOL
                            3 = TCP/UDP PROTOCOL
                    sport : source port
                    dip   : destination ip
                    dport : destination port
        Return(s):
                    None
        Notes:
                    2016-10-19 V1.0.0[Heyn]
        """

        url = 'http://' + self.host + '/cgi-bin/luci/;stok=' + \
            self.stok + '/api/xqnetwork/add_redirect'

        data = {
            "name:" : 'Python',
            "proto" : proto,
            "sport" : sport,
            "ip"    : dip,
            "dport" : dport
        }
        response = requests.post(url=url, data=data, timeout=5)
        resjson = json.loads(response.content.decode())
        if resjson['code'] != 0:
            print('New redirect port failed.(code = %d)' % resjson['code'])
            return False

        # [WARNING] Failed to parse headers
        # url = 'http://' + self.host + '/cgi-bin/luci/;stok=' + \
        #     self.stok + '/api/xqnetwork/redirect_apply'
        # applyjson = json.loads(requests.get(url).content.decode())
        # if applyjson['code'] != 0:
        #     return False

        print('New redirect port success.')
        return True

    def reboot(self):
        """ Reboot MiWiFi Router.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        url = 'http://' + self.host + '/cgi-bin/luci/;stok=' + \
            self.stok + '/api/xqsystem/reboot?client=web'
        try:
            rebootjson = json.loads(requests.get(
                url, timeout=5).content.decode())
            if rebootjson['code'] == 0:
                print('Rebooting...')
            else:
                print('Reboot failed!')
        except BaseException:
            print('Reboot failed!')

    def status(self):
        """ Get MiWiFi Router Status.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        url = 'http://' + self.host + '/cgi-bin/luci/;stok=' + \
            self.stok + '/api/misystem/status'
        strjson = requests.get(url, timeout=5).content.decode()
        try:
            statusjson = json.loads(strjson)
            devlist = statusjson['dev']
            cpuhz = statusjson['cpu']['hz']
            print('[CPU]: ' + cpuhz +
                  '(' + str(statusjson['cpu']['core']) + ' CORE)')
            print('[MAC]: ' + statusjson['hardware']['mac'])
            print('[MEM]: ' + statusjson['mem']['type'] + ' Total: ' + statusjson['mem']
                  ['total'] + '  Usage:' + str(statusjson['mem']['usage'] * 100) + '% \n')
            print('--------------------[DEV]----------------------')
            for dev in devlist:
                print(dev['mac'] + ' ' + dev['devname'])
        except BaseException:
            print('Get status failed!')

    def wlaninfo(self):
        """ Get MiWiFi WLan Information.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        url = 'http://' + self.host + '/cgi-bin/luci/;stok=' + \
            self.stok + '/api/xqnetwork/wan_info'
        try:
            wlanjson = json.loads(requests.get(
                url, timeout=5).content.decode())
            print('\n--------------------[WAN]----------------------')
            print('IP:  ' + wlanjson['info']['ipv4'][0]['ip'])
            print('GW:  ' + wlanjson['info']['gateWay'])
            print('DNS: ' + wlanjson['info']['dnsAddrs'])
        except BaseException:
            print('Get status failed!')

    def ping(self):
        """Ping command."""

        if platform.system() == 'Windows':
            cmd = ["ping", "-{op}".format(op='n'), "1", self.host]
        else:
            cmd = ["ping", "-{op}".format(op='c'), "1", self.host]

        output = os.popen(" ".join(cmd)).readlines()
        for line in list(output):
            if not line:
                continue
            if str(line).upper().find("TTL") >= 0:
                return True
        return False

if __name__ == '__main__':

    MI = MiWiFi()

    while True:
        try:
            if MI.ping() is True:
                if MI.connect('192.168.0.1', 'psdcd2016'):
                    MI.reboot()
                    # MI.addredirect(1, 55555, '192.168.0.222', 12345)
                    time.sleep(20)
                    # break
            else:
                print('Waiting......')
                time.sleep(30)
        except KeyboardInterrupt:
            import sys
            sys.exit(1)
