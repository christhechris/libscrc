# -*- coding:utf8 -*-
""" WeChat """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  WeChat.
# History:  2016/11/21 V1.0.0[Heyn]

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]


import os
import re
import time
import json
import random
import urllib
import urllib.request
import urllib.parse
# pip install requests 2016-09-29
import requests
# import xml.dom.minidom
# import multiprocessing
# import platform


def catch_keyboard_interrupt(fnc):
    """catchKeyboardInterrupt"""
    def wrapper(*args):
        """Wrapper"""
        try:
            return fnc(*args)
        except KeyboardInterrupt:
            print('\n[*] Force the exit procedure')
    return wrapper


class WebWeChat(object):
    """Web WeChat."""

    def __str__(self):
        description = \
            "=========================\n" + \
            "[#] Web WeChat\n" + \
            "[#] Debug Mode: " + str(self.debug) + "\n" + \
            "[#] Uuid: " + self.uuid + "\n" + \
            "[#] Uin: " + str(self.uin) + "\n" + \
            "[#] Sid: " + self.sid + "\n" + \
            "[#] Skey: " + self.skey + "\n" + \
            "[#] DeviceId: " + self.deviceid + "\n" + \
            "[#] PassTicket: " + self.pass_ticket + "\n" + \
            "========================="
        return description

    def __init__(self):
        self.debug = False
        self.uuid = ''
        self.base_uri = ''
        self.redirect_uri = ''
        self.uin = ''
        self.sid = ''
        self.skey = ''
        self.pass_ticket = ''
        self.deviceid = 'e' + repr(random.random())[2:17]
        self.baserequest = {}
        self.synckey = ''
        self.synckeylist = []
        self.user = []
        self.memberlist = []
        self.contactlist = []
        self.grouplist = []
        self.groupmemeberlist = []
        self.publicuserslist = []
        self.specialuserslist = []
        self.autoreplymode = True
        self.synchost = ''
        self.user_agent = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3)
                             AppleWebKit/537.36 (KHTML, like Gecko)
                             Chrome/48.0.2564.109 Safari/537.36"""
        self.interactive = True
        self.autoopen = False
        self.savefolder = os.path.join(os.getcwd(), 'saved')
        self.savesubfolders = {'webwxgeticon': 'icons',
                               'webwxgetheadimg': 'headimgs',
                               'webwxgetmsgimg': 'msgimgs',
                               'webwxgetvideo': 'videos',
                               'webwxgetvoice': 'voices',
                               '_showQRCodeImg': 'qrcodes'}

        self.appid = 'wx782c26e4c19acffb'
        self.lang = 'zh_CN'
        self.lastcheckts = time.time()
        self.membercount = 0
        self.specialusers = ['newsapp', 'fmessage', 'filehelper', 'weibo',
                             'qqmail', 'fmessage', 'tmessage', 'qmessage',
                             'qqsync', 'floatbottle', 'lbsapp', 'shakeapp',
                             'medianote', 'qqfriend', 'readerapp', 'blogapp',
                             'facebookapp', 'masssendapp', 'meishiapp', 'feedsapp',
                             'voip', 'blogappweixin', 'weixin', 'brandsessionholder',
                             'weixinreminder', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c',
                             'officialaccounts', 'notification_messages', 'wxid_novlwrv3lqwv11',
                             'gh_22b87fa7cb3c', 'wxitil', 'userexperience_alarm',
                             'notification_messages']

        self.timeout = 20  # (Unit:Second)
        self.media_count = -1
        self.qrcodepath = ''

    def getuuid(self):
        """Get UUID."""
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': self.appid,
            'fun': 'new',
            'lang': self.lang,
            '_': int(time.time()),
        }

        request = urllib.request.Request(
            url=url, data=urllib.parse.urlencode(params).encode(encoding='UTF-8'))
        response = urllib.request.urlopen(request)
        data = response.read().decode('UTF-8')
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        ret = re.search(regx, data)
        if ret:
            code = ret.group(1)
            self.uuid = ret.group(2)
            return code == '200'
        return False

    def genqrcode(self):
        """Get QR Code."""
        self._showqrcodeimage()

    def _showqrcodeimage(self):
        """Show QR code image."""
        url = 'https://login.weixin.qq.com/qrcode/' + self.uuid
        params = {
            't': 'webwx',
            '_': int(time.time())
        }

        request = urllib.request.Request(
            url=url, data=urllib.parse.urlencode(params).encode(encoding='UTF-8'))
        response = urllib.request.urlopen(request)
        data = response.read()

        self.qrcodepath = self._savefile('qrcode.jpg', data, '_showQRCodeImg')
        os.startfile(self.qrcodepath)

    def waitforlogin(self, tip=1):
        """Wait for login."""
        time.sleep(tip)
        url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
            tip, self.uuid, int(time.time()))
        data = self._get(url)
        ret = re.search('window.code=(\\d+)', data)
        code = ret.group(1)

        if code == '201':
            return True
        elif code == '200':
            ret = re.search('window.redirect_uri="(\\S+?)";', data)
            r_uri = ret.group(1) + '&fun=new'
            self.redirect_uri = r_uri
            self.base_uri = r_uri[:r_uri.rfind('/')]
            return True
        elif code == '408':
            self._echo('[Login timeout] \n')
        else:
            self._echo('[Landing abnormal] \n')
        return False

    def login(self):
        """WeChat login."""
        data = self._get(self.redirect_uri)
        doc = xml.dom.minidom.parseString(data)
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data

        if '' in (self.skey, self.sid, self.uin, self.pass_ticket):
            return False

        self.baserequest = {
            'Uin': int(self.uin),
            'Sid': self.sid,
            'Skey': self.skey,
            'DeviceID': self.deviceid,
        }
        return True

    def webwxinit(self):
        """Web WeChat Init."""
        url = self.base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            self.pass_ticket, self.skey, int(time.time()))
        params = {
            'BaseRequest': self.baserequest
        }
        dic = self._post(url, params)
        self.synckeylist = dic['SyncKey']
        self.user = dic['User']
        # synckey for synccheck
        self.synckey = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                 for keyVal in self.synckeylist['List']])

        return dic['BaseResponse']['Ret'] == 0

    def webwxstatusnotify(self):
        """Web WeChat Status Notify."""
        url = self.base_uri + \
            '/webwxstatusnotify?lang=zh_CN&pass_ticket=%s' % (self.pass_ticket)
        params = {
            'BaseRequest': self.baserequest,
            "Code": 3,
            "FromUserName": self.user['UserName'],
            "ToUserName": self.user['UserName'],
            "ClientMsgId": int(time.time())
        }
        dic = self._post(url, params)

        return dic['BaseResponse']['Ret'] == 0

    def webwxgetcontact(self):
        """Get Web WeChat Contact."""
        specialusers = self.specialusers
        print(self.base_uri)
        url = self.base_uri + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
            self.pass_ticket, self.skey, int(time.time()))
        params = {
            'BaseRequest': self.baserequest
        }
        dic = self._post(url, params)

        self.membercount = dic['MemberCount']
        self.memberlist = dic['MemberList']

        contactlist = self.memberlist[:]
        # GroupList = self.grouplist[:]
        # PublicUsersList = self.publicuserslist[:]
        # SpecialUsersList = self.specialuserslist[:]

        for i in range(len(contactlist) - 1, -1, -1):
            contact = contactlist[i]
            if contact['VerifyFlag'] & 8 != 0:
                contactlist.remove(contact)
                self.publicuserslist.append(contact)
            elif contact['UserName'] in specialusers:
                contactlist.remove(contact)
                self.specialuserslist.append(contact)
            elif contact['UserName'].find('@@') != -1:
                contactlist.remove(contact)
                self.grouplist.append(contact)
            # elif Contact['UserName'] == self.user['UserName']:
            #     contactlist.remove(Contact)
        self.contactlist = contactlist

        return True

    def webwxbatchgetcontact(self):
        """Web WeChat Batch Get Contact."""
        url = self.base_uri + \
            '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (
                int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.baserequest,
            "Count": len(self.grouplist),
            "List": [{"UserName": g['UserName'], "EncryChatRoomId":""} for g in self.grouplist]
        }
        dic = self._post(url, params)

        contactlist = dic['ContactList']
        # contactcount = dic['Count']
        self.grouplist = contactlist

        for i in range(len(contactlist) - 1, -1, -1):
            contact = contactlist[i]
            memberlist = contact['MemberList']
            for member in memberlist:
                self.groupmemeberlist.append(member)
        return True

    def _getuserid(self, name):
        for member in self.memberlist:
            if name == member['RemarkName'] or name == member['NickName']:
                return member['UserName']
        return None

    def _webwxsendmsg(self, word, to_user_name='filehelper'):
        url = self.base_uri + \
            '/webwxsendmsg?pass_ticket=%s' % (self.pass_ticket)
        clientmsgid = str(int(time.time() * 1000)) + \
            str(random.random())[:5].replace('.', '')
        params = {
            'BaseRequest': self.baserequest,
            'Msg': {
                "Type": 1,
                "Content": word,
                "FromUserName": self.user['UserName'],
                "ToUserName": to_user_name,
                "LocalID": clientmsgid,
                "ClientMsgId": clientmsgid
            }
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii=False).encode('utf8')
        ret = requests.post(url, data=data, headers=headers)
        dic = ret.json()
        return dic['BaseResponse']['Ret'] == 0

    def _run(self, infostr, func, *args):
        print(infostr, end='')
        if func(*args):
            print('Success')
        else:
            print('Failure\n[*] Exit the program')
            exit()

    def _echo(self, infostr):
        print(infostr)

    def _get(self, url, api=None):
        request = urllib.request.Request(url=url)
        request.add_header('Referer', 'https://wx.qq.com/')
        if api == 'webwxgetvoice':
            request.add_header('Range', 'bytes=0-')
        if api == 'webwxgetvideo':
            request.add_header('Range', 'bytes=0-')
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        return data

    def _post(self, url, params, jsonfmt=True):
        if jsonfmt:
            request = urllib.request.Request(
                url=url, data=json.dumps(params).encode(encoding='UTF-8'))
            request.add_header(
                'ContentType', 'application/json; charset=UTF-8')
        else:
            request = urllib.request.Request(
                url=url, data=urllib.parse.urlencode(params).encode(encoding='UTF-8'))
        response = urllib.request.urlopen(request)
        data = response.read().decode()

        # For debug.
        # fns = open(os.getcwd() + '/webwxgetcontact.json', 'wb')
        # fns.write(data.encode())
        # fns.close()

        if jsonfmt:
            return json.loads(data)
        return data

    def _savefile(self, filename, data, api=None):
        fns = filename
        if self.savesubfolders[api]:
            dirname = os.path.join(self.savefolder, self.savesubfolders[api])
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            fns = os.path.join(dirname, filename)
            with open(fns, 'wb') as file:
                file.write(data)
                file.close()
        return fns

    @catch_keyboard_interrupt
    def start(self):
        """Start."""
        self._echo('[*] Web WeChat ... Starting')
        while True:
            self._run('[*] Getting UUID ... ', self.getuuid)
            self._echo('[*] Getting QR Code ... Success')
            self.genqrcode()
            print('[*] Please use WeChat to scan QR code to login ... ')
            if not self.waitforlogin():
                print('[*] Please click on the phone to confirm ... ')
                continue
            if not self.waitforlogin(0):
                continue
            break

        os.remove(self.qrcodepath)

        self._run('[*] Logging in ... ', self.login)
        self._run('[*] Wechat initialization ... ', self.webwxinit)
        self._run('[*] Start status notify ... ', self.webwxstatusnotify)
        self._run('[*] Get contact ... ', self.webwxgetcontact)
        self._echo('[*] Due %s Contact， Read to Contacts %d' %
                   (self.membercount, len(self.memberlist)))
        self._echo('[*] Total %d Group | %d Contact | %d SpecialUsers ｜ %d PublicUsers' %
                   (len(self.grouplist),
                    len(self.contactlist),
                    len(self.specialuserslist),
                    len(self.publicuserslist)))
        self._run('[*] Get a group ... ', self.webwxbatchgetcontact)
        if self.debug:
            print(self)


    def sendmsg(self, name, word, isfile=False):
        """Send Message."""
        ids = self._getuserid(name)
        if ids:
            if isfile:
                with open(word, 'r') as file:
                    for line in file.readlines():
                        line = line.replace('\n', '')
                        self._echo('-> ' + name + ': ' + line)
                        if self._webwxsendmsg(line, ids):
                            print(' [Success]')
                        else:
                            print(' [Failure]')
                        time.sleep(1)
            else:
                if self._webwxsendmsg(word, ids):
                    pass
                    # print('[*] The message was sent successfully')
                else:
                    print('[*] Message delivery failed')
        else:
            print('[*] This user does not exist')
