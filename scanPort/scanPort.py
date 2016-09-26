# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Authro:   Heyn
# Program:  Scan port
# History:  2016.05.04  Ver1.0 [Windows]
#           2016.05.07  Ver1.1 [Windows]
 
import sys, socket, time, threading

TIMEOUT = 1

def pingPort(ip, port, timeout = TIMEOUT):
    """
    """
    global portList
    try:
        if port >= 65535:
            print ('Scan port over!')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result=s.connect_ex((ip,port))
        if result == 0 :
            #print  (ip,u':',port,'Port is opening!')
            portList.append(port)
        s.close()
        
    except Exception as e :
        print ('Scan port error : %s' %e)


class Scan(threading.Thread):
    """
    """
    
    def __init__(self, ip, timeout):
        """
        """
        threading.Thread.__init__(self)
        self.ip = ip
        self.timeout = timeout
        
    def run(self):
        """
        """
        global mutex, portBegin, portEnd
        threadname = threading.currentThread().getName()
        while True:
            mutex.acquire()
            portBegin += 1
            if (portBegin > portEnd) :
                mutex.release()
                break;
            mutex.release()
        pingPort(self.ip, portBegin, self.timeout)
            
def scanUrl(url, p_begin, p_end, timeout):
    """
    """
    global mutex, portBegin, portEnd, portList
    threads = []
    portList = []
    mutex=threading.Lock()
    ip = str(socket.gethostbyname(url))
    print ('Scan start %s' % ip ," port:[from %d"%p_begin,"to %d]"%p_end)
    start_time=time.time()

    portBegin = p_begin
    portEnd = p_end
    for i in range(100):
        thread = Scan(ip,timeout)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        
    print ('Scan port finished, used time ：%.2fs' %(time.time()-start_time))

    if portList:
        portList.sort()
        print ("On host \"",url,"\" port:[ ",end="")
        for port in portList:
            print (port," ", end="")
        print ("] is opened.")
    else :
        print ("On host \"",url,"\" can't find any port.")
    
if __name__=='__main__':
    url = input('Input the ip you want to scan:\n')
    scanUrl(url,0,100,0.1)
