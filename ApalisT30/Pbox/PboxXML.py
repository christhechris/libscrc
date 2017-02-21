# -*- coding:utf8 -*-
""" PBox XML Syntax Resolve."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  PBox XML
# History:  2017/02/20 V1.0.0[Heyn]


import xml.etree.ElementTree as PBET

class PboxXML:
    """P-Box XML"""

    def __init__(self, path='/www/pages/htdocs/conf/config.xml'):
        super(PboxXML, self).__init__()
        try:
            self.tree = PBET.parse(path)
            self.root = self.tree.getroot()
        except BaseException:
            print("Error:cannot parse file : %s." % path)

    def get_config(self):
        """ Get Configure from XML.
        Argument(s):
        Return(s):
                    Dict: { 'table_name'   : '',
                            'devicedriver' : '',
                            'config'       : '',
                            'Items' : [{'itemName' : '',
                                        'itemType' : '',
                                        'itemValue': ['', '', '']
                                        }
                                      ]
                            'Pbox'  :   {
                                            #See : get_pbox
                                        }
                          }
        Notes:
                    2017-02-20 V1.0[Heyn]
        """
        xmllist = []
        xmldict = {}
        for child in self.root:
            for model in child.iter('model'):
                """
                Example:
                <model  n="hello"
                        id="169"
                        d="IDrv.Custom:libDModbus"
                        config="rtu;/dev/ttyO4;9600;None;8;1;STANDARD;200;100;20"
                        devicedriver="Modbus-RTU">
                """
                xmldict['config'] = model.attrib['config']
                xmldict['table_name'] = model.attrib['n']
                xmldict['devicedriver'] = model.attrib['devicedriver']
                xmldict['Items'] = []

            dicts = {'BOOLEAN': 'B08', 'BYTE': 'B08', 'int16_t': 'S16',
                     'int32_t': 'S32', 'DOUBLE': 'D32', 'WORD': 'S32', 'FLOAT': 'F16'}
            itemdict = {}

            for items in child.iter('dataItem'):
                itemlist = items.attrib['config'].split(';')
                itemdict['itemName'] = items.attrib['n']
                itemdict['itemType'] = itemlist[4]
                # itemdict['itemValue'] = [function code, register address, data type]
                itemdict['itemValue'] = [int(itemlist[1]), int(itemlist[2]), dicts[itemlist[4]]]
                xmldict['Items'].append(itemdict.copy())
            xmldict['Pbox'] = self.get_pbox()
            xmllist.append(xmldict.copy())
        return xmllist

    def get_pbox(self, path='/www/pages/htdocs/conf/AnyLink.xml'):
        """Get Pbox configure.
            xmldict {
                    'CloudInfo' : '',
                    'WAN':  {
                                'dhcp': 'NO',
                                'gateway': '192.168.5.1',
                                'dns': '114.114.114.114',
                                'mask': '255.255.255.0',
                                'ip': '192.168.5.126'
                            }
                    }
        """
        try:
            tree = PBET.parse(path)
            root = tree.getroot()
        except BaseException:
            print("Error:cannot parse file : %s." % path)
        xmldict = {}
        # xmldict['CloudInfo'] = root.find('Address').text

        for child in root:
            for items in child.iter('WAN'):
                xmldict['WAN'] = items.attrib.copy()
            for items in child.iter('CloudInfo'):
                xmldict['CloudInfo'] = items.find('Address').text
        return xmldict

# if __name__ == '__main__':
#     XML = PboxXML('./config.xml')
#     print(XML.get_config())
