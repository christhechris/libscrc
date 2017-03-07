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
import struct
import logging
import logging.config

class PboxRL132:
    """Pbox NM-EJR5A NM-EJR6A RL132"""

    def __init__(self):
        super(PboxRL132, self).__init__()
        logging.config.fileConfig("../../etc/logging.config")
        self.logger = logging.getLogger("AVRL132")

        self.sock = None
        self.isopened = False

        self.cmdicts = {}
        self.cmdicts['C1M000'] = self.__c1m000__    # 进行生产管理信息（设备累计）的读出
        self.cmdicts['C1M000P'] = self.__c1m000p__  # 进行生产管理信息（生产品种）的读出
        self.cmdicts['C1N000'] = self.__c1n000__    # 进行托盘板信息的读出
        self.cmdicts['C1Z000'] = self.__c1z000__    # 进行料架信息的读出
        self.cmdicts['C1R000'] = self.__c1r000__    # 进行转动夹信息的读出 (仅仅AV132)

        self.cmdicts['C2ST'] = self.__c2st__        # 装置状态

    def __del__(self):
        if self.isopened is True:
            self.sock.close()
        self.isopened = False

    def open(self, addr='192.168.5.102', port=49152, block=True):
        """Open Socket"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(block)    # 0 = noBlocking 1 = Blocking
        if block is False:
            self.sock.settimeout(3)     # seconds

        self.isopened = False

        try:
            self.sock.connect((addr, port))
            self.isopened = True
        except socket.error as err:
            self.close()
            if err.errno != errno.EWOULDBLOCK:
                self.logger.error(err)

        self.logger.debug('IP=%s:%d Blocking=%d', addr, port, block)
        return self.isopened

    def close(self):
        """Close Sokcet"""
        self.isopened = False
        self.sock.close()

    def __send_packet__(self, cmd):
        """Socket (TCP) Send."""
        if self.isopened is False:
            self.logger.warning('TCP Socket is not open.')
            return False

        # instruct(256Bytes) + datasize(4Bytes) + end(3Bytes)
        instruct = cmd + ' ' * (256 - len(cmd)) + '0' * 4 + '0' * 3
        try:
            self.sock.send(instruct.encode(encoding='UTF-8'))
        except BaseException as err:
            self.close()
            self.logger.error(err)
            return False
        return True

    def __recv_packet__(self, cmd):
        """Socket (TCP) Receive"""
        dicts = {'cmds' : 'A0', 'data' : '', 'lens':'0'}
        tuples = ('D0', 'D1', 'A0', 'A2', 'A3', 'A4E00', 'A4E01')

        if self.__send_packet__(cmd) is not True:
            return None

        if cmd == 'A2':
            return None

        try:
            msg = self.sock.recv(1024).decode(encoding='UTF-8')
        except BaseException as err:
            self.close()
            self.logger.error(err)
            return None

        if len(msg) < 256 + 4 + 3:
            self.logger.warning('Receive packet length error!')
            return None

        header = msg[0:256].strip(' ')
        if header not in tuples:
            self.logger.warning('Receive packet header[%s] error!', header)
            return None

        dicts['cmds'] = header
        # dicts['lens'] = msg[256:260]
        dicts['lens'] = struct.unpack("l", bytes(msg[256:260], encoding='UTF-8'))[0]
        dicts['data'] = msg[260:-3]

        # Determine whether the received data length is correct
        if dicts['cmds'] == 'D0' or dicts['cmds'] == 'D1':
            if len(dicts['data']) != (dicts['lens']):
                self.logger.warning('The length of the received data is error!')
                return None

        return dicts

    def recv(self):
        """Receive data from RL132
        TODO:
        """
        try:
            msg = self.sock.recv(1024)
        except BaseException as err:
            self.logger.error(err)
            return None

        return msg.decode(encoding='UTF-8')

    def send(self, cmd='C1M000'):
        """Send command to device."""
        if cmd not in self.cmdicts:
            self.logger.error('Command does not support. [%s]!', cmd)
            return None

        return self.cmdicts[cmd](self.__recv_packet__(cmd))

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

        if msgdata is None or ((msgdata['cmds'] > 'D0') - (msgdata['cmds'] < 'D0') == -1):
            self.logger.error('C1M instruct error')
            return None

        c1m000dict = {}
        for item in msgdata['data'].splitlines():
            c1m000dict[item[0:2]] = item[2:]
            self.logger.debug('%s --> %s', item[0:2], item[2:])

        while True:
            data = self.__recv_packet__('A0')
            if data is None or data['cmds'] == 'A2':
                break
            for item in data['data'].splitlines():
                c1m000dict[item[0:2]] = item[2:]
                self.logger.debug('%s --> %s', item[0:2], item[2:])

        return c1m000dict

    def __c2st__(self, msgdata):
        """ 取得装置状态(使用的端口1)  m m n
            n     -> 0: 在线 1: 远程
            m m   ->00: Run 状态
            m m   ->01: Ready (准备) 状态
            m m   ->02: Error (出错停止) 状态
            msgdata instruct(256Bytes) + datasize(4Byte) + Data(NBytes) + EOF(3Bytes)
        """

        if msgdata is None or ((msgdata['cmds'] > 'D1') - (msgdata['cmds'] < 'D1') == -1):
            self.logger.error('C2ST instruct error.')
            return None

        c2stdict = {}
        c2stdict['Status'] = msgdata['data']
        if self.__send_packet__('A2') is False:
            return None

        self.logger.debug('C2ST --> %s', c2stdict)
        return c2stdict

    def __c1m000p__(self, msgdata):
        """进行生产管理信息（生产品种）的读出"""
        self.logger.debug('C1M000P --> %s', msgdata)

    def __c1n000__(self, msgdata):
        """进行托盘板信息的读出"""
        self.logger.debug('C1N000 --> %s', msgdata)

    def __c1z000__(self, msgdata):
        """进行料架信息的读出"""
        self.logger.debug('C1Z000 --> %s', msgdata)

    def __c1r000__(self, msgdata):
        """进行转动夹信息的读出 (仅仅AV132)"""
        self.logger.debug('C1R000 --> %s', msgdata)
