# -*- coding:utf8 -*-
""" CoraCom COM Server."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  CoraCom.
# History:  2016/12/20


# [Modules]
#
# 1) pypiwin32-219-cp35-none-win32.whl
#    Web: https://pypi.python.org/pypi/pypiwin32/219
# 2) pywin32-220.win32-py3.5.exe or pywin32-220.win-amd64-py3.5.exe
#    Web: https://sourceforge.net/projects/pywin32/files/pywin32/
#

# [Register]
#
# PyCoraCom.py --register
# PyCoraCom.py --unregister
# or
# Python IDEL->F5

# [Pyinstaller to *.exe]
# pyinstaller -F D:\..\..\PyNCTool.py --hidden-import=win32timezone
#

# [Run *.exe (Windows Plugins)]
# 1) vc_redist.x86.exe or vc_redist.x64.exe
# Web:https://www.microsoft.com/zh-cn/download/confirmation.aspx?id=48145
#

# [Using]
# 1) VBS
# Set PyCom = CreateObject("Cora.PyNCTool")
# PyCom.open()
# PyCom.sleep(1000)
# PyCom.read("Hello I'm (read)!")
# PyCom.write("Hello I'm (write)!")
# PyCom.close()
#

import time
import errno
import socket
import pythoncom

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 54321

TCP_SOCKET_BLOCKING = 1        # No Blocking (=0), or Blocking (=1)
TCP_SOCKET_NO_BLOCKING = 0

BUFFER_SIZE = 1024
TIMEOUT = 2


class CoraCOM:
    """CoraCOM Class"""

    def __init__(self):
        self.sock = ''

    def __del__(self):
        self.close()

    def open(self, tmr=TIMEOUT):
        """Connect Socket."""
        address = (DEFAULT_IP, DEFAULT_PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(tmr)

        try:
            self.sock.connect(address)
        except socket.error as err:
            # EWOULDBLOCK is not an error, as the socket is non-blocking
            if err.errno != errno.EWOULDBLOCK:
                raise

        self.sock.setblocking(TCP_SOCKET_BLOCKING)
        return True

    def close(self):
        """Close Socket."""
        self.sock.close()

    def sleep(self, tmr):
        """Sleep Method."""
        time.sleep(tmr / 1000)

    def read(self, strmsg):
        """CoraCom Read Method."""
        try:
            self.sock.send(strmsg.encode())
            bytesmsg = self.sock.recv(BUFFER_SIZE)
        except BaseException:
            return 'ERROR'
        return bytesmsg.decode('UTF-8')

    def write(self, strmsg):
        """CoraCom Write Method."""
        try:
            self.sock.send(strmsg.encode('UTF-8'))
            self.sock.recv(BUFFER_SIZE)
        except BaseException:
            return 'ERROR'

    def ncprint(self, strmsg):
        """CoraCom Print Method."""
        try:
            self.sock.send(strmsg.encode('UTF-8'))
            self.sock.recv(BUFFER_SIZE)
        except BaseException:
            return 'ERROR'

    def alert(self, strmsg):
        """CoraCom Alert Method."""
        try:
            self.sock.send(strmsg.encode('UTF-8'))
            self.sock.recv(BUFFER_SIZE)
        except BaseException:
            return 'ERROR'


class _WrapPyCoraCom(CoraCOM):
    """
    Get COM Server Class ID.
    import pythoncom
    print(pythoncom.CreateGuid())
    """

    _reg_desc_ = "Python COM Server"
    # _reg_clsid_ = '{8780D017-BB63-42AE-8DAC-6D5C6CE4FFC9}'
    _reg_clsid_ = pythoncom.CreateGuid()
    _reg_progid_ = "Cora.PyNCTool"
    _public_methods_ = ['sleep', 'open', 'read', 'write', 'ncprint', 'alert', 'close']


if __name__ == '__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(_WrapPyCoraCom)
    input()
    # CORACOM = CoraCOM()
    # CORACOM.open()
    # CORACOM.sleep(1000)
    # print(CORACOM.read('Hello'))
    # CORACOM.write('World')
    # CORACOM.close()
