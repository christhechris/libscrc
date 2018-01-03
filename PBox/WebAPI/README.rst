PBoxWebAPI
==========

PBoxWebAPI is a library for PBox device web interface.

Installation
------------

* Install the library::

    pip3 install PBoxWebAPI

  You will need the administrative privileges to execute the last command.

Usage
-----

  In Python 3::

    from PBoxWebAPI import *


Example
-------
* New Channel::
    params = ['Modbus-TCP', '192.168.3.1', '65535', '500'] or
    params = ['Modbus-RTU', '/dev/ttymxc1', '9600', 'Odd/Even/None', '8', '1', '500']
    webnewchannel(name, params, flag=True)

* New Device::
    webnewdevice(name)

* New Items::
    item = ['python', 'test', '5000', 'a', '0', '1', '1;3;2;1;INT16;0;0;0']
    webnewitem(item)


V1.1.2 (2017-09-14)
+++++++++++++++++++
* Release V1.1.2


Other projects
--------------

