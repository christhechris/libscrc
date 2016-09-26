# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Threading
# History:  2016.06.12  Ver1.0 [Windows]
 

import threading 
  
class hzThread(threading.Thread):
    """
    """

    def __init__(self, threadID, name):
        threading.Thread.__init__ (self)
        
    def run(self):
