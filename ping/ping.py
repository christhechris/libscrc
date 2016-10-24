# -*- coding:utf8 -*-
""" ping """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  File's read and search.
# History:  2016/06/12  V1.0.0[Heyn]
#           2016/10/24  V1.0.1[Heyn]

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import re
import time
import locale
import socket
import platform


from subprocess import Popen, PIPE


def get_os():
    """Get OS Type."""
    ost = platform.system()
    if ost == "Windows":
        return "n"
    else:
        return "c"

def invoke_ping(addr):
    """Ping command."""
    cmd = ["ping", "-{op}".format(op=get_os()), "1", addr]

    ret = None
    try:
        ret = Popen(cmd, bufsize=1024, stdout=PIPE)
    except ValueError:
        print('ERROR occur in invoke_ping: ' + addr)
    return ret

def check_online(popen_obj):
    """Send ping command and get ping echo check host online"""
    echo = popen_obj.communicate()[0].decode(
        locale.getdefaultlocale()[1]).split('\n')

    if len(echo) >= 3:
        findlist = re.findall('\\d+(?=ms)|(?<=TTL\\=)\\d+', echo[2])
        if len(findlist) == 2:
            return (int(findlist[0]), int(findlist[1]))

    return tuple()


def ping_scan(dst):
    """Scan ping command."""
    oks = []
    scq = {}
    net_addr = dst.split('.')
    for i in range(0, 256):
        net_addr[3] = str(i)
        tmp = invoke_ping('.'.join(net_addr))
        if not isinstance(tmp, int):
            scq[i] = tmp

    while len(scq) != 0:
        to_be_removed = []
        for key, val in scq.items():
            if val.poll() != None:
                ret = check_online(val)
                if len(ret) > 0:
                    net_addr[3] = str(key)
                    oks.append((key, ret))
                to_be_removed.append(key)
        for i in to_be_removed:
            scq.pop(i)
    return oks


if __name__ == '__main__':
    START_TIME = time.clock()
    DST_NET = socket.gethostbyname(socket.gethostname())
    ONLINE_LIST = ping_scan(DST_NET)
    ONLINE_LIST.sort()
    PREFIX = '.'.join(DST_NET.split('.')[0:3])
    for item in ONLINE_LIST:
        fmt = '%-15s time=%-5dms   ttl=%d'
        print(fmt % (PREFIX + '.' + str(item[0]), item[1][0], item[1][1]))
    print('%d hosts on line' % len(ONLINE_LIST))
    print('Process time: %lfs' % (time.clock() - START_TIME))
