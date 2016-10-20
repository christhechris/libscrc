# -*- coding:utf8 -*-
""" UDP Client"""
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  UDP Client
# History:  2016/10/11
#           [PyLint Message: See web: http://pylint-messages.wikidot.com/]
#           2016/10/20 V1.0.1 New multiprocess\Modify multithread class.

import re
import errno
import socket
import threading
import multiprocessing

IPADDR = '192.168.0.101'
PORTNUM = 54320
BUFFER_SIZE = 1024

PACKETDATA = b'Hello,Amp!'

# UDP_SOCKET_BLOCKING     = 1         # No Blocking (=0), or Blocking (=1)
UDP_SOCKET_NO_BLOCKING = 0

# DONGLESTRING = ''


def udpconnect(server_ip='127.0.0.1'):
    """UDP Connect Server."""

    dongle_message = ''
    address = (server_ip, PORTNUM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock.setblocking(UDP_SOCKET_NO_BLOCKING)
    sock.settimeout(1)
    try:
        sock.connect(address)
    except socket.error as err:
        if err.errno != errno.EWOULDBLOCK:
            return 0
    sock.send(PACKETDATA)
    try:
        dongle_message = sock.recv(BUFFER_SIZE)
    except socket.error as err:
        sock.close()
        return ''

    sock.close()
    donglestr = dongle_message.decode() + ',' + server_ip

    return donglestr


class UdpThread(threading.Thread):
    """UDP Thread."""

    def __init__(self, funclist=None):
        threading.Thread.__init__(self)
        self.funclist = funclist
        self.threads = []
        self.retlist = 0

    def start(self):
        self.retlist = []

        for funcdict in self.funclist:
            new_arg_list = []
            new_arg_list.append(funcdict["func"])
            for arg in funcdict["args"]:
                new_arg_list.append(arg)
            new_arg_tuple = tuple(new_arg_list)

            ths = threading.Thread(target=self.trace_func, args=new_arg_tuple)
            self.threads.append(ths)

        for threadobj in self.threads:
            threadobj.start()

        for threadobj in self.threads:
            threadobj.join()

    def trace_func(self, func, *args, **kwargs):
        """Thread return value"""
        ret = func(*args, **kwargs)
        if ret != '':
            self.retlist.append(ret)

def broadcast(broadip=('255.255.255.255', PORTNUM)):
    """ UDP BroadCast Client"""

    server_message = ''
    loacladdr = ('0.0.0.0', 10013)
    sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sockudp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sockudp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockudp.settimeout(0.5)
    sockudp.bind(loacladdr)
    sockudp.sendto(PACKETDATA, broadip)
    try:
        server_message = sockudp.recv(BUFFER_SIZE)
    except BaseException:
        return ''
    server_message = server_message.decode() + '##'
    print(server_message)
    return server_message

if __name__ == '__main__':
    # broadcast()

    LOCALIP = socket.gethostbyname(socket.gethostname())
    LOCALIP = re.sub(r'[^\.][\d]{1,3}$', '', LOCALIP)

    RETLIST = []
    THREADPOOL = []

    for i in range(10):
        # THREADPOOL.append({"func":udpconnect, "args":(LOCALIP + str(i),)})
        THREADPOOL.append({"func":udpconnect, "args":('192.168.0.101',)})

    UDPTH = UdpThread(THREADPOOL)
    UDPTH.start()
    RETLIST.extend(UDPTH.retlist)

    # MultiProcess Test.
    # MAX_PROCESS = 10
    # IPARRAY = []
    # POOL = multiprocessing.Pool(MAX_PROCESS)
    # for i in range(MAX_PROCESS):
    #     # IPARRAY.append(LOCALIP + str(i))
    #     IPARRAY.append('192.168.0.101')

    # RETLIST = POOL.map(udpconnect, IPARRAY)
    # POOL.close()
    # POOL.join()

    for item in RETLIST:
        print(item)
    print(len(RETLIST))
