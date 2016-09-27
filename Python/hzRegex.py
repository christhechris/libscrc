# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn
# Program:  Regular
# History:  2016-09-04

import os
import re

class hzRegex :
	def __init__(self, debug = False) :
		super(hzRegex,self).__init__()
		self.debug = debug

	def getRegexAnotation(self, str) :
		''' Regular expression search.
		excluding : ://
		including : /* */ and //
		'''
		ret = re.search('([^:]//.*?$)|(/\*(.*?)\*/)|(\*(.*?)\*)', str, re.I)
		return ret

	def regexDeleAnotation(self, str) :
		''' Regular delete anotation.
		excluding : ://
		including : [/* */] & [//] & [/*]
		Notes:  
			2016-09-15 V1.0 [Heyn]
			2016-09-17 V1.1 [Heyn] 	Add: [/*] Regex = (/\*(.*?))
			2016-09-18 V1.2 [Heyn]  Bug: ([^:]//.*?$)  --> ([^:]?//.*?$)
		'''
		strMsg = re.sub('([^:]?//.*?$)|(/\*(.*?)\*/)|(\*(.*?)\*)|(/\*(.*?))', '',str).strip()
		if self.debug :
			print (strMsg)
		return strMsg

	def getRegexFileName(self, matchStr, str) :
		'''

		'''
		ret = re.search("^[A-Za-z0-9_]*" + matchStr, str, re.I)
		return ret
