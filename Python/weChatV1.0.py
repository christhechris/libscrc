# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  weChat
# History:  2016-09-24

import os
import re
import sys
import time
import json
import urllib
import urllib.request
import urllib.parse
import cookies
import xml.dom.minidom

DEBUG = True

uuid = ''
tip = 0

base_uri = ''
redirect_uri = ''

skey = ''  
wxsid = ''  
wxuin = ''  
pass_ticket = ''  
deviceId = 'e000000000000000'  
BaseRequest = {}
ContactList = []
My = []

imagesPath = os.getcwd()+'/weixin.jpg'

def getUUID() :
	global uuid
	url = 'https://login.weixin.qq.com/jslogin'
	values = {
		'appid':'wx782c26e4c19acffb',
		'fun':'new',
		'lang':'zh_CN',
		'_':int(time.time())
	}
	request = urllib.request.Request(url=url,data=urllib.parse.urlencode(values).encode(encoding='UTF8'))
	response = urllib.request.urlopen(request)
	data = response.read().decode("UTF8")
	print (data)

	regx = 'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
	pm = re.search(regx,data)
	code = pm.group(1)
	uuid = pm.group(2)
	print (code, uuid)
		
	if code == '200' :
		return True
	return False

def show2DimensionCode():
	global tip

	url = 'https://login.weixin.qq.com/qrcode/' + uuid
	values = {
		't':'webwx',
		'_':int(time.time())
	}

	request = urllib.request.Request(url=url,data=urllib.parse.urlencode(values).encode(encoding='UTF8'))
	response = urllib.request.urlopen(request)
	tip = 1
	f = open(imagesPath,'wb')
	f.write(response.read())
	f.close()
	time.sleep(1)
	os.system('call %s' %imagesPath)

def isLoginSucess():
	global tip, base_uri, redirect_uri
	url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s'%(tip,uuid,int(time.time()))
	request = urllib.request.Request(url = url)
	response = urllib.request.urlopen(request)
	data = response.read().decode()
	print (data)

	regx = 'window.code=(\d+)'
	pm = re.search(regx,data)
	code = pm.group(1)

	if code == '201' :
		print('Scan QR code successfully!')
	elif code == '200' :
		print('Logining...')
		regx = 'window.redirect_uri="(\S+?)";'
		pm = re.search(regx, data)
		redirect_uri = pm.group(1) + '&fun=new'
		base_uri = redirect_uri[:redirect_uri.rfind('/')]
	elif code == '408' :
		print('Login Timeout!')

	return code

def login() :
	global skey, wxsid, wxuin, pass_ticket, BaseRequest
	request = urllib.request.Request(url = redirect_uri)
	response = urllib.request.urlopen(request)
	data = response.read()

	doc = xml.dom.minidom.parseString(data)
	root = doc.documentElement
	for node in root.childNodes :
		if node.nodeName == 'skey':
			skey = node.childNodes[0].data
		elif node.nodeName == 'wxsid':
			wxsid = node.childNodes[0].data
		elif node.nodeName == 'wxuin':
			wxuin = node.childNodes[0].data
		elif node.nodeName == 'pass_ticket':
			pass_ticket = node.childNodes[0].data
	# print ('skey: %s, wxsid: %s, wxuin: %s, pass_ticket: %s' % (skey, wxsid, wxuin, pass_ticket))

	if skey == '' or wxsid == '' or wxuin == '' or pass_ticket == '' :
		return False  

	BaseRequest = {
		'Uin': int(wxuin),
		'Sid': wxsid,
		'Skey': skey,
		'DeviceID': deviceId,
	}

	return True


def webwxinit() :
	url = base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (pass_ticket, skey, int(time.time()))
	params = {
		'BaseRequest': BaseRequest
	}

	request = urllib.request.Request(url = url, data = json.dumps(params).encode(encoding='UTF8'))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib.request.urlopen(request)
	data = response.read().decode()

	if DEBUG == True:
		f = open(os.getcwd() + '/webwxinit.json', 'wb')
		f.write(data.encode())
		f.close()

	global ContactList, My
	dic = json.loads(data)
	ContactList = dic['ContactList']
	My = dic['User']

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print (ErrMsg)

	Ret = dic['BaseResponse']['Ret']
	if Ret != 0 :
		return False
	return True

def webwxgetcontact():
    
	url = base_uri + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (pass_ticket, skey, int(time.time()))
	params = {
		'BaseRequest': BaseRequest
	}
	request = urllib.request.Request(url = url, data = json.dumps(params).encode(encoding='UTF8'))	
	# request = urllib.request.Request(url = url)
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib.request.urlopen(request)
	data = response.read().decode()

	if DEBUG == True:
		f = open(os.getcwd() + '/webwxgetcontact.json', 'wb')
		f.write(data.encode())
		f.close()

	dic = json.loads(data)
	MemberList = dic['MemberList']

	SpecialUsers = ['newsapp', 'fmessage', 'filehelper', 'weibo', 'qqmail', 'fmessage', 'tmessage', 'qmessage', 'qqsync', 'floatbottle', 'lbsapp', 'shakeapp', 'medianote', 'qqfriend', 'readerapp', 'blogapp', 'facebookapp', 'masssendapp', 'meishiapp', 'feedsapp', 'voip', 'blogappweixin', 'weixin', 'brandsessionholder', 'weixinreminder', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c', 'officialaccounts', 'notification_messages', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c', 'wxitil', 'userexperience_alarm', 'notification_messages']

	for i in range(len(MemberList) - 1, -1, -1) :
		Member = MemberList[i]
		if Member['VerifyFlag'] & 8 != 0 :
			MemberList.remove(Member)
		elif Member['UserName'] in SpecialUsers :
			MemberList.remove(Member)
		elif Member['UserName'].find('@@') != -1 :
			MemberList.remove(Member)
		elif Member['UserName'] == My['UserName'] :
			MemberList.remove(Member)

	return MemberList

def main():
	# cookie = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	# urllib2.install_opener(cookie)
	
	if getUUID()==False:
		print('Get uuid unsuccessfully!')
		return None

	show2DimensionCode()
	time.sleep(1)

	while isLoginSucess() !='200':
		pass

	print('Login successfully and delete QRCode!')
	os.remove(imagesPath)

	if login() == False :
		print('<ERROR> Login failure !!!')
		return

	if webwxinit() == False:
		print("<ERROR> Init wechat failure !!!")
		return

	MemberList = webwxgetcontact()
	MemberCount = len(MemberList)
	print ('Total = %d'%MemberCount)

	# print('Login successfully!')

if __name__=='__main__':
	print('Welcome to use weChat personnal version')
	print('Please click Enter key to continue......')
	main()
