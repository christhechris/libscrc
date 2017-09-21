libscrc
=======

libscrc is a library for calculating CRC8 CRC16 CRC32 CRC64.

+------------+------------+-----------+-----------+ 
| CRC8       | CRC16      | CRC32     | CRC64     |
+============+============+===========+===========+ 
| Intel      | Modbus     | FSC       | ISO       |
+------------+------------+-----------+-----------+ 
| BCC        | IBM        | FILE      | ECMA182   |
+------------+------------+-----------+-----------+ 
| LRC        | XModem     |           |           |
+------------+------------+-----------+-----------+ 
| MAXIM8     | CCITT      |           |           |
+------------+------------+-----------+-----------+ 
| ROHC       | Kermit     |           |           |
+------------+------------+-----------+-----------+ 
| ITU        | Sick       |           |           |
+------------+------------+-----------+-----------+ 
| CRC8       | DNP        |           |           |
+------------+------------+-----------+-----------+ 
|            | X25        |           |           |
+------------+------------+-----------+-----------+ 
|            | USB        |           |           |
+------------+------------+-----------+-----------+
|            | MAXIM16    |           |           |
+------------+------------+-----------+-----------+
|            | DECT       |           |           |
+------------+------------+-----------+-----------+

Installation
------------

* Compile and install the library::

    pip3 install libscrc

  or::

    python setup.py build
    python setup.py install

  You will need the administrative privileges to execute the last command.

* After installation you can run unit tests to make sure that the library works fine.  Execute::

    python -m libscrc.testmodbus
    python -m libscrc.testcrc64

Usage
-----

  In Python 3::

    import libscrc
    crc16 = libscrc.modbus(b'1234')  # Calculate ASCII of modbus
    crc16 = libscrc.modbus(b'\x01\x02')  # Calculate HEX of modbus

  You can also calculate CRC gradually::

    import libscrc
    crc16 = libscrc.xmodem(b'1234')
    crc16 = libscrc.xmodem(b'5678', crc16)

Example
-------
* CRC8::

    crc8 = libscrc.intel(b'1234')
    crc8 = libscrc.bcc(b'1234')  
    crc8 = libscrc.lrc(b'1234')  
    crc8 = libscrc.maxim8(b'1234')
    crc8 = libscrc.rohc(b'1234')
    crc8 = libscrc.itu(b'1234')
    crc8 = libscrc.crc8(b'1234')

* CRC16::

    crc16 = libscrc.ibm(b'1234')            # poly=0xA001 (default Reversed)  
    crc16 = libscrc.ibm(b'1234', 0x8005)    # poly=0x8005 (Normal)
    crc16 = libscrc.modbus(b'1234')  
    crc16 = libscrc.xmodem(b'1234')  
    crc16 = libscrc.ccitt(b'1234')  
    crc16 = libscrc.ccitt_false(b'1234')  
    crc16 = libscrc.kermit(b'1234')  
    crc16 = libscrc.sick(b'1234')  
    crc16 = libscrc.dnp(b'1234')  
    crc16 = libscrc.x25(b'1234')  
    crc16 = libscrc.usb16(b'1234')  
    crc16 = libscrc.maxim16(b'1234')  
    crc16 = libscrc.dect(b'1234')           # poly=0x0589 (Cordless Telephones)

* CRC32::
    
    crc32 = libscrc.fsc(b'1234')
    crc32 = libscrc.crc32(b'1234')

* CRC64::

    crc64 = libscrc.iso(b'1234')
    crc64 = libscrc.ecma182(b'1234')


V0.1.4 (2017-09-21)
+++++++++++++++++++
* New CRC8-MAXIM8   Poly = 0x31 Initial = 0x00 Xorout=0x00 Refin=True  Refout=True
* New CRC8-ROHC     Poly = 0x07 Initial = 0xFF Xorout=0x00 Refin=True  Refout=True
* New CRC8-ITU      Poly = 0x07 Initial = 0x00 Xorout=0x55 Refin=False Refout=False
* New CRC8-CRC8     Poly = 0x07 Initial = 0x00 Xorout=0x00 Refin=False Refout=False


V0.1.3 (2017-09-19)
+++++++++++++++++++
* New CRC16-X25  
* New CRC16-USB  
* New CRC16-MAXIM16  
* New CRC16-CCITT_FALSE
* New CRC16-DECT

**Bugfixes**
  * Calculate CRC16-IBM of poly = 0x8005 is ERROR.


V0.1.2 (2017-08-22)
+++++++++++++++++++
**Platform Support**
  * Win32
  * Linux_x86_64
  * MacOSX_10_6_intel
  * ARMv7 (Toradex Ixora iMX6 Linux-4.1.41)

**Bugfixes**
  * Coding C99 standard.
  * Python/C API parsing arguments type error in linux.

V0.1.1 (2017-08-20)
+++++++++++++++++++
* New CRC16-NDP and CRC16-SICK

