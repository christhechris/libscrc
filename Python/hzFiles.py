# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Files
# History:  2016/09/04
#           2016/10/07 PEP 8 Code Style

import sys
import os
import os.path
import re

from glob import glob


class hzFiles:

    def __init__(self, dirPath=sys.path[0], debug=False):
        super(hzFiles, self).__init__()
        self.dirPath = dirPath
        self.debug = debug
        self.count = 0
        self.braceCnt = 0
        self.lineAsterisk = 0

    def getFilesListInCurrentFolder(self):
        ''' Find files in current folder.
        Argument(s):
                    None
        Return(s):
                    FileList
        Notes:
                    2016-09-14 V1.0[Heyn]
        '''
        filesList = []
        for root, dirs, files in os.walk(self.dirPath):
            for fileObj in files:
                filesList.append(os.path.join(root, fileObj))
        return filesList

    def getFilterFilesEXT(self, filterStr):
        ''' Filter file's extension.
        Argument(s):
                    filterStr [filter key words]
                    e.g. (".c|.h")
        Return(s):
                    Grep result fileslist
        Notes:
                    2016-09-14 V1.0[Heyn]
                    2016-09-26 V1.1[Heyn]	Delete space(" ") in filterStr
        '''
        filesList = []
        # Delete space(" ") in filterStr
        filterStr = "".join([x for x in filterStr if x != " "])

        for root, dirs, files in os.walk(self.dirPath):
            for fileObj in files:
                if os.path.isfile(os.path.join(root, fileObj)):
                    ext = os.path.splitext(fileObj)[1].lower()
                    if ext in filterStr.split("|"):
                        filesList.append(os.path.join(root, fileObj))
        print("Search valid %s files = %d" % (filterStr, len(filesList)))
        return filesList

    def getFileName(self, filePath):
        fileName = os.path.basename(filePath)
        return fileName

    def getFileApproximateMatch(self, pattern):
        ''' Approximate Serach files.
        Argument(s):
                    pattern (* , ? , [ , ] )
                    e.g. Grep .c and .h files   pattern = "*.[c,h]"
                    e.g. Grep .jpg files 		pattern = "*.jpg"
        Return(s):

        Notes:  (Used Module) from glob import glob
                2016-09-15 V1.0[Heyn]
                2016-09-26 V1.0[Heyn] Add anotation.
        '''
        for root, dirs, files in os.walk(self.dirPath):
            for match in glob(os.path.join(root, pattern)):
                yield match

    def getFilePreciseMatch(self, pattern):
        ''' Precise Serach files.
        Argument(s):
                    None
        Return(s):

        Notes:  (Used Module) from glob import glob
                2016-09-17 V1.0[Heyn]
        '''
        for root, dirs, files in os.walk(self.dirPath):
            candidate = os.path.join(root, pattern)
            if os.path.isfile(candidate):
                yield os.path.abspath(candidate)

    def __getFunctionName__(self, eachLineList, eachLineStrip, functionName):
        '''
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-20 V1.0[Heyn]
        '''

        if re.match(".*?{.*?", eachLineStrip, re.I):
            strCache = ""
            loop = 2
            self.braceCnt += 1
            if (self.braceCnt == 1):
                # When the function name is divided into two or more rows defined
                # We need to loop processing
                try:
                    while True:
                        functionLine = str(
                            eachLineList[len(eachLineList) - loop]) + strCache
                        # Delete array
                        if re.match(".*?\[.*?\]", functionLine, re.I):
                            self.braceCnt -= 1
                            break
                        # Delete special keywords.
                        if re.match(".*?(struct|enum|union).*?", functionLine, re.I):
                            self.braceCnt -= 1
                            break

                        if re.match(".*?\(.*?\)", functionLine, re.I):
                            functionNameEnd = functionLine[
                                : functionLine.find("(")].strip()
                            functionNameStartIndex = functionNameEnd.rfind(" ")
                            functionName = functionNameEnd[
                                functionNameStartIndex + 1:].strip()
                            # print(functionName)
                            self.count += 1
                            break
                        else:
                            loop += 1
                            strCache = functionLine
                except Exception as e:
                    # print (str(e))
                    pass

        if re.match(".*?}.*?", eachLineStrip, re.I):
            if self.braceCnt > 0:
                self.braceCnt -= 1

        return functionName

    def __deleteAnotation__(self, eachLine):
        '''Find and remove the comment.
        Argument(s):
                    eachLine : file's each line.
        Return(s):
                    Remove the comment and striped.
        Notes:
                    2016-09-20 V1.0[Heyn]
        '''
        eachLineStrip = re.sub(
            '([^:]?//.*?$)|(/\*(.*?)\*/)', '', eachLine).strip()
        if re.match('.*?/\*', eachLineStrip) and self.lineAsterisk == 0:
            self.lineAsterisk = 1
            eachLineStrip = re.sub('/\*.*?$', '', eachLineStrip).strip()
        if re.match('.*?\*/$', eachLineStrip) and self.lineAsterisk == 1:
            self.lineAsterisk = 0
            eachLineStrip = re.sub('^.*?\*/$', '', eachLineStrip).strip()
        if self.lineAsterisk == 1:
            return ""
        #print (eachLineStrip)
        return eachLineStrip.strip()

    def findStringFromFile(self, filePath, regex):
        '''
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-09-17 V1.0.0[Heyn]
                    2016-09-17 V1.0.1[Heyn] Delete (space) in eachLineStrip
        '''
        functionName = ''
        infoLists = [[] for i in range(3)]  # [[], [], []]
        fileList = []
        lineNum = 0
        fileObj = open(filePath, 'r', encoding='SJIS', errors='ignore')
        try:

            for eachLine in fileObj.readlines():
                lineNum += 1
                eachLineStrip = self.__deleteAnotation__(eachLine.strip())
                fileList.append(eachLineStrip)
                functionName = self.__getFunctionName__(
                    fileList, eachLineStrip, functionName)

                if eachLineStrip:
                    if re.search(regex, eachLineStrip):
                        # <bug: 1609202120> self.braceCnt != 0
                        # When the function does not match the condition
                        # The next function name match the condition
                        # The output will cause an error.
                        if self.braceCnt != 0:
                            infoLists[0].append(functionName)
                            infoLists[1].append(lineNum)
                            # Delete space in eachLineStrip
                            infoLists[2].append(
                                "".join([x for x in eachLineStrip if x != " "]))

                        if self.debug == True:
                            print("%5d" % lineNum, end='')
                            print("%20s      " %
                                  self.getFileName(filePath), end='')
                            if self.braceCnt != 0:
                                print("%50s      " % functionName, end='')
                            else:
                                print("%50s      " % "<NONE>", end='')
                            print(eachLineStrip)

            return infoLists
        finally:
            fileObj.close()

    def grepStringFromFile(self, filePath, regex):
        '''Grep string from file.
        Argument(s):
                    filePath : file path
                    regex	 : matching rule
        Return(s):
                    fileList[[], [], []]
                    [0] filePath
                    [1] line number
                    [2] content
        Notes:
                    2016-09-25 V1.0[Heyn]
        '''

        infoLists = [[] for i in range(3)]  # [[], [], []]
        lineNum = 0
        fileObj = open(filePath, 'r', encoding='SJIS', errors='ignore')
        try:
            for eachLine in fileObj.readlines():
                lineNum += 1
                eachLineStrip = self.__deleteAnotation__(eachLine.strip())
                if eachLineStrip:
                    if re.search(regex, eachLineStrip, re.I):
                        infoLists[0].append(filePath)
                        infoLists[1].append(lineNum)
                        infoLists[2].append(eachLineStrip)
                        if self.debug == False:
                            print("%5d" % lineNum, end='')
                            print("%20s      " %
                                  self.getFileName(filePath), end='')
                            print(eachLineStrip)

            return infoLists
        finally:
            fileObj.close()
