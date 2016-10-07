# -*- coding:utf8 -*-
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn
# Program:  Excel's read and write.
# History:  2016/09/18
#           2016/10/07 PEP 8 Code Style AND add logging

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]

import os
import sys
import xlrd
import logging

from xlutils.copy import copy
from xlwt import *

class hzExcel :
    __excelObj = None
    __excelObjCopy = None

    def __init__(self, filePath, debugLevel = logging.WARNING) :
        ''' .
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                2016-09-18 V1.0 [Heyn]
                2016-10-07 V1.1 [Heyn]
                Logging CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
        '''
        super(hzExcel,self).__init__()
        self.filePath = filePath
        self.isOpened = False

        try :
            if os.path.isfile(self.filePath) :
                fileName = os.path.basename(self.filePath)
                if fileName.split('.')[-1] == 'xls':
                    self.__excelObj = xlrd.open_workbook(self.filePath,
                    formatting_info = True)
                    self.__excelObjCopy = copy(self.__excelObj)
                    self.isOpened = True
                    logging.basicConfig(level = debugLevel)
                    # logging.basicConfig(filename='hzExcel.log',
                    #                     level = debugLevel)

        except Exception as e:
            self.__excelObj = None
            self.isOpened = False
            logging.critical(str(e))

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
                    xlsInfoLists -> [0] sheet name
                                    [1] rows number
                                    [2] coln number
        Notes:
                2016-09-18 V1.0.0[Heyn]
                2016-09-27 V1.0.1[Heyn] Add return
        '''
        xlsInfoLists = [[] for i in range(3)]    # [[], [], []]

        if self.isOpened is True :
            for sheetname in self.__excelObj.sheet_names() :
                worksheet = self.__excelObj.sheet_by_name(sheetname)
                xlsInfoLists[0].append(sheetname)
                xlsInfoLists[1].append(worksheet.nrows)
                xlsInfoLists[2].append(worksheet.ncols)
                logging.info('%s:(%d row,%d col).' %
                            (sheetname,
                            worksheet.nrows,
                            worksheet.ncols))
        else :
            logging.error("File %s is not opened"%self.filePath)
            return None
        return xlsInfoLists

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
            if self.isOpened is True :
                worksheets = self.__excelObj.sheet_names()
                if sheetName not in worksheets :
                    logging.error('%s is not exit.'%sheetName)
                    return False
                worksheet = self.__excelObj.sheet_by_name(sheetName)
                cell = worksheet.cell_value(rown,coln)
                logging.debug('[sheet:%s,row:%s,col:%s]:%s.' %
                     (sheetName,rown,coln,cell))
            else :
                logging.error("File %s is not opened"%self.filePath)
        except :
            logging.critical("Read excel cell failed.")

    def readRow(self, sheetName = "sheet1", rown = 0) :
        ''' Read file's a row content.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                2016-09-18 V1.0[Heyn]
        '''
        row = None
        try :
            if self.isOpened is True :
                worksheets = self.__excelObj.sheet_names()
                if sheetName not in worksheets :
                    logging.error('%s is not exit.'%sheetName)
                    return False
                worksheet = self.__excelObj.sheet_by_name(sheetName)
                row = worksheet.row_values(rown)
                logging.debug('[sheet:%s,row:%s]:%s.'%(sheetName,rown,row))
            else :
                logging.error("File %s is not opened"%self.filePath)
        except :
            logging.critical("Read excel row failed.")
        return row

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
            if self.isOpened is True :
                worksheets = self.__excelObj.sheet_names()
                if sheetName not in worksheets :
                    logging.error('%s is not exit.'%sheetName)
                    return False
                worksheet = self.__excelObj.sheet_by_name(sheetName)
                col = worksheet.col_values(coln)
                logging.debug('[sheet:%s,col:%s]:%s.'%(sheetName,coln,col))
            else :
                logging.error("File %s is not opened"%self.filePath)
        except :
            logging.critical("Read excel column failed.")

    def writeCell(self, value = '', sheetn = 0, rown = 0, coln = 0) :
        ''' Write a cell to file,other cell is not change.
        Argument(s):
                    [vale, sheetn, rown, coln]
        Return(s):
                    None
        Notes:  (Used Module) from xlutils.copy import copy
                2016-09-18 V1.0.0[Heyn]
                2016-09-27 V1.0.1[Heyn] Removed object copy and save
        '''
        try :
            if self.isOpened is True :
                worksheet = self.__excelObjCopy.get_sheet(sheetn)
                worksheet.write(rown,coln,value,self.settingMerged())
            else :
                logging.error("File %s is not opened"%self.filePath)
        except :
            logging.critical("Write excel cell failed.")

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
            if self.isOpened is True :
                worksheet = self.__excelObjCopy.get_sheet(sheetn)
                values = values.split('#')
                for value in values :
                    worksheet.write(rown,coln,value,self.settingMerged())
                    coln += 1
                logging.debug("Write row:%s to [sheet:%s,row:%s,col:%s]." %
                             (values,sheetn,rown,coln))
            else :
               logging.error("File %s is not opened"%self.filePath)
        except :
            logging.critical("Write excel row failed.")

    def saveWorkBook(self) :
        '''Save excel workbook.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                2016-09-27 V1.0.0[Heyn]
        '''
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
            if self.isOpened is True :
                xlrd_objectc = copy(self.__excelObj)
                worksheet = xlrd_objectc.get_sheet(sheetn)
                values = values.split(',')
                for value in values :
                    worksheet.write(rown,coln,value)
                    rown += 1
                xlrd_objectc.save(self.filePath)
                logging.debug("Write column:%s to [sheet:%s,row:%s,col:%s]." %
                             (values,sheetn,rown,coln))
            else :
                logging.error("File %s is not opened" % self.filePath)
        except :
            logging.critical("Write excel column failed!")
