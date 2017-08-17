------------
Installation
------------

* compile and install the library::

    [Win32 or Ubuntu Linux]  
    # python setup.py build
    # python setup.py install
    * you will need the administrative privileges to execute the last command.

    [ARM imx6(toradex)]  
    # opkg install gcc
    # opkg install gcc-symlinks
    # opkg install binutils

    # gcc version 6.2.1 20161016 (Linaro GCC 6.2-2016.11)

    # CC=gcc LDSHARED='gcc -shared' python setup.py build 
    # CC=gcc LDSHARED='gcc -shared' python setup.py install
    # CC=gcc LDSHARED='gcc -shared' python setup.py build bdist_wheel

-----
Usage
-----

In Python 3::
    import libscrc  
    # ASCII  
    crc16 = libscrc.modbus(b'1234')  
    # HEX  
    crc16 = libscrc.modbus(b'\x01\x02')  
    # Swap Method  
    import struct  
    [ i for i in struct.pack('<H',crc16)]  
  
You can also calculate CRC gradually::
    import libscrc  
    crc16 = libscrc.xmodem(b'1234')  
    crc16 = libscrc.xmodem(b'5678', crc16)  
    print(crc16)  
  
  
Other Example:  
    # CRC8 Method  
    crc8 = libscrc.intel(b'1234')  
    crc8 = libscrc.bcc(b'1234')  
    crc8 = libscrc.lrc(b'1234')  
    crc8 = libscrc.verb(b'1234')  
  
    # CCITT poly=0x1021 initvalue=0xFFFF  
    crc16 = libscrc.ccitt(b'1234', 0xFFFF)  
    # CCITT poly=0x1021 initvalue=0x1D0F  
    crc16 = libscrc.ccitt(b'1234', 0x1D0F)  

    # CCITT Kermit poly=0x8408 initvalue=0x0000  
    crc16 = libscrc.kermit(b'1234')  
    crc16 = libscrc.kermit(b'\x01\x02')  
  
    crc16 = libscrc.ibm(b'1234')  
    crc16 = libscrc.modbus(b'1234')  
    crc16 = libscrc.xmodem(b'1234')  
    crc16 = libscrc.ccitt(b'1234', 0xFFFF)  
    crc16 = libscrc.kermit(b'1234')  
    crc16 = libscrc.sick(b'1234')  
    crc16 = libscrc.dnp(b'1234')  
  
    # Media file (MPEG) and Ethernet frame sequence (FSC)  
    crc32 = libscrc.fsc(b'1234')  
    # Files  
    crc32 = libscrc.crc32(b'1234')  
  
--------------
Other projects
--------------
  
  