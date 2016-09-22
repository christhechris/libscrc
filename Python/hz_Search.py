#!/usr/bin/env python
#-*- coding:utf-8 -*-  

import os
import re

from hzRegex import *
from hzFiles import *
from hzExcel import *

def main():
	fileDir = "D:\\test"#D:\\MySrc\\Hz\\Hobe"
	regexFileName = "*uart*"
	regex   = "uart"

	excel = hzExcel("D:\\test\\abc.xls")	
	excel.getInfo()
	# excel.writeRow("hello,ok,error,1234",0,1,1);
	# excel.save()

	hzFilesList = hzFiles(fileDir,debug = True)
	fileList = hzFilesList.getFilterFilesForTuple(('.c'))
	#matchs = list(hzFilesList.getFileApproximateMatch(regexFileName))
	#print ('%d match' % len(matchs))
	#for match in matchs:
	#	print (match)
		
	print ("*****************************************************************")
	lineNum = []
	excelStartRow = 1

	for fileObj in fileList:
		regexRule = hzRegex()
		if regexRule.getRegexFileName("uart", os.path.basename(fileObj)) :
			#print(fileObj)
			infoLists = hzFilesList.findStringFromFile(fileObj, regex)
			# print (len(infoLists[0]), len(infoLists))
			for i in range(len(infoLists[0])) :
				excel.writeRow( "%d"%excelStartRow + "#" + \
								os.path.basename(fileObj) + "#" + \
								str(infoLists[0][i]) + "#" + \
								"OK"+ "#" + \
								str(infoLists[1][i]) + "#" + \
								str(infoLists[2][i]) \
								,0,excelStartRow,1);
				excelStartRow += 1			
			excel.save()

			if infoLists :
				lineNum.extend(infoLists[0])
	print ("Check items = %d"%len(lineNum))
	print ("Total files = %d"%hzFilesList.count)
	#os.system("pause")

if __name__ == '__main__':
	main()
