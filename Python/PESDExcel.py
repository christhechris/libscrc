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
    colnIndex = [2, 3, 5, 6]
    __excel_sheet_index = 0
    __excel_sheet_name = ""
    __excel_rown = 0
    __excel_coln = 0
    xlsInfoLists = [[] for i in range(3)]  # [[], [], []]
    excelContentDict = {}
    externVarDict = {}

    def __init__(self, filepath):
        """__init__"""
        super(PESDExcel, self).__init__()
        self.filepath = filepath
        self.excel = CoraExcel(self.filepath)
        xlsinfolists = self.excel.info()
        if xlsinfolists is None:
            raise IOError
        self.__excel_sheet_name = xlsinfolists[0][self.__excel_sheet_index]
        self.__excel_rown = xlsinfolists[1][self.__excel_sheet_index]
        self.__excel_coln = xlsinfolists[2][self.__excel_sheet_index]
        # Read all data from excel to memory.
        dictkey = 0

        for line in range(self.__excel_rown):
            excelrowlist = self.excel.readrow(
                self.__excel_sheet_name, line)
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
                    messagelist :file's name,
                                 function name,
                                 line number,
                                 keywords
                    i.e.
                    ['Uart_ext.h', 'None', 110, 'extern void UART_dem_init(void);']
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
            self.excel.writecell(value, self.__excel_sheet_index,
                                 self.__excel_rown + rown,
                                 self.colnIndex[messagelist.index(value)])

    def updaterow(self, messagelist, rown=0):
        """Update excel row.
        Argument(s):
                    messagelist :file's name,
                                 function name,
                                 line number,
                                 keywords
                    i.e.
                    ['Uart_ext.h', 'None', 110, 'extern void UART_dem_init(void);']
        Return(s):
                    exists (False)  others (True)
        Notes:
                    2016-09-27 V1.0.0[Heyn]
                    2016-09-28 V1.0.1[Heyn] Search & Matching from Dictionary (origin from excel)
        """

        # <xxx> Delete (;) at end of messagelist
        # messagelist = [(lambda val : "".join([x for x in val if x != ";"]))
        #           (str(val)) for val in messagelist]

        for key in range(self.__excel_rown):
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
                    sheetn = self.__excel_sheet_index
                    conln = self.colnIndex[messagelist.index(messagelist[2])]
                    self.excel.writecell(messagelist[2], sheetn, key, conln)

                    # Delete keys from dictionary
                    self.excelContentDict.pop(key)
                    return False
            except BaseException:
                continue
        print("[OK] Line = %d" % messagelist[2])
        self.writerow(messagelist, rown)
        return True

    @classmethod
    def search_define_value(cls, messagelist):
        """Search define values. <Unstable>"""
        match = re.search('(#define)(\\s+)(\\S+)(\\s+)(.+)', messagelist[3])
        if match is not None:
            print(match.group(3), ' = ', match.group(5),
                  re.findall('\\(.*?\\)$', match.group(5)))

    def search_extern_variable(self, messagelist):
        """Search extern variable.
        Argument(s):
                    messagelist :file's name,
                                 function name,
                                 line number,
                                 keywords
                    i.e.
                    ['Uart_ext.h', 'None', 110, 'extern void UART_dem_init(void);']
        Return(s):
                    exists (False)  others (True)
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        # Search string excluding '(' or ')' in messagelist
        match = re.search('^((?!\\(|\\)).)*$', messagelist[3], re.I)
        if match is not None:
            # (1) Replace \t to ''
            # (2) Removed ';'
            # (3) Split string by ' '
            # (4) Get extern variable and strip it.
            newstr = messagelist[3].replace('\t', ' ').replace(
                ';', '').split(' ')[-1].strip()
            if newstr in self.externVarDict:
                return False
            else:
                # File's name is messagelist[0]
                self.externVarDict[newstr] = messagelist[0]
                # print(newstr)
                return True
        return False

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
