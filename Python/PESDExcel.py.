# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  esdExcel
# History:  2016/09/27
#           2016/10/07 PEP 8 Code Style

import os
import sys
import re
from hzExcel import *


class esdExcel:
    colnIndex = [2, 4, 3, 5]  # write excel coln index match values list
    __excel_sheet_index__ = 2

    __excel_sheet_name__ = ""
    __excel_rown__ = 0
    __excel_coln__ = 0
    xlsInfoLists = [[] for i in range(3)]  # [[], [], []]
    excelContentDict = {}

    def __init__(self, filePath):
        ''' .
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        '''
        super(esdExcel, self).__init__()
        self.filePath = filePath
        self.excelhd = hzExcel(self.filePath)
        xlsInfoLists = self.excelhd.getInfo()
        self.__excel_sheet_name__ = xlsInfoLists[0][self.__excel_sheet_index__]
        self.__excel_rown__ = xlsInfoLists[1][self.__excel_sheet_index__]
        self.__excel_coln__ = xlsInfoLists[2][self.__excel_sheet_index__]

        # Read all data from excel to memory.
        dictKey = 0
        for line in range(self.__excel_rown__):
            excelRowList = self.excelhd.readRow(
                self.__excel_sheet_name__, line)
            # Delete space " "  in excel every cell
            excelRowList = [(lambda val: "".join([x for x in val if x != " "]))(
                str(val)) for val in excelRowList]
            # Delete enter "\n" in excel every cell
            excelRowList = [(lambda val: "".join([x for x in val if x != "\n"]))(
                str(val)) for val in excelRowList]
            self.excelContentDict[dictKey] = excelRowList
            dictKey += 1

    def writeExcelRow(self, strMessage, rown=0):
        '''Write excel row.
        Argument(s):
                    strMessage [excelFileName, functionName, keywordsLines, keywords]
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        '''
        values = strMessage.split('#')
        # Delete (;) at end of values
        # values = [(lambda val : "".join([x for x in val if x != ";"]))(str(val)) for val in values]
        for value in values:
            self.excelhd.writeCell(value, self.__excel_sheet_index__,
                                   self.__excel_rown__ + rown, self.colnIndex[values.index(value)])

    def updateExcelRow(self, strMessage, rown=0):
        '''Update excel row.
        Argument(s):
                    strMessage [excelFileName, functionName, keywordsLines, keywords]
        Return(s):
                    exists (False)  others (True)
        Notes:
                    2016-09-27 V1.0.0[Heyn]
                    2016-09-28 V1.0.1[Heyn] Search & Matching from Dictionary (origin from excel)
        '''
        values = strMessage.split('#')
        # <xxx> Delete (;) at end of values
        # values = [(lambda val : "".join([x for x in val if x != ";"]))(str(val)) for val in values]

        for key in range(self.__excel_rown__):
            # excelRowList and values 's Intersection
            # e.g.
            # a=[2,3,4,5]
            # b=[2,5,8]
            # tmp = [val for val in a if val in b]	--> result [2, 5]
            # list(set(a).intersection(set(b)))   	--> result [2, 5]
            # list(set(a).union(set(b)))			--> result [2,3,4,5,8]
            # list(set(b).difference(set(a)))		--> result [8]
            try:
                ret = [val for val in self.excelContentDict[
                    key] if val in values]
                if len(ret) == 4:
                    return False

                if len(ret) == 3:
                    # <TODO> Update keywords line number

                    # Delete keys from dictionary
                    self.excelContentDict.pop(key)
                    return False
            except:
                continue

        self.writeExcelRow(strMessage, rown)
        return True

    def saveExcel(self):
        '''Save excel workbook.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        '''
        self.excelhd.saveWorkBook()
