# -*- coding:utf8 -*-
""" Excel read and write """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Excel's read and write.
# History:  2016/09/18
#           2016/10/07 PEP 8 Code Style AND add logging
#           2016/10/13 Pylint check

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import os
import logging
import xlrd
import xlwt


from xlutils.copy import copy


class CoraExcel:  # pylint: disable=W0702,W0703,W1201
    """ Cora Excel Class. """
    __excelobj = None
    __excelobjcopy = None

    def __init__(self, filepath, debugLevel=logging.WARNING):
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
                    logging.basicConfig(level=debugLevel)
                    # logging.basicConfig(filename='hzExcel.log',
                    #                     level = debugLevel)

        except Exception as err:
            self.__excelobj = None
            self.isopened = False
            logging.critical(str(err))

    def settingmerged(self):
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

        if self.isopened is True:
            for sheetname in self.__excelobj.sheet_names():
                worksheet = self.__excelobj.sheet_by_name(sheetname)
                xlsinfolists[0].append(sheetname)
                xlsinfolists[1].append(worksheet.nrows)
                xlsinfolists[2].append(worksheet.ncols)
                logging.info('%s:(%d row,%d col).' %
                             (sheetname,
                              worksheet.nrows,
                              worksheet.ncols))
        else:
            logging.error('File %s is not opened' % self.filepath)
            return None
        return xlsinfolists

    def readcell(self, sheetname="sheet1", rown=0, coln=0):
        """ Read file's a cell content.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """

        try:
            if self.isopened is True:
                worksheets = self.__excelobj.sheet_names()
                if sheetname not in worksheets:
                    logging.error('%s is not exit.' % sheetname)
                    return False
                worksheet = self.__excelobj.sheet_by_name(sheetname)
                cell = worksheet.cell_value(rown, coln)
                logging.debug('[sheet:%s,row:%s,col:%s]:%s.' %
                              (sheetname, rown, coln, cell))
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Read excel cell failed.")

    def readrow(self, sheetname="sheet1", rown=0):
        """ Read file's a row content.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """

        row = None
        try:
            if self.isopened is True:
                worksheets = self.__excelobj.sheet_names()
                if sheetname not in worksheets:
                    logging.error('%s is not exit.' % sheetname)
                    return False
                worksheet = self.__excelobj.sheet_by_name(sheetname)
                row = worksheet.row_values(rown)
                logging.debug('[sheet:%s,row:%s]:%s.' % (sheetname, rown, row))
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Read excel row failed.")
        return row

    def readcol(self, sheetname="sheet1", coln=0):
        """ Read file's a column content.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-18 V1.0.0[Heyn]
        """
        try:
            if self.isopened is True:
                worksheets = self.__excelobj.sheet_names()
                if sheetname not in worksheets:
                    logging.error('%s is not exit.' % sheetname)
                    return False
                worksheet = self.__excelobj.sheet_by_name(sheetname)
                col = worksheet.col_values(coln)
                logging.debug('[sheet:%s,col:%s]:%s.' % (sheetname, coln, col))
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Read excel column failed.")

    def writecell(self, value='', sheetn=0, rown=0, coln=0):
        """ Write a cell to file,other cell is not change.
        Argument(s):
                    [value, sheetn, rown, coln]
        Return(s):
                    None
        Notes:      (Used Module) from xlutils.copy import copy
                    2016-09-18 V1.0.0[Heyn]
                    2016-09-27 V1.0.1[Heyn] Removed object copy and save
        """

        try:
            if self.isopened is True:
                worksheet = self.__excelobjcopy.get_sheet(sheetn)
                worksheet.write(rown, coln, value, self.settingmerged())
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Write excel cell failed.")

    def writerow(self, values='', sheetn=0, rown=0, coln=0):
        """ Write a row to file, other row and cell is not change.
        Argument(s):
                    [values, sheetn, rown, coln]
        Return(s):
                    None
        Notes:      (Used Module) from xlutils.copy import copy
                    2016-09-18 V1.0.0[Heyn]
                    2016-09-27 V1.0.1[Heyn] Removed object copy and save
        """

        try:
            if self.isopened is True:
                worksheet = self.__excelobjcopy.get_sheet(sheetn)
                values = values.split('#')
                for value in values:
                    worksheet.write(rown, coln, value, self.settingmerged())
                    coln += 1
                logging.debug("Write row:%s to [sheet:%s,row:%s,col:%s]." %
                              (values, sheetn, rown, coln))
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Write excel row failed.")

    def saveworkbook(self):
        """ Save excel workbook.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-27 V1.0.0[Heyn]
        """

        self.__excelobjcopy.save(self.filepath)

    def writecol(self, values='', sheetn=0, rown=0, coln=0):
        """ Write a col to file, other col and cell is not change.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:  (Used Module) from xlutils.copy import copy
                2016-09-18 V1.0[Heyn]
        """

        try:
            if self.isopened is True:
                xlrd_objectc = copy(self.__excelobj)
                worksheet = xlrd_objectc.get_sheet(sheetn)
                values = values.split(',')
                for value in values:
                    worksheet.write(rown, coln, value)
                    rown += 1
                xlrd_objectc.save(self.filepath)
                logging.debug("Write column:%s to [sheet:%s,row:%s,col:%s]." %
                              (values, sheetn, rown, coln))
            else:
                logging.error("File %s is not opened" % self.filepath)
        except:
            logging.critical("Write excel column failed!")
