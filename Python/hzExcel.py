# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn
# Program:  Excel
# History:  2016-09-18

import os
import sys
import xlrd

from xlutils.copy import copy
from xlwt import *

class hzExcel :
	__excelObj = None
	__excelObjCopy = None

	def __init__(self, filePath) :
		''' .
		Argument(s): 
					None
		Return(s): 
					None
		Notes: 
				2016-09-18 V1.0[Heyn]
		'''    		
		super(hzExcel,self).__init__()
		self.filePath = filePath
		self.isOpened = False

		try :
			if os.path.isfile(self.filePath) :
				fileName = os.path.basename(self.filePath)
				if fileName.split('.')[-1] == 'xls':
					self.__excelObj = xlrd.open_workbook(self.filePath, \
														 formatting_info = True)

					self.__excelObjCopy = copy(self.__excelObj)
					self.isOpened = True
		except Exception as e:
			self.__excelObj = None
			self.isOpened = False
			print (str(e))

	def settingMerged(self) :
		alignment = Alignment()
		alignment.horz = Alignment.HORZ_CENTER
		alignment.vert = Alignment.VERT_CENTER
		alignment.wrap = Alignment.WRAP_AT_RIGHT

		font = Font()
		font.name = 'Arial'
		# font.height = 300 # 15Point
		font.bold = False

		style = XFStyle()
		style.font = font
		style.alignment = alignment
		return style

	def getInfo(self) :
		''' .
		Argument(s): 
					None
		Return(s): 
					None
		Notes: 
				2016-09-18 V1.0[Heyn]
		'''    		
		if self.isOpened == True :
			for sheetname in self.__excelObj.sheet_names() :
				worksheet = self.__excelObj.sheet_by_name(sheetname)
				print('%s:(%d row,%d col).'%(sheetname,worksheet.nrows,worksheet.ncols))
		else :
			print ("File %s is not opened"%self.filePath)
	
	def readCell(self, sheetName = "sheet1", rown = 0, coln = 0) :
		''' Read file's a cell content.
		Argument(s): 
					None
		Return(s): 
					None
		Notes: 
				2016-09-18 V1.0[Heyn]
		''' 
		try :
			if self.isOpened == True :
				worksheets = self.__excelObj.sheet_names()
				if sheetName not in worksheets :
					print('%s is not exit.'%sheetName)
					return False
				worksheet = self.__excelObj.sheet_by_name(sheetName)
				cell = worksheet.cell_value(rown,coln)
				print('[sheet:%s,row:%s,col:%s]:%s.'%(sheetName,rown,coln,cell))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Read Cell is fail.")

	def readRow(self, sheetName = "sheet1", rown = 0) :
		''' Read file's a row content.
		Argument(s): 
					None
		Return(s): 
					None
		Notes: 
				2016-09-18 V1.0[Heyn]
		'''
		try :
			if self.isOpened == True :
				worksheets = self.__excelObj.sheet_names()
				if sheetName not in worksheets :
					print('%s is not exit.'%sheetName)
					return False
				worksheet = self.__excelObj.sheet_by_name(sheetName)
				row = worksheet.row_values(rown)
				print('[sheet:%s,row:%s]:%s.'%(sheetName,rown,row))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Read row is fail.")	
	
	def readCol(self, sheetName = "sheet1", coln = 0) :
		''' Read file's a col content.
		Argument(s): 
					None
		Return(s): 
					None
		Notes: 
				2016-09-18 V1.0[Heyn]
		'''
		try :
			if self.isOpened == True :
				worksheets = self.__excelObj.sheet_names()
				if sheetName not in worksheets :
					print('%s is not exit.'%sheetName)
					return False
				worksheet = self.__excelObj.sheet_by_name(sheetName)
				col = worksheet.col_values(coln)
				print('[sheet:%s,col:%s]:%s.'%(sheetName,coln,col))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Read row is fail.")

	
	def writeCell(self, value = '', sheetn = 0, rown = 0, coln = 0) :
		''' Write a cell to file,other cell is not change.
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  (Used Module) from xlutils.copy import copy
				2016-09-18 V1.0[Heyn]
		'''
		try :
			if self.isOpened == True :
				xlrd_objectc = copy(self.__excelObj)
				worksheet = xlrd_objectc.get_sheet(sheetn)
				worksheet.write(rown,coln,value)
				xlrd_objectc.save(self.filePath)
				print('writerow value:%s to [sheet:%s,row:%s,col:%s] is ture.'%(value,sheetn,rown,coln))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Write excel cell fail.")


	def writeRow(self, values = '', sheetn = 0, rown = 0, coln = 0) :
		''' Write a row to file, other row and cell is not change.
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  (Used Module) from xlutils.copy import copy
				2016-09-18 V1.0[Heyn]
		'''      		
		try :
			if self.isOpened == True :
				#xlrd_objectc = copy(self.__excelObj)
				#worksheet = xlrd_objectc.get_sheet(sheetn)
				worksheet = self.__excelObjCopy.get_sheet(sheetn)
				values = values.split('#')
				for value in values :
					worksheet.write(rown,coln,value,self.settingMerged())
					coln += 1
				#xlrd_objectc.save(self.filePath)
				print('writerow values:%s to [sheet:%s,row:%s,col:%s] is ture.'%(values,sheetn,rown,coln))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Write excel row fail.")
			
	def save(self) :
		self.__excelObjCopy.save(self.filePath)

	def writeCol(self, values = '', sheetn = 0, rown = 0, coln = 0) :
		''' Write a col to file, other col and cell is not change.
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  (Used Module) from xlutils.copy import copy
				2016-09-18 V1.0[Heyn]
		'''      		
		try :
			if self.isOpened == True :
				xlrd_objectc = copy(self.__excelObj)
				worksheet = xlrd_objectc.get_sheet(sheetn)
				values = values.split(',')
				for value in values :
					worksheet.write(rown,coln,value)
					rown += 1
				xlrd_objectc.save(self.filePath)
				print('writerow values:%s to [sheet:%s,row:%s,col:%s] is ture.'%(values,sheetn,rown,coln))
			else :
				print ("File %s is not opened"%self.filePath)
		except :
			print ("Write excel row fail.")			
			