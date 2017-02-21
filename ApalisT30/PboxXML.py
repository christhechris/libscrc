# -*- coding:utf8 -*-
""" PBox XML Syntax Resolve."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows
# Author:   Heyn
# Program:  PBox XML
# History:  2017/02/10 V1.0.0[Heyn]


# import xml.etree.ElementTree as PBET
from xml.dom.minidom import parse
import xml.dom.minidom


class PboxXML:
    """P-Box XML"""

    def __init__(self, path='/www/pages/htdocs/conf/config.xml'):
        super(PboxXML, self).__init__()
        try:
            self.tree = xml.dom.minidom.parse(path)
            self.data = self.tree.documentElement
        except BaseException:
            print("Error:cannot parse file : %s." % path)

    def dataitem(self):
        """Get XML Data Items"""
        datalist = []
        dicts = {'BOOLEAN': 'B08', 'BYTE': 'B08', 'int16_t': 'S16',
                 'int32_t': 'S32', 'DOUBLE': 'D32', 'WORD': 'S32'}
        for items in self.data.getElementsByTagName('dataItem'):
            if items.hasAttribute("config"):
                itemlist = items.getAttribute("config").split(';')
                if items.hasAttribute('n'):
                    datalist.append([int(itemlist[1]), int(itemlist[2]), dicts[
                        itemlist[4]], items.getAttribute('n')])
        return datalist

    def driverinfo(self):
        """Get Serial Configure Information."""
        # datalist = []
        for items in self.data.getElementsByTagName('driver'):
            if items.hasAttribute("config"):
                datalist = items.getAttribute("config").split(';')
        print(datalist)

    def devicedriver(self):
        """ Get Device Driver.
            [Modbus-RTU, Modbus-TCP]
        """
        for items in self.data.getElementsByTagName('model'):
            if items.hasAttribute("devicedriver"):
                return items.getAttribute("devicedriver")
        return None

    def items_info(self):
        """Get Items information."""
        datalist = []
        dicts = {}
        for items in self.data.getElementsByTagName('dataItem'):
            if items.hasAttribute("config"):
                itemlist = items.getAttribute("config").split(';')
                dicts['itemType'] = itemlist[4]
                if items.hasAttribute('n'):
                    dicts['itemName'] = items.getAttribute('n')
                datalist.append(dicts.copy())
        return datalist

    def device_name(self):
        """Get Device Name for database's table name."""
        for items in self.data.getElementsByTagName('device'):
            if items.hasAttribute('n'):
                return items.getAttribute('n')
        return None
