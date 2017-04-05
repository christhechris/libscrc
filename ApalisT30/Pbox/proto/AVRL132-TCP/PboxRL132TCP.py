# -*- coding:UTF-8 -*-
"""
NM-EJA5A NM-EJA6A AV132
NM-EJR5A NM-EJR6A RL132
"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  Panasonic RL132
# History:  2017/03/03 V1.0.0[Heyn]
#           2017/03/30 V1.0.1[Heyn]

import time
import errno
import socket
import struct
import binascii
import logging
import logging.config

class PboxRL132:
    """Pbox NM-EJR5A NM-EJR6A RL132"""

    def __init__(self):
        super(PboxRL132, self).__init__()
        self.sock = None
        self.isopened = False
        self.blocksize = 2048
        logging.config.fileConfig("logging.config")
        self.logger = logging.getLogger("AVRL132")

    def __del__(self):
        if self.isopened is True:
            self.sock.close()
        self.isopened = False

    def connect(self, addr='192.168.5.102', port=49152, block=True):
        """Open Socket & connect RL132 device."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(block)    # 0 = noBlocking 1 = Blocking
        if block is False:
            self.sock.settimeout(3)     # seconds
        self.isopened = False
        self.logger.debug('IP=%s:%d Blocking=%d', addr, port, block)
        try:
            self.sock.connect((addr, port))
            self.isopened = True
        except socket.error as err:
            self.disconnect()
            if err.errno != errno.EWOULDBLOCK:
                self.logger.error(err)

        return self.isopened

    def disconnect(self):
        """Close Sokcet"""
        self.isopened = False
        # self.sock.close()

    def __send_packet__(self, cmd):
        """Socket (TCP) Send."""
        if self.isopened is False:
            self.logger.warning('RL132 Socket is closed.')
            return False

        # instruct(256Bytes) + datasize(4Bytes) + end(3Bytes)
        instruct = cmd + ' ' * (256 - len(cmd)) + '\x00\x00\x00\x00' + '\x00'*3
        self.logger.debug('SND(string) -> ' + instruct)

        try:
            self.sock.send(instruct.encode(encoding='UTF-8'))
        except BaseException as err:
            self.disconnect()
            self.logger.error(err)
            return False
        else:
            # self.logger.debug('SND(ascii) -> ')
            # self.logger.debug(binascii.b2a_hex(instruct.encode("UTF-8")))
            pass

        return True

    def __recv_packet__(self):
        """Socket (TCP) Receive."""

        try:
            # instruct(256Bytes) + datasize(4Bytes) = 260(Bytes)
            instruct = self.sock.recv(260)
        except BaseException as err:
            self.disconnect()
            self.logger.error(err)
            return None
        else:
            self.logger.debug('RCV(string) <- ' + str(instruct))
            if len(instruct) != 260:
                self.logger.error('Receive packet size error!')
                return None

        command = instruct[0:256].decode('UTF-8').strip(' ')
        tuples = ('D0', 'D1', 'A0', 'A2', 'A3', 'A4E00', 'A4E01')
        if command not in tuples:
            self.logger.error('Receive packet header[%s] error!', command)
            return None

        try:
            package_size = struct.unpack('>L', bytes(instruct[256:260]))[0]
        except BaseException as err:
            package_size = 0
            self.logger.error(err)

        self.logger.debug('Data Size = %d', package_size)

        info = b''
        while True:
            try:
                data = self.sock.recv(self.blocksize)
                info = info + data
                if len(info) >= package_size:
                    break
            except BaseException as err:
                self.disconnect()
                self.logger.error(err)
                return None

        return dict(cmds=command, \
                    data=info.decode('UTF-8'), \
                    lens=package_size)

    def getdata(self, cmd):
        """Get data from RL132."""
        datalist = []
        if self.__send_packet__(cmd) is False:
            return datalist

        # msg = 'SD2014/01/04 08:23:18\r\nED2017/03/30 15:32:31\r\nPC0000009581\r\nCC0000010611\r\nAT000217:43:36\r\nPT00526:23:32\r\nOT00037:49:25\r\nPR00451:45:59\r\nWL00016:16:55\r\nWU00001:41:07\r\nMT00008:59:37\r\nTT00002:31:39\r\nIT00002:13:16\r\nET00004:32:45\r\nOR007185\r\nAO010598\r\nIR099921\r\nTR099971\r\nLE0000000031\r\nPE0000000145\r\nIC0000398554\r\nIE0000000312\r\nRE0000000039\r\nTE0000000113\r\nES0000000187\r\nLU0000000144\r\nLT00000:09:41\r\n*\r\n'
        # datadict = dict(cmds='D0', data=msg, lens=395)

        datadict = self.__recv_packet__()

        if datadict is None or datadict.get('lens') == 0:
            return datalist

        for item in datadict.get('data').splitlines():
            if item[0:2] == '*':
                break
            datalist.append(dict(itemName=item[0:2], value=item[2:]))

            # Debug Start
            # comment = dict(SD='収集スタート日時', ED='収集エンド日時', PC='生産枚数コマンド', \
            #                CC='生産回路数コマンド', WU='基板待ち時間コマンド', PT='電源時間コマンド', \
            #                OT='運転時間コマンド', PR='運転準備時間コマンド', WL='基板待ち時間コマンド', \
            #                MT='メンテナス時間コマンド', TT='トラブル時間コマンド', ET='部品切れ時間コマンド', \
            #                OR='稼動率コマンド', AO='設備稼動率コマンド', IR='挿入率コマンド', \
            #                TR='総合挿入率コマンド', LE='搬送エラー回数コマンド', PE='部品切れ回数コマンド', \
            #                IC='挿入回数コマンド', IE='挿入エラー回数コマンド', RE='リカバリーエラー回数コマンド', \
            #                TE='総合挿入エラー回数コマンド', ES='エラー停止回数コマンド', IT='挿入エラー時間コマンド', \
            #                LT='注記', AT='注記', LU='注記', \
            #                )

            # self.logger.debug('[ ' + item[0:2] + \
            #                   ' -- ' + \
            #                   comment.get(item[0:2]).ljust(30 - len(comment.get(item[0:2]))) + \
            #                   ' ] :  ' + \
            #                    item[2:].lstrip('0:'))
            # Debug End
        self.logger.debug(datadict)
        print(datadict)
        return datalist

# if __name__ == '__main__':
#     RL132 = PboxRL132()
#     RL132.connect('10.78.246.74', 49152, False)
#     # RL132.connect('192.168.3.103', 49152, False)
#     while True:
#         RL132.getdata('C1M000')
#         RL132.getdata('A0')
#         time.sleep(5)
