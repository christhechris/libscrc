# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  ping
# History:  2016.06.12  Ver1.0 [Windows]
 

import os
import sys
import time
import platform
import threading 
  
def get_os(): 
    ''''' 
    get os 类型 
    '''
    os = platform.system() 
    if os == "Windows": 
        return "n"
    else: 
        return "c"
    
def ping_ip(ip_str): 
    cmd = ["ping", "-{op}".format(op=get_os()), "1", ip_str] 
    output = os.popen(" ".join(cmd)).readlines()
    #print (output)
    
    flag = False
    for line in list(output): 
        if not line: 
            continue
        if str(line).upper().find("TTL") >=0: 
            flag = True
            break
    if flag: 
        print ("ip: %s is ok ***"%ip_str )
  
def find_ip(ip_prefix): 
    ''''' 
    给出当前的127.0.0 ，然后扫描整个段所有地址 
    '''
    for i in range(1,256): 
        ip = '%s.%s'%(ip_prefix,i) 
        threading.Thread(target = ping_ip,args = (ip,)).start() 
        time.sleep(0.3) 
    
if __name__ == "__main__": 
    print ("start time %s"%time.ctime())
    commandargs = sys.argv[1:] 
    args = "".join(commandargs)   
    
    ip_prefix = '.'.join(args.split('.')[:-1])
    ip_prefix = "192.168.0"
    find_ip(ip_prefix) 
    print ("end time %s"%time.ctime())
