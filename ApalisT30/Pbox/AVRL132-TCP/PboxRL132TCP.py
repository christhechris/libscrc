# -*- coding:utf-8 -*-
"""
NM-EJA5A NM-EJA6A AV132
NM-EJR5A NM-EJR6A RL132
"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:
# History:  2017/03/03 V1.0.0[Heyn]

import errno
import socket

class PboxRL132:
    """Pbox NM-EJR5A NM-EJR6A RL132"""

    def __init__(self, addr='192.168.5.102', port=49152, block=True):
        super(PboxRL132, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(block)    # 0 = noBlocking 1 = Blocking
        if block is False:
            self.sock.settimeout(3)     # seconds

        self.isopened = False

        try:
            self.sock.connect((addr, port))
            self.isopened = True
        except socket.error as err:
            self.isopened = False
            if err.errno != errno.EWOULDBLOCK:
                print(err)

        self.cmdicts = {}
        self.cmdicts['C1M000'] = self.__c1m000__    # 进行生产管理信息（设备累计）的读出
        self.cmdicts['C1M000P'] = self.__c1m000__   # 进行生产管理信息（生产品种）的读出
        self.cmdicts['C1N000'] = self.__c1m000__    # 进行托盘板信息的读出
        self.cmdicts['C1Z000'] = self.__c1m000__    # 进行料架信息的读出
        self.cmdicts['C1R000'] = self.__c1m000__    # 进行转动夹信息的读出

    def __del__(self):
        if self.isopened is True:
            self.sock.close()
        self.isopened = False

    def __send_packet__(self, cmd):
        """Socket (TCP) Send."""
        if self.isopened is False:
            return False

        # instruct(256Bytes) + datasize(4Bytes) + end(3Bytes)
        instruct = cmd + ' ' * (256 - len(cmd)) + '0' * 4 + '0' * 3
        try:
            self.sock.send(instruct.encode(encoding='UTF-8'))
        except BaseException as err:
            print(err)
            return False
        return True

    def __recv_packet__(self):
        """Socket (TCP) Receive"""
        try:
            msg = self.sock.recv(1024)
        except BaseException as err:
            print(err)
            return None

        return msg.decode(encoding='UTF-8')

    def __c1m000__(self, msgdata):
        """C1M000 [Response packet format]
        进行生产管理信息（设备累计）的读出
        C1M000 -> 读出后，设备内的生产管理信息（设备累计的运转信息）不会被清除。
        C1M900 -> 读出后，设备内的生产管理信息（设备累计的运转信息）将被清除。
        return
        SD  --->  2010/09/10 14:04:35   收集开始时间
        ED  --->  2010/09/27 12:25:20   收集结束时间
        PC  --->  0000000059            生产数量
        CC  --->  0000000000            生产回路数量
        AT  --->  003989:40:31          设备运转累计时间
        PT  --->  00068:25:45           电源开启时间
        OT  --->  00000:37:33           设备运转时间
        PR  --->  00066:04:58           设备准备时间
        WL  --->  00000:03:10           基板等待时间
        WU  --->  00000:00:56           基板
        MT  --->  00000:21:01
        TT  --->  00000:05:56
        IT  --->  00000:31:19
        ET  --->  00000:40:52
        OR  --->  000914
        AO  --->  001014
        IR  --->  095647
        TR  --->  100000
        LE  --->  0000000005
        PE  --->  0000000026
        IC  --->  0000000813
        IE  --->  0000000037
        RE  --->  0000000023
        TE  --->  0000000000
        ES  --->  0000000003
        """
        c1m000dict = {}
        for item in msgdata[259:-3].splitlines():
            c1m000dict[item[0:2]] = item[2:]
            print(item[0:2], ' ---> ', item[2:])
        return c1m000dict

    def recv(self):
        """Receive data from RL132"""
        try:
            msg = self.sock.recv(1024)
        except BaseException as err:
            print(err)
            return None

        return msg.decode(encoding='UTF-8')

    def send(self, cmd='C1M000'):
        """Send command to device."""
        dicts = {}

        if self.__send_packet__(cmd) is not True:
            return None

        data = self.__recv_packet__()

        if len(data) < 256 + 4 + 3:
            return None

        dicts = self.cmdicts[cmd](data)

        # self.__send_packet__('A0')
        # data = self.__recv_packet__()

        return dicts
