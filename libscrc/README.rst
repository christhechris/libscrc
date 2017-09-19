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
|            | CCITT      |           |           |
+------------+------------+-----------+-----------+ 
|            | Kermit     |           |           |
+------------+------------+-----------+-----------+ 
|            | Sick       |           |           |
+------------+------------+-----------+-----------+ 
|            | DNP        |           |           |
+------------+------------+-----------+-----------+ 
|            | X25        |           |           |
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
    crc8 = libscrc.verb(b'1234')

* CRC16::

    crc16 = libscrc.ibm(b'1234')  
    crc16 = libscrc.modbus(b'1234')  
    crc16 = libscrc.xmodem(b'1234')  
    crc16 = libscrc.ccitt(b'1234', 0xFFFF)  # poly=0x1021 initvalue=0xFFFF or 0x1D0F
    crc16 = libscrc.kermit(b'1234')  
    crc16 = libscrc.sick(b'1234')  
    crc16 = libscrc.dnp(b'1234')
    crc16 = libscrc.x25(b'1234')

* CRC32::
    
    crc32 = libscrc.fsc(b'1234')
    crc32 = libscrc.crc32(b'1234')

* CRC64::

    crc64 = libscrc.iso(b'1234')
    crc64 = libscrc.ecma182(b'1234')


V0.1.3 (2017-09-19)
+++++++++++++++++++
* New CRC16-X25

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

