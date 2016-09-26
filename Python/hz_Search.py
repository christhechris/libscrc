#!/usr/bin/env python
#-*- coding:utf-8 -*-  

import os
import re

from hzRegex import *
from hzFiles import *
from hzExcel import *
from hzMainWindow import *

dlg = None

def main(msgList):
	fileFolder = msgList[0]
	excelExport = msgList[1]
	regexFileEXT = msgList[2]
	regexFileName = msgList[3]
	regexKeyWords = msgList[4]

	excel = hzExcel(excelExport)
	excel.getInfo()
	# excel.writeRow("hello,ok,error,1234",0,1,1);
	# excel.save()

	hzFilesList = hzFiles(fileFolder,debug = True)
	fileList = hzFilesList.getFilterFilesEXT(regexFileEXT)

	matchs = list(hzFilesList.getFileApproximateMatch("*.[c,h]"))
	print ('%d match' % len(matchs))
	# for match in matchs:
	# 	print (match)
		
	print ("*****************************************************************")
	lineNum = []
	excelStartRow = 1

	for fileObj in fileList:
		regexRule = hzRegex()
		if regexRule.getRegexFileName(regexFileName, os.path.basename(fileObj)) :
			#print(fileObj)
			infoLists = hzFilesList.findStringFromFile(fileObj, regexKeyWords)
			# hzFilesList.grepStringFromFile(fileObj, regexKeyWords)
			# print (len(infoLists[0]), len(infoLists))
			for i in range(len(infoLists[0])) :
				# excel.writeRow( "%d"%excelStartRow + "#" + \
				# 				os.path.basename(fileObj) + "#" + \
				# 				str(infoLists[0][i]) + "#" + \
				# 				"OK"+ "#" + \
				# 				str(infoLists[1][i]) + "#" + \
				# 				str(infoLists[2][i]) \
				# 				,0,excelStartRow,1);
				excelStartRow += 1			
			excel.save()

			if infoLists :
				lineNum.extend(infoLists[0])
	print ("Check items = %d"%len(lineNum))
	print ("Total files = %d"%hzFilesList.count)
	
	# global dlg
	# dlg.signeltableWidgetUpdate([["File EXT.",str(len(fileList))],
	# 							 ["Grep RET.",str(len(lineNum))],
	# 							 ["Total Files",str(hzFilesList.count)]])
	#os.system("pause")

if __name__ == '__main__':
    	
	main(["D:\\AIS_INV_CAN\\13_SWC\\02_ソースコード",
		  "D:\\pythonTools\\abc.xls",
		  ".c | .h",
		  "DTC_|CAN_",
		  "DMCU_1BIT_SIFT"])

	# app = QApplication(sys.argv)
	# dlg = hzMainWindowsDlg()
	# dlg.signelConnectStartBtn(main)
	# dlg.show()
	# sys.exit(app.exec_())	
