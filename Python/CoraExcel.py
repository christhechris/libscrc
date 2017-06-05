# -*- coding:utf8 -*-
""" Excel read and write """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Excel's read and write.
# History:  2016/09/18
#           2016/10/07 PEP 8 Code Style AND add logging
#           2016/10/13 Pylint check [Rated at 10.00/10]
#           2017/06/05 Python decorator

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import os
import sys
import logging
import xlrd
import xlwt


from xlutils.copy import copy

def excel_catch_exception(origin_func):
    """Catch exception."""
    def wrapper(self, *args, **kwargs):
        """Wrapper."""
        try:
            return origin_func(self, *args, **kwargs)
        except BaseException:
            logging.critical('%s failed.', origin_func.__name__)
    return wrapper

def excel_para_checker(func):
    """Parameter Check."""
    def wrapper(self, *args, **kwargs):
        """wrapper."""
        if self.isopened is True:
            return func(self, *args, **kwargs)
        else:
            logging.error('File %s is not opened', self.filepath)
            return False
    return wrapper

class CoraExcel:
    """ Cora Excel Class. """
    __excelobj = None
    __excelobjcopy = None


    def __init__(self, filepath=sys.path[0], debugLevel=logging.WARNING):
        """ Logging CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET """
        super(CoraExcel, self).__init__()
        self.filepath = filepath
        self.isopened = False

        try:
            if os.path.isfile(self.filepath):
                filename = os.path.basename(self.filepath)
                if filename.split('.')[-1] == 'xls':
                    self.__excelobj = xlrd.open_workbook(self.filepath,
                                                         formatting_info=True)
                    self.__excelobjcopy = copy(self.__excelobj)
                    self.isopened = True

                    formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
                    logging.basicConfig(level=debugLevel, format=formatopt)
                    # logging.basicConfig(
                    # level=debugLevel, format=formatopt, filemode='w',
                    # filename='logging.log')

        except BaseException:
            self.__excelobj = None
            self.isopened = False
            logging.critical("CoraExcel (__init__) failed...")

    @classmethod
    def settingmerged(cls):
        """ Set meraged. """
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

        font = xlwt.Font()
        font.name = 'Arial'
        # font.height = 300 # 15Point
        font.bold = False

        style = xlwt.XFStyle()
        style.font = font
        style.alignment = alignment
        return style

    @excel_para_checker
    def info(self):
        """ Display excel information.
        Argument(s):
                    None
        Return(s):
                    xlsInfoLists -> [0] sheet name
                                    [1] rows number
                                    [2] coln number
        Notes:
                    2016-09-18 V1.0.0[Heyn]
                    2016-09-27 V1.0.1[Heyn] Add return
        """

        xlsinfolists = [[] for i in range(3)]    # [[], [], []]

        for sheetname in self.__excelobj.sheet_names():
            worksheet = self.__excelobj.sheet_by_name(sheetname)
            xlsinfolists[0].append(sheetname)
            xlsinfolists[1].append(worksheet.nrows)
            xlsinfolists[2].append(worksheet.ncols)
            logging.info('%s:(%d rows, %d columns).', sheetname, worksheet.nrows, worksheet.ncols)

        return xlsinfolists

    @excel_para_checker
    @excel_catch_exception
    def readcell(self, sheetname='sheet1', rown=0, coln=0):
        """ Read excel a cell value.
        Argument(s):
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    rown : sheet rows number
                    coln : sheet columns number
        Return(s):
                    cellvalue
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """


        worksheets = self.__excelobj.sheet_names()
        if sheetname not in worksheets:
            logging.error('%s is not exit.', sheetname)
            return False

        worksheet = self.__excelobj.sheet_by_name(sheetname)
        cellvalue = worksheet.cell_value(rown, coln)
        logging.debug('[Sheet:%s,row:%s,col:%s]:%s.', sheetname, rown, coln, cellvalue)

        return cellvalue


    @excel_para_checker
    @excel_catch_exception
    def readrow(self, sheetname='sheet1', rown=0):
        """ Read excle a row values.
        Argument(s):
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    rown : sheet rows number
        Return(s):
                    rowvalues
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """

        rowvalues = None

        worksheets = self.__excelobj.sheet_names()
        if sheetname not in worksheets:
            logging.error('%s is not exit.', sheetname)
            return False
        worksheet = self.__excelobj.sheet_by_name(sheetname)
        rowvalues = worksheet.row_values(rown)
        logging.debug('[Sheet:%s,row:%s]:%s.', sheetname, rown, rowvalues)

        return rowvalues


    @excel_para_checker
    @excel_catch_exception
    def readcol(self, sheetname='sheet1', coln=0):
        """ Read excel a column values.
        Argument(s):
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    coln : sheet columns number
        Return(s):
                    colvalues
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """

        worksheets = self.__excelobj.sheet_names()
        if sheetname not in worksheets:
            logging.error('%s is not exit.', sheetname)
            return False
        worksheet = self.__excelobj.sheet_by_name(sheetname)
        colvalues = worksheet.col_values(coln)
        logging.debug('[Sheet:%s,col:%s]:%s.', sheetname, coln, colvalues)

        return colvalues


    @excel_para_checker
    @excel_catch_exception
    def writecell(self, value='', sheetn=0, rown=0, coln=0):
        """ Write a cell's value to file, other cells is not change.
        Argument(s):
                    values : write's values
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    rown : sheet rows number
                    coln : sheet columns number
        Return(s):
                    None
        Notes:
                    (Used Module) from xlutils.copy import copy
                    2016-09-18 V1.0.0[Heyn]
                    2016-09-27 V1.0.1[Heyn] Removed object copy and save
        """

        worksheet = self.__excelobjcopy.get_sheet(sheetn)
        worksheet.write(rown, coln, value, self.settingmerged())

    @excel_para_checker
    @excel_catch_exception
    def writerow(self, values='', sheetn=0, rown=0, coln=0):
        """ Write a row's values to file, other rows and cells is not change.
        Argument(s):
                    values : write's values
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    rown : sheet rows number
                    coln : sheet columns number
        Return(s):
                    None
        Notes:
                    (Used Module) from xlutils.copy import copy
                    2016-09-18 V1.0.0[Heyn]
                    2016-09-27 V1.0.1[Heyn] Removed object copy and save
        """


        worksheet = self.__excelobjcopy.get_sheet(sheetn)
        values = values.split('#')
        for value in values:
            worksheet.write(rown, coln, value, self.settingmerged())
            coln += 1

        logging.debug(
            "Write row:%s to [Sheet:%s,row:%s,col:%s].", values, sheetn, rown, coln)

    @excel_para_checker
    @excel_catch_exception
    def writecol(self, values='', sheetn=0, rown=0, coln=0):
        """ Write a column's values to excel, other columns and cells is not change.
        Argument(s):
                    values : write's values
                    sheetname : worksheet's name[i.e. sheet1 or sheet 2 and so on]
                    rown : sheet rows number
                    coln : sheet columns number
        Return(s):
                    None
        Notes:
                    (Used Module) from xlutils.copy import copy
                    2016-09-18 V1.0[Heyn]
        """

        worksheet = self.__excelobjcopy.get_sheet(sheetn)
        values = values.split(',')
        for value in values:
            worksheet.write(rown, coln, value)
            rown += 1

        logging.debug(
            'Write column:%s to [Sheet:%s,row:%s,col:%s].', values, sheetn, rown, coln)

    @excel_catch_exception
    def save(self):
        """ Save excel workbook.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
                    2016-10-13 V1.0.1[Heyn] try ... except ...
                    2016-10-13 V1.0.2[Heyn] Delete try ... except ...
        """

        self.__excelobjcopy.save(self.filepath)


if __name__ == '__main__':
    CORAEXCEL = CoraExcel('D:\\test\\abc.xls', debugLevel=logging.INFO)
    CORAEXCEL.info()
    CORAEXCEL.writecell(value='789', sheetn=0, rown=1, coln=1)
    CORAEXCEL.save()
