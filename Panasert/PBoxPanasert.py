# -*- coding:utf-8 -*-
"""
NM-EJA5A NM-EJA6A AV132
NM-EJR5A NM-EJR6A RL132
"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  For Panasonic RL132/AV132 TCP/IP
# History:  2017-03-03 V1.0.0 [Heyn]
#           2017-03-30 V1.0.1 [Heyn]
#           2017-12-04 V1.0.2 [Heyn] Optimized code.


import socket
import struct
import logging
import binascii

def catch_exception(origin_func):
    """ Catch exception. """
    def wrapper(self, *args, **kwargs):
        """Wrapper."""
        try:
            self.isopened = True
            return origin_func(self, *args, **kwargs)
        except BaseException as msg:
            logging.error('[ERROR] %s an exception raised. *** %s ***', origin_func, str(msg))
            self.isopened = False
            return False
    return wrapper

class PBoxPanasertTCP:
    """ PBox NM-EJR5A NM-EJR6A RL132. """

    def __init__(self):
        self.__sock = None
        self.isopened = False
        self.__blocksize = 2048

    def __del__(self):
        if self.isopened is True:
            self.isopened = False
            self.__sock.close()

    @catch_exception
    def connect(self, addr='192.168.5.102', port=49152, block=True):
        """ Open Socket & connect device. """
        logging.debug('IP=%s:%d Blocking=%d', addr, port, block)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setblocking(block)    # False = noBlocking True = Blocking
        if block is False:
            self.__sock.settimeout(3)     # seconds

        self.__sock.connect((addr, port))
        return True

    def disconnect(self):
        """Close Sokcet"""
        if self.isopened is True:
            self.__sock.close()
        self.isopened = False

    @catch_exception
    def __send_packet(self, cmd='C1M000'):
        """ Socket (TCP) Send.
            # instruct(256Bytes) + datasize(4Bytes) + end(3Bytes)
        """
        if len(cmd) > 256:
            logging.error('The command maximum length of more than 256.!!!')
            return False

        instruct = cmd + ' ' * (256 - len(cmd)) + '\x00\x00\x00\x00' + '\x00'*3
        self.__sock.send(instruct.encode(encoding='UTF-8'))
        logging.info('SND(string) -> ' + instruct)
        logging.debug(binascii.b2a_hex(instruct.encode('UTF-8')))

        return True

    @catch_exception
    def __recv_packet(self):
        """ Socket (TCP) Receive.
            instruct(256Bytes) + datasize(4Bytes) = 260(Bytes)
        """
        msgdict = dict(cmds='', data='', lens=0)
        instruct = self.__sock.recv(260)
        logging.info('RCV(string) <- ' + str(instruct))
        if len(instruct) != 260:
            return msgdict

        msgdict['cmds'] = instruct[0:256].decode('UTF-8').strip(' ')
        if msgdict['cmds'] not in ('D0', 'D1', 'A0', 'A2', 'A3', 'A4E00', 'A4E01'):
            return msgdict

        try:
            msgdict['lens'] = struct.unpack('>L', bytes(instruct[256:260]))[0]
        except BaseException:
            msgdict['lens'] = 0
            return msgdict


        logging.debug('Data Size = %d', msgdict['lens'])

        while True:
            msgdict['data'] = msgdict['data'] + self.__sock.recv(self.__blocksize).decode('UTF-8')
            if len(msgdict['data']) >= msgdict['lens']:
                break
        logging.info('RCV(Data) <- ' + str(msgdict))
        return msgdict

    def getdata(self, cmd='C1M000'):
        """ Get data from RL132. """
        msgdict = dict(cmds='', data='', lens=0)

        if self.__send_packet(cmd) is False:
            return msgdict

        datadict = self.__recv_packet()

        if isinstance(datadict, dict) is False:
            return msgdict

        msgdict.update(datadict)

        if msgdict['cmds'] in ['A4E00', 'A4E01']:
            msgdict['data'] = msgdict['data'] + 'Instruction ERROR!!'
            return msgdict

        if self.__send_packet('A0') is False:
            return msgdict

        self.__recv_packet()
        return msgdict
