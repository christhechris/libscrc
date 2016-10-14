# -*- coding:utf8 -*-
""" Main """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Main.
# History:  V1.0.0 2016/10/13

import os
import sys

from CoraFiles import CoraFiles
from PESDExcel import PESDExcel

from HzMainWindows import QtGui
from HzMainWindows import HzMainWindows

QTDLG = None

def main(msglist):
    """ Main Function. """

    dirpaths = msglist[0]
    excelpath = msglist[1]
    regexrule = msglist[2]
    rkeywords = msglist[3]
    excelstartrow = 1

    corafiles = CoraFiles(dirpaths)
    try:
        excel = PESDExcel(excelpath)
    except BaseException:
        print('Open <%s> failed...' % excelpath)
        return False

    filelist = corafiles.findrulefileinfolder(regexrule)
    for fileobj in filelist:
        infolists = corafiles.getinfomationfromfile(fileobj, rkeywords)
        for items in infolists:
            items.insert(0, os.path.basename(fileobj))
            # excel.search_define_value(items)
            ret = excel.updaterow(items, excelstartrow)
            if ret is True:
                excelstartrow += 1
    excel.save()

if __name__ == '__main__':

    # main(["D:\\",
    #       "D:\\pythonTools\\456.xls",
    #       "DGT_*.[c]",
    #       "DGT_dcm_init"])

    # APP = QApplication(sys.argv)
    # QTDLG = HzMainWindows()
    # QTDLG.signelConnectStartBtn(main)
    # QTDLG.show()
    # sys.exit(APP.exec_())
