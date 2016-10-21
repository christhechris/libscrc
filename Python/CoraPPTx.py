# -*- coding:utf8 -*-
""" PPTx read and write """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PPTx's read and write.
# History:  2016/10/21 V1.0.0[Heyn]

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]
# (4) [See web: https://msdn.microsoft.com/zh-cn/library/ff743835.aspx]


import sys
import logging
import win32com.client
import win32com.client.dynamic


class CoraPPTx:
    """Cora PPTx class."""

    def __init__(self, filepath=sys.path[0], debugLevel=logging.WARNING):
        super(CoraPPTx, self).__init__()
        self.filepath = filepath
        pptx = win32com.client.Dispatch("PowerPoint.Application")
        pptx.Visible = True
        self.presentation = pptx.Presentations.Open(self.filepath)

        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)

    def slide_count(self):
        """Get PPTx Slide Count."""
        return self.presentation.Slides.Count

    def shape_count(self, slide_index):
        """Get Slide's Shape Count."""
        return self.presentation.Slides(slide_index).Shapes.Count

    def shape_type(self, slide_index, shape_index):
        """ Get Shape's type.
        Argument(s):
                    slide_index: Slide Index.
                    shape_index: Shape Index.
        Return(s):
                    =13 [It's a picture]
        Notes:
                    2016-10-21 V1.0.0[Heyn]
        """

        return self.presentation.Slides(slide_index).Shapes(shape_index).Type

    def shape_width_height(self, slide_index):
        """ Get All Shape's Width & Height.
        Argument(s):
                    slide_index: Slide Index.
        Return(s):
                    width : Unit(Pound) 1Pound=0.3528mm
                    height: Unit(Pound) 1Pound=0.3528mm
        Notes:
                    2016-10-21 V1.0.0[Heyn]
        """
        for item in range(1, self.shape_count(slide_index) + 1):
            width = self.presentation.Slides(slide_index).Shapes(item).Width
            height = self.presentation.Slides(slide_index).Shapes(item).Height
            print(width, height)

    def add_image(self, img, slide_index):
        """Add a picture to slide."""
        self.presentation.Slides(slide_index).Shapes.AddPicture(
            img, LinkToFile=False, SaveWithDocument=True, Left=40, Top=100, Width=300, Height=200)

    def del_image(self, slide_index):
        """Delete all picture in slide."""
        while self.shape_count(slide_index) != 0:
            if self.shape_type(slide_index, 1) == 13:
                print('''Find a picture!''')
                # See web: https://msdn.microsoft.com/zh-cn/library/ff745726.aspx
                self.presentation.Slides(slide_index).Shapes(1).Delete()
            else:
                print(self.shape_type(slide_index, 1))

if __name__ == '__main__':

    CORAPPTX = CoraPPTx('D:\\test.pptx', debugLevel=logging.INFO)
    SLIDE_COUNT = CORAPPTX.slide_count()
    print('PPTx Slide = %d' % SLIDE_COUNT)
    SHAPE_COUNT = CORAPPTX.shape_count(1)
    print('PPTx Shape = %d' % SHAPE_COUNT)
    # CORAPPTX.del_image(1)
    # CORAPPTX.del_image(2)
    CORAPPTX.shape_width_height(1)
    # for i in range(3):
    #     CORAPPTX.add_image('d:\\123.png', 1)
