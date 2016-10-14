# -*- coding:utf8 -*-
""" ESD Excel read and write"""
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  esdExcel
# History:  2016/09/27
#           2016/10/07 PEP 8 Code Style

import re


from CoraExcel import CoraExcel


class PESDExcel:
    """ESD Excel Class"""
    # write excel coln index match values list
    colnIndex = [2, 4, 3, 5]
    __excel_sheet_index__ = 0
    __excel_sheet_name__ = ""
    __excel_rown__ = 0
    __excel_coln__ = 0
    xlsInfoLists = [[] for i in range(3)]  # [[], [], []]
    excelContentDict = {}

    def __init__(self, filepath):
        """__init__"""
        super(PESDExcel, self).__init__()
        self.filepath = filepath
        self.excel = CoraExcel(self.filepath)
        xlsinfolists = self.excel.info()
        if xlsinfolists is None:
            raise IOError
        self.__excel_sheet_name__ = xlsinfolists[0][self.__excel_sheet_index__]
        self.__excel_rown__ = xlsinfolists[1][self.__excel_sheet_index__]
        self.__excel_coln__ = xlsinfolists[2][self.__excel_sheet_index__]
        # Read all data from excel to memory.
        dictkey = 0

        for line in range(self.__excel_rown__):
            excelrowlist = self.excel.readrow(
                self.__excel_sheet_name__, line)
            # Delete space " "  in excel every cell
            # excelrowlist = [(lambda val: "".join([x for x in val if x != " "]))(
            #     str(val)) for val in excelrowlist]
            # Delete enter "\n" in excel every cell
            # excelrowlist = [(lambda val: "".join([x for x in val if x != "\n"]))(
            #     str(val)) for val in excelrowlist]
            self.excelContentDict[dictkey] = excelrowlist
            dictkey += 1

    def writerow(self, messagelist, rown=0):
        """ Write excel row.
        Argument(s):
                    messagelist :excelFileName,
                                 functionName,
                                 keywordsLines,
                                 keywords
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        """

        # values = strmessage.split('#')
        # Delete (;) at end of messagelist
        # messagelist = [(lambda val: "".join([x for x in val if x != ";"]))
        #           (str(val)) for val in messagelist]

        for value in messagelist:
            self.excel.writecell(value, self.__excel_sheet_index__,
                                 self.__excel_rown__ + rown,
                                 self.colnIndex[messagelist.index(value)])

    def updaterow(self, messagelist, rown=0):
        """Update excel row.
        Argument(s):
                    messagelist :excelFileName,
                                 functionName,
                                 keywordsLines,
                                 keywords
        Return(s):
                    exists (False)  others (True)
        Notes:
                    2016-09-27 V1.0.0[Heyn]
                    2016-09-28 V1.0.1[Heyn] Search & Matching from Dictionary (origin from excel)
        """

        # <xxx> Delete (;) at end of messagelist
        # messagelist = [(lambda val : "".join([x for x in val if x != ";"]))
        #           (str(val)) for val in messagelist]

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
                memorylist = [x for x in self.excelContentDict[key] if x != '']
                if not memorylist:
                    # Delete keys from dictionary
                    self.excelContentDict.pop(key)
                    continue
                ret = list(set(memorylist).intersection(set(messagelist)))
                if len(ret) == 4:
                    # Delete keys from dictionary
                    self.excelContentDict.pop(key)
                    return False

                if len(ret) == 3:
                    # <TODO> Update keywords line number
                    sheetn = self.__excel_sheet_index__
                    conln = self.colnIndex[messagelist.index(messagelist[2])]
                    self.excel.writecell(messagelist[2], sheetn, key, conln)

                    # Delete keys from dictionary
                    self.excelContentDict.pop(key)
                    return False
            except BaseException:
                continue
        print("OK")
        self.writerow(messagelist, rown)
        return True

    @classmethod
    def search_define_value(cls, messagelist):
        """Search define values. <Unstable>"""
        match = re.search('(#define)(\\s+)(\\S+)(\\s+)(.+)', messagelist[3])
        if match is not None:
            print(match.group(3), ' = ', match.group(5),
                  re.findall('\\(.*?\\)$', match.group(5)))

    def save(self):
        """Save excel workbook.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        """
        self.excel.save()
