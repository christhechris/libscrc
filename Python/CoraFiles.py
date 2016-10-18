# -*- coding:utf8 -*-
""" Files Search """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  File's read and search.
# History:  V1.0.0 2016/10/13

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import sys
import re
import os
import os.path
import logging


from glob import glob


class CoraFiles:
    """ CoraFiles Class """

    def __init__(self, dirpath=sys.path[0], debugLevel=logging.WARNING):
        super(CoraFiles, self).__init__()
        self.dirpath = dirpath
        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)
        # logging.basicConfig(
        # level=debugLevel, format=formatopt, filemode='w',
        # filename='logging.log')

    def findallfileinfolder(self):
        """ Find all files in current folder.
        Argument(s):
                    None
        Return(s):
                    fileslist
        Notes:
                    2016-10-08 V1.0[Heyn]
        """
        filelist = []
        for root, dirs, files in os.walk(self.dirpath):  # pylint: disable=W0612
            for fileobj in files:
                filelist.append(os.path.join(root, fileobj))
        return filelist

    def findrulefileinfolder(self, pattern='*.*'):
        """ Find all files in current folder by pattern.
        Argument(s):
                    pattern (* , ? , [ , ] )
                    e.g. Grep .c and .h files   pattern = "*.[c,h]"
                    e.g. Grep .jpg files        pattern = "*.jpg"
        Return(s):
                    fileslist
        Notes:
                    (Used Module) from glob import glob
                    2016-10-08 V1.0[Heyn]
        """
        filelist = []
        for root, dirs, files in os.walk(self.dirpath):  # pylint: disable=W0612
            for match in glob(os.path.join(root, pattern)):
                filelist.append(match)
        return filelist

    @classmethod
    def findstringinfile(cls, filepath, pattern=r'[\\s\\S]*'):
        """ Find string in current file by pattern.
        Argument(s):
                    pattern (* , ? , [ , ] )
                    e.g. Grep .c and .h files   pattern = "*.[c,h]"
                    e.g. Grep .jpg files        pattern = "*.jpg"
        Return(s):
                    content Dict
        Notes:
                    (Used Module) from glob import glob
                    2016-10-08 V1.0[Heyn]
        """
        contentdict = {}
        fileobj = open(filepath, 'r', encoding='SJIS', errors='ignore')
        try:
            for linenumber, eachline in enumerate(fileobj):
                if re.search(pattern, eachline, re.I):
                    contentdict[linenumber] = eachline
            print((lambda dict: [item for item in dict.items()])(contentdict))
        finally:
            fileobj.close()
        return contentdict

    @classmethod
    def findstringindict(cls, filecontentdict, pattern=r'[\\s\\S]*'):
        """ Find string in dicts by pattern.
        Argument(s):
                    filecontentdict  : File Content Dict
                    pattern([\\s\\S]*) : Search any characters
        Return(s):
                    contentdict = {index:[lineNumber, eachLine], ...}
        Notes:
                    2016-10-08 V1.0[Heyn]
        """
        contentdict = {}
        for index, value in filecontentdict.items():
            if re.search(pattern, value[1], re.I):
                contentdict[index] = value
        # print((lambda dict: [item for item in dict.items()])(contentdict))
        return contentdict

    @classmethod
    def delanotationinfile(cls, filepath):
        """ Delete anotation in file.
        Argument(s):
                    filePath : file path
        Return(s):
                    contentlist = [(linenumber,eachline),(key,value),...]
        Notes:
                    2016-10-08 V1.0.0[Heyn]
                    2016-10-18 V1.0.1[Heyn]
                    (1) re.sub(r'([^:]?//.*?$)|(/\\*(.*?)\\*/)', '', eachline).strip()
                    Change TO:
                    (2) re.sub(r'([^:]?//.*?$)|(/\\*(.*?)\\*/$)', '', eachline).strip()
                    i.e.
                    /* This is a test / message. */
                    If used (1) process  -> result = message. */
                    If used (2) process  -> result = ''
        """
        contentdict = {}
        multilinenote = False
        indexdict = 0
        fileobj = open(filepath, 'r', encoding='SJIS', errors='ignore')
        try:
            for linenumber, eachline in enumerate(fileobj):
                eachlineregex = re.sub(
                    r'([^:]?//.*?$)|(/\\*(.*?)\\*/$)', '', eachline).strip()
                if (multilinenote is False) and (
                        re.match('.*?/\\*', eachlineregex)):
                    multilinenote = True
                    eachlineregex = re.sub(
                        r'/\\*.*?$', '', eachlineregex).strip()
                    # Methods for handling the following annotations
                    # for (i=0; i<100; i++)     /* loop 100 times
                    #                              It's test code */
                    # Add below code.
                    if eachlineregex != '':
                        contentdict[linenumber] = eachlineregex
                if (multilinenote is True) and (
                        re.match(r'.*?\\*/$', eachlineregex)):
                    multilinenote = False
                    eachlineregex = re.sub(
                        r'^.*?\\*/$', '', eachlineregex).strip()
                if multilinenote is True:
                    continue
                if eachlineregex != '':
                    contentdict[indexdict] = [linenumber + 1, eachlineregex]
                    indexdict += 1
        finally:
            fileobj.close()

        for key, value in contentdict.items():
            logging.info(str(key) + "  " + str(value))

        # Sorted by key     key=lambda d: d[0]
        # Sorted by value   key=lambda d: d[1]
        # return sorted(contentdict.items(),
        #               key=lambda d: d[0],
        #               reverse = False)
        return contentdict

    @classmethod
    def findfunctionnameindict(cls, contentdict):
        """ Find function name in dict.
        Argument(s):
                    filePath : file path
        Return(s):
                    functionlinenum
        Notes:
                    2016-10-08 V1.0[Heyn]
        """

        # Dict
        linenumlist1 = [x[0] for x in contentdict.items() if '{' in x[1][1]]
        linenumlist2 = [x[0] for x in contentdict.items() if '}' in x[1][1]]
        # print(linenumlist1)
        # print(linenumlist2)

        if not linenumlist1 or not linenumlist2:
            return []

        functionlinenum = []
        functionlinenum.append(linenumlist1[0] - 1)
        for num in linenumlist1:
            if num > linenumlist2[0]:
                linenumlist2 = [y for y in linenumlist2 if num < y]
                # The number of braces{} in the function is the same
                if len(linenumlist2) == (len(linenumlist1) -
                                         linenumlist1.index(num)):
                    functionlinenum.append(num - 1)
        # Function must be include '(' and ')'
        # contentdict = {key : [lineNumber, Values]}
        functionlinenum = [
            key for key in functionlinenum if '(' in contentdict.get(key)[1]]
        # Remove C language key words
        ckeywords = ['#define', 'struct', '#if', '#endif']
        functionlinenum = [key for key in functionlinenum if all(
            t not in contentdict.get(key)[1] for t in ckeywords)]
        # e.g. void UART_com_init ( void )
        functionsplit = list(
            map(lambda key: contentdict.get(key)[1].split('('), functionlinenum))
        # e.g. ['void UART_com_init ', 'void )']
        functionsplit = list(
            map(lambda x: x[0].strip().split(' ')[-1], functionsplit))
        # Update dict
        # [New] contentdict = {key : [lineNumber, function, functionName]}
        list(map(lambda val, key: contentdict[key].append(
            val), functionsplit, functionlinenum))

        # Debug information
        # list(map(lambda key: print(key, contentdict.get(key)), functionlinenum))
        # print("Function Count = %d" % (len(functionlinenum) + 1))
        return functionlinenum

    def getinfomationfromfile(self, filepath, pattern=r"[\\s\\S]*"):
        """ Get information from file by pattern.
        Argument(s):
                    filepath : file path
                    pattern([\\s\\S]*) : Search any characters
                    i.e.
                    pattern = "for|<<|>>|while|\\+\\+|\\+\\=|--|-\\="
        Return(s):
                    [functionName, lineNumber, keywords]
        Notes:
                    2016-10-08 V1.0[Heyn]
        """

        retinfolist = []
        filedicts = self.delanotationinfile(filepath)
        keywordslist = sorted(self.findstringindict(
            filedicts, pattern).items(), key=lambda d: d[0], reverse=False)

        fnindexlist = self.findfunctionnameindict(filedicts)

        for keyindex, values in keywordslist:
            newlinenum = [x for x in fnindexlist if x > keyindex]
            diff = list(set(fnindexlist).difference(set(newlinenum)))
            diff.sort()
            infolist = []
            if len(newlinenum) == len(fnindexlist):
                infolist.append('None')
            elif not newlinenum:
                infolist.append(filedicts[fnindexlist[-1]][2])
            else:
                infolist.append(filedicts[diff[-1]][2])
            infolist.extend(values)
            retinfolist.append((lambda x: [x[0], x[1], x[2]])(infolist))

        # print('#' * 120)
        # print("FILE NAME: [ %s ]    MATCH: (%d)" % (
        #     os.path.basename(filepath), len(retinfolist)))
        # for items in retinfolist:
        #     print(('%-50s%4d %90s') % (items[0], items[1], items[2]))
        # print('\r\n')

        return retinfolist

# if __name__ == '__main__':
#     HZFILE = CoraFiles()
#     FILELIST = HZFILE.findrulefileinfolder("DGT_*.[c,h]")
#     for file in FILELIST:
#         HZFILE.getinfomationfromfile(file, 'for')

#     HZFILE.getinfomationfromfile("G:\\@gitHub\\Python\\LD_LCM.c", 'LCD_BUFFER')
