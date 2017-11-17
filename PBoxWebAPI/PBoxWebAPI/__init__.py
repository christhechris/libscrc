# -*- coding:utf-8 -*-
""" PBox WebMc API """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PBox WebMc API.
# History:  2017-07-27 V1.0 [Heyn]
#           2017-08-07 Wheel Ver:0.0.6 [Heyn]
#           2017-08-24 Wheel Ver:0.1.0 [Heyn] New webdeldevice interface.
#           2017-08-25 Wheel Ver:0.1.1 [Heyn] New webpansert & websiap interface.
#           2017-09-07 Wheel Ver:1.0.1 [Heyn] New __getdriverinfo() \ __getbasicinfo()
#                                                 version() \ datetime()
#           2017-11-13 Wheel Ver:1.1.3 [Heyn] New webpboxinfo()
#           2017-11-17 Wheel Ver:1.2.2 [Heyn] New webwifi() websave() webload()

from .PBoxWebAPI import PBoxWebAPI
from .PBoxWebAPI import print_pretty

# pylint: disable=C0103, C0326

__all__ = ['weblogin', 'webnewchannel', 'webnewdevice', 'webnewitem',
           'webdelchannel', 'webdeldevice', 'webdelitems',
           'webalterchannel', 'webalterdevice', 'webalteritem',
           'webcloudaddress', 'webdownload', 'armreboot', 'webnewpassword',
           'weblanip', 'webwanip', 'webnet',
           'imageReport', 'webpansert', 'websiap', 'webconfpassword',
           'webversion', 'webdatetime', 'webupdate', 'webrecovery',
           'webpboxinfo', 'webwifi', 'websave', 'webload']

instanceList = []

def new_instance():
    newInstance = PBoxWebAPI()
    instanceList.append(newInstance)
    return newInstance

originInstance  = new_instance()

weblogin        = originInstance.login

webnewchannel   = originInstance.newchannel
webnewdevice    = originInstance.newdevice
webnewitem      = originInstance.newitem

webalterchannel = originInstance.alterchannel
webalterdevice  = originInstance.alterdevice
webalteritem    = originInstance.alteritem

webdelchannel   = originInstance.delchannel
webdeldevice    = originInstance.deldevice
webdelitems     = originInstance.delitems

webcloudaddress = originInstance.cloudaddress
webdownload     = originInstance.download2app
armreboot       = originInstance.reboot

weblanip        = originInstance.lanipaddress
webwanip        = originInstance.wanipaddress
webnet          = originInstance.netswitch

imageReport     = print_pretty

webpansert      = originInstance.get_pansert
websiap         = originInstance.get_siap

webnewpassword  = originInstance.newpassword
webconfpassword = originInstance.confpassword

webversion      = originInstance.version
webdatetime     = originInstance.datetime

webupdate       = originInstance.update
webrecovery     = originInstance.recovery

webpboxinfo     = originInstance.informations
webwifi         = originInstance.wifi
websave         = originInstance.save
webload         = originInstance.load
