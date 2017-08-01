# -*- coding:utf8 -*-
""" GUI AutoTest WebMc """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  GUI AutoTest WebMc.
# History:  2017/07/28 V1.0 [Heyn]

import sys
import time

from PIL import Image, ImageDraw, ImageFont

from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton, QApplication)

from PyQt5.QtGui import QFont
from PyQt5.QtQuick import QQuickView

from PBoxWebAPI import PBoxWebAPI




# TEST = """+----------------------+-----------+-----------+----------+---------------+---------------+------+----------+------+------------+-----+--------+
# |       ItemName       | AliasName | Frequency | Slave ID | Function Code | Slave Address | Rate |   TYPE   | MQTT | B/L Endian | R/W | Result |
# +----------------------+-----------+-----------+----------+---------------+---------------+------+----------+------+------------+-----+--------+
# | K7fe3XozjcaZDUfmaLht |   test1   |   649229  |    24    |       2       |   1241709151  |  1   |  INT16   |  1   |     1      |  1  | False  |
# | W0iET5ZYvMC4PdmYzCBu |   test2   |   74621   |   235    |       3       |   646733809   |  0   |  FLOAT   |  1   |     0      |  1  | False  |
# | 3iM9gzWkUmYzerjOFHLd |   test3   |  2716559  |    38    |       1       |   1403898291  |  1   |  DWORD   |  0   |     0      |  0  | False  |
# | lZkWKto6wfLIyMSOKD1L |   test4   |  2270041  |    4     |       2       |   1279810640  |  1   |  INT16   |  1   |     0      |  1  | False  |
# | 0Cxdc3YXmlJumWRWAhKx |   test5   |  1889244  |    98    |       1       |   1873614635  |  0   |  DWORD   |  0   |     1      |  1  | False  |
# | EuJa6TvZUIxDWrIkyTt0 |   test6   |   985414  |   207    |       1       |   1084227429  |  1   |  DOUBLE  |  0   |     1      |  1  | False  |
# | kRz5wHsztotmWAzUm0c2 |   test7   |  2798311  |    38    |       5       |   189548108   |  0   |   BOOL   |  1   |     0      |  0  | False  |
# | sez0Az0DO1x1Da480y3T |   test8   |   289489  |   122    |       1       |   1380593664  |  0   |  FLOAT   |  0   |     1      |  0  | False  |
# | sJsDprg0DjZre9T1pXmJ |   test9   |  3342694  |    55    |       1       |   2141183518  |  0   |  FLOAT   |  0   |     0      |  0  | False  |
# | vampXSSbWWfXlknQB9dB |   test10  |  1505306  |   142    |       1       |   2074030975  |  1   |   WORD   |  1   |     0      |  1  | False  |
# | cDKWiKE10KnOzjaQBmGH |   test11  |   25867   |   139    |       2       |   1402322162  |  1   | STRING20 |  1   |     0      |  0  | False  |
# | oX34d7dcyWgpyFNhivHc |   test12  |  1698340  |    33    |       1       |   823117212   |  0   | STRING38 |  0   |     0      |  0  | False  |
# | hAseq84PrTmeVPIRPeZ6 |   test13  |  2223157  |   146    |       4       |   577396549   |  0   |   BOOL   |  1   |     0      |  1  | False  |
# | WRE1yI34VfcpAe1oAISV |   test14  |  1598966  |   236    |       1       |   2050986327  |  1   | STRING6  |  0   |     1      |  0  | False  |
# | nL2ixGHuWK9hp1OSXZuu |   test15  |  1453711  |    86    |       3       |   1174594204  |  1   |   WORD   |  0   |     0      |  0  | False  |
# | NiMm5qDn4h7j6mUBKE3g |   test16  |   773918  |   247    |       3       |   1406688706  |  0   |  DOUBLE  |  0   |     0      |  1  | False  |
# | nVYRbdQ731aN5hoJafsW |   test17  |  1259790  |   211    |       3       |   1783982078  |  1   |  FLOAT   |  0   |     1      |  1  | False  |
# | Blz71ua7Xf9BHgzpxfMt |   test18  |  2013863  |   254    |       2       |   1519419283  |  1   | STRING20 |  1   |     0      |  0  | False  |
# | uV4rEmpvvQum9rKEAR1t |   test19  |  3397024  |   112    |       5       |   525772188   |  1   |   WORD   |  0   |     1      |  0  | False  |
# | DkDOVCJbzwSWLZpmFPAM |   test0   |  3129691  |   197    |       4       |   2084387857  |  1   |   WORD   |  1   |     0      |  1  | False  |
# +----------------------+-----------+-----------+----------+---------------+---------------+------+----------+------+------------+-----+--------+"""

class SlotClass(QObject):
    """PyQt & QML slot"""
    def __init__(self):
        super(SlotClass, self).__init__()
        self.web = None
        self.newitemsize = 0

    def saveimage(self, letters):
        """Save Image"""
        img = Image.new("RGB", (1024, 20 + (5 + self.newitemsize)*14 + 20), (255, 255, 255))
        drw = ImageDraw.Draw(img)
        font = ImageFont.truetype("cour.ttf", 12)
        reportime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        drw.text((10, 20), reportime + '\n' + str(letters), font=font, fill="#000000")
        # img.show()
        img.save(str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + '.png')

    @pyqtSlot(str, str, result=bool)
    def login(self, hostip, pwd):
        """Login WebMc."""
        self.web = PBoxWebAPI(hostip)
        print(self.web.login(password=pwd))
        return True

    @pyqtSlot(result=str)
    def start(self):
        """Start test."""
        self.web.newchannel(items=['Modbus-RTU', '/dev/ttymxc1', '9600', 'None', '8', '1', '500'])
        self.web.newdevice(name='Default')
        ret = self.web.newitems(self.newitemsize)
        self.saveimage(ret)
        return str(ret)

    @pyqtSlot(int)
    def comboBox(self, index):
        """Index"""
        self.newitemsize = int(index)

    @pyqtSlot()
    def exit(self):
        """GUI Exit"""
        sys.exit()

def main():
    """Main Function Entry."""
    app = QApplication(sys.argv)

    # Create a label and set its properties
    applable = QQuickView()
    applable.setSource(QUrl('basic.qml'))

    conn = SlotClass()
    context = applable.rootContext()
    context.setContextProperty("conn", conn)

    # Show the Label
    applable.show()
    # Execute the Application and Exit
    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()
