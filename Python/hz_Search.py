#!/usr/bin/env python
#-*- coding:utf-8 -*-  

import os
import re

from hzRegex import *
from hzFiles import *
from hzExcel import *
from esdExcel import *
from hzMainWindow import *

dlg = None

def main(msgList):
	fileFolder = msgList[0]
	excelExport = msgList[1]
	regexFileEXT = msgList[2]
	regexFileName = msgList[3]
	regexKeyWords = msgList[4]

	excel = esdExcel(excelExport)

	hzAllFilesList = hzFiles(fileFolder,debug = False)
	fileList = hzAllFilesList.getFilterFilesEXT(regexFileEXT)

	matchs = list(hzAllFilesList.getFileApproximateMatch("*.[c,h]"))
	print ('%d Glob match' % len(matchs))
	# for match in matchs:
	# 	print (match)
		
	print ("#"*100)
	lineNum = []
	excelStartRow = 1
	testCount = 0
	for fileObj in fileList:
		regexRule = hzRegex()
		if regexRule.getRegexFileName(regexFileName, os.path.basename(fileObj)) :
			#print(fileObj)
			testCount += 1
			infoLists = hzAllFilesList.findStringFromFile(fileObj, regexKeyWords)
			# hzAllFilesList.grepStringFromFile(fileObj, regexKeyWords)
			# print (len(infoLists[0]), len(infoLists))
			for i in range(len(infoLists[0])) :
				# strMessage [excelFileName, functionName, keywordsLines, keywords]
				excel.writeExcelRow(os.path.basename(fileObj) + "#" + \
									str(infoLists[0][i]) + "#" + str(infoLists[1][i]) + "#" + \
									str(infoLists[2][i]),excelStartRow)

				# ret = excel.updateExcelRow(os.path.basename(fileObj) + "#" + \
				# 					str(infoLists[0][i]) + "#" + str(infoLists[1][i]) + "#" + \
				# 					str(infoLists[2][i]), excelStartRow)

				if (ret == True) :
					excelStartRow += 1
			excel.saveExcel()

			if infoLists :
				lineNum.extend(infoLists[0])
	print ("Check items = %d"%len(lineNum))
	print ("Files Regex = %d"%testCount)
	print ("Files EXT.  = %d"%len(fileList))
	print ("Total files = %d"%hzAllFilesList.count)
	
	# global dlg
	# dlg.signeltableWidgetUpdate([["File EXT.",str(len(fileList))],
	# 							 ["Grep RET.",str(len(lineNum))],
	# 							 ["Total Files",str(hzAllFilesList.count)]])
	#os.system("pause")

if __name__ == '__main__':
    	
	main(["D:\\AIS_INV_CAN\\13_SWC\\02_ソースコード",
		  "D:\\pythonTools\\abc.xls",
		  ".c",
		  "DGT_|CAN_",
		  "while"])

	# main(["D:\\test",
	# 	  "D:\\test\\abc.xls",
	# 	  ".c | .h",
	# 	  ".",
	# 	  "UART"])

	# app = QApplication(sys.argv)
	# dlg = hzMainWindowsDlg()
	# dlg.signelConnectStartBtn(main)
	# dlg.show()
	# sys.exit(app.exec_())	
