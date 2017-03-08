# -*- coding:UTF-8 -*-
""" PBox XML Syntax Resolve."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn
# Program:  PBox XML
# History:  2017/02/20 V1.0.0[Heyn]
#           2017/03/08 V1.0.1[Heyn] New get_config() return values Dict->Items->itemSize

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
        Notes:
                    2017-02-20 V1.0[Heyn]
                    2017-03-08 V1.1[Heyn]
        """
        xmllist = []

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
                xmldict = dict(table_name=model.attrib['n'],\
                               devicedriver=model.attrib['devicedriver'],\
                               config=model.attrib['config'],\
                               Items=[],\
                               Pbox='')

            dicts = {'BOOLEAN': 'B08', 'BYTE': 'B08', 'int16_t': 'S16', 'STRING' : 'S16',
                     'int32_t': 'S32', 'DOUBLE': 'D32', 'WORD': 'S32', 'FLOAT': 'F16'}

            itemdict = dict(itemName='DT0', itemType='int16_t', itemSize=1, itemValue=[3, 0, 'S16'])

            for items in child.iter('dataItem'):
                itemlist = items.attrib['config'].split(';')
                itemdict.update(itemName=items.attrib['n'])
                itemdict.update(itemType=itemlist[4])

                if 'STRING' in itemlist[4]:
                    itemdict.update(itemSize=int(itemlist[4][-2:]))
                    itemlist[4] = 'STRING'
                else:
                    itemdict.update(itemSize=1)

                # itemdict['itemValue'] = [function code, register address, data type]
                itemdict.update(itemValue=[int(itemlist[1]), \
                                           int(itemlist[2]), \
                                           dicts.get(itemlist[4], 'S16')])
                xmldict['Items'].append(itemdict.copy())

            xmldict.update(Pbox=self.get_pbox())
            xmllist.append(xmldict.copy())
        return xmllist

    def get_pbox(self, path='/www/pages/htdocs/conf/AnyLink.xml'):
        """Get Pbox configure."""
        xmldict = dict(WAN=dict(dhcp='NO',\
                                ip='192.168.5.13',\
                                gatway='192.168.5.1',\
                                mask='255.255.255.0',\
                                dns='8.8.8.8'), \
                       CloudInfo='47.93.79.77',\
                       TimeZone='UTC-8')

        try:
            tree = PBET.parse(path)
            root = tree.getroot()
        except BaseException:
            print("Error:cannot parse file : %s." % path)
            return xmldict

        # <CloudInfo><Address>47.93.79.77</Address></CloudInfo>
        # <TimeZoneInfo>
        #     <TimeZone>UTC</TimeZone>
        # </TimeZoneInfo>

        for child in root:
            for items in child.iter('WAN'):
                xmldict.update(WAN=items.attrib.copy())
            for items in child.iter('CloudInfo'):
                xmldict.update(CloudInfo=items.find('Address').text)
            for items in child.iter('TimeZoneInfo'):
                xmldict.update(TimeZone=items.find('TimeZone').text)

        return xmldict

# if __name__ == '__main__':
#     XML = PboxXML('./config.xml')
#     print(XML.get_config())
#     print(XML.get_pbox())
