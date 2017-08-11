# -*- coding:utf8 -*-
""" PBox WebMc API """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PBox WebMc API.
# History:  2017-07-27 V1.0 [Heyn]
#           2017-08-07 Wheel Ver:0.0.6 [Heyn]
#

from .PBoxWebAPI import PBoxWebAPI
from .PBoxWebAPI import print_pretty

instanceList = []

def new_instance():
    newInstance = PBoxWebAPI()
    instanceList.append(newInstance)
    return newInstance

originInstance = new_instance()

weblogin   = originInstance.login

webnewchannel   = originInstance.newchannel
webnewdevice    = originInstance.newdevice
webnewitem      = originInstance.newitem
webnewitems     = originInstance.newitems

webalterchannel = originInstance.alterchannel
webalterdevice  = originInstance.alterdevice
webalteritem    = originInstance.alteritem

webdelchannel   = originInstance.delchannel
webdelitems     = originInstance.delitems

webcloudaddress = originInstance.cloudaddress
webdownload     = originInstance.download2app
armreboot       = originInstance.reboot

webnewpassword  = originInstance.newpassword
weblanip        = originInstance.lanipaddress

imageReport     = print_pretty
