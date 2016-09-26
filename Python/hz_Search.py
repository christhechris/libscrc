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

	hzAllFilesList = hzFiles(fileFolder,debug = False)
	fileList = hzAllFilesList.getFilterFilesEXT(regexFileEXT)

	matchs = list(hzAllFilesList.getFileApproximateMatch("*.[c,h]"))
	print ('%d Glob match' % len(matchs))
	# for match in matchs:
	# 	print (match)
		
	print ("#"*100)
	lineNum = []
	excelStartRow = 1

	for fileObj in fileList:
		regexRule = hzRegex()
		if regexRule.getRegexFileName(regexFileName, os.path.basename(fileObj)) :
			#print(fileObj)
			infoLists = hzAllFilesList.findStringFromFile(fileObj, regexKeyWords)
			hzAllFilesList.grepStringFromFile(fileObj, regexKeyWords)
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
	print ("Files EXT.  = %d"%len(fileList))
	print ("Total files = %d"%hzAllFilesList.count)
	
	# global dlg
	# dlg.signeltableWidgetUpdate([["File EXT.",str(len(fileList))],
	# 							 ["Grep RET.",str(len(lineNum))],
	# 							 ["Total Files",str(hzAllFilesList.count)]])
	#os.system("pause")

if __name__ == '__main__':
    	
	# main(["D:\\AIS_INV_CAN\\13_SWC\\02_ソースコード",
	# 	  "D:\\pythonTools\\abc.xls",
	# 	  ".c | .h",
	# 	  "DTC_|CAN_",
	# 	  "DMCU_1BIT_SIFT"])

	main(["D:\\test",
		  "D:\\test\\abc.xls",
		  ".c | .h",
		  ".",
		  "UART"])

	# app = QApplication(sys.argv)
	# dlg = hzMainWindowsDlg()
	# dlg.signelConnectStartBtn(main)
	# dlg.show()
	# sys.exit(app.exec_())	
