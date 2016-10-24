# -*- coding:utf8 -*-
"""Port Scan."""
#!/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Authro:   Heyn
# Program:  Scan port
# History:  2016.05.04  Ver1.0.0 [Heyn]
#           2016.05.07  Ver1.0.1 [Heyn]
#           2016.10.24  Ver1.0.2 [Heyn] New Process & Threads


import time
import socket
import threading
import multiprocessing


IPADDR = '192.168.0.1'
TIMEOUT = 0.5
THREADS_MAX_NUM = 600


def scan_port(port):
    """Scan Server Port."""
    try:
        if port >= 65535:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((IPADDR, port))
        if result == 0:
            print(IPADDR, u':', port, 'Port is opening!')
            return port
        sock.close()

    except BaseException:
        pass
    return 0


class ScanThread(threading.Thread):
    """Scan Thread."""

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        scan_port(self.port)


def processtask(port):
    """Process Task."""
    threads = []
    for i in range(port, port + THREADS_MAX_NUM):
        thread = ScanThread(i)
        threads.append(thread)

    for threadobj in threads:
        threadobj.start()

    for thread in threads:
        thread.join()

    return

if __name__ == '__main__':

    START_TIME = time.time()
    POOLS = multiprocessing.Pool(8)
    POOLS.map(processtask, map(lambda x: x * THREADS_MAX_NUM,
                               [x for x in range(int(65535 / THREADS_MAX_NUM) + 1)]))
    POOLS.close()
    POOLS.join()
    print('Scan port finished, used time ：%.2fs' % (time.time() - START_TIME))
