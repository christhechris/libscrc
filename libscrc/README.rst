libscrc
=======

|Python3|

libscrc is a library for calculating CRC8 CRC16 CRC32 CRC64.

Installation
------------

* Compile and install the library::

.. code:: bash

    pip3 install libscrc

or

.. code:: bash

    python setup.py build
    python setup.py install

* You will need the administrative privileges to execute the last command.

After installation you can run unit tests to make sure that the library works fine.  Execute::

.. code:: python

    python -m libscrc.testmodbus 
    python -m libscrc.testcrc64 

Usage
-----

In Python 3::

.. code:: python

    import libscrc

    crc16 = libscrc.modbus(b'1234')  # for ASCII  
    crc16 = libscrc.modbus(b'\x01\x02')  # for HEX  

You can also calculate CRC gradually::

.. code:: python

    import libscrc
    crc16 = libscrc.xmodem(b'1234')
    crc16 = libscrc.xmodem(b'5678', crc16)
  
Other projects
--------------

  