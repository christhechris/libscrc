# -*- coding:utf8 -*-
""" Main """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Main.
# History:  V1.0.0 2016/10/13

import os


from CoraFiles import CoraFiles
from PESDExcel import PESDExcel

def main(msglist):
    """ Main Function. """
    filespath = msglist[0]
    excelpath = msglist[1]
    regexrule = msglist[2]
    rkeywords = msglist[3]
    excelstartrow = 1

    corafiles = CoraFiles()
    excel = PESDExcel(excelpath)

    filelist = corafiles.findrulefileinfolder(regexrule)
    for fileobj in filelist:
        infolists = corafiles.getinfomationfromfile(fileobj, rkeywords)
        for items in infolists:
            str4excel = os.path.basename(
                fileobj) + '#' + str(items[0]) + '#' + str(items[1]) + '#' + str(items[2])
            # print(str4excel)
            ret = excel.updaterow(str4excel, excelstartrow)
            if ret is True:
                excelstartrow += 1
    excel.save()

if __name__ == '__main__':

    main(["D:\\",
          "D:\\pythonTools\\abc.xls",
          "DGT_*.[c]",
          "while"])
