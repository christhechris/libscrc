# -*- coding:utf-8 -*-
""" Txt to STL"""
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Txt to STL.
# History:  2017/10/25 V1.0 [Heyn]


import stl
import logging
import numpy as np
from stl import mesh

from matplotlib import pyplot
from mpl_toolkits import mplot3d


STL_HORIZONTAL = 0.0
STL_VERTICAL = 1.0

class CoraTXTtoSTL:
    """"""

    def __init__(self):
        self.zonedata = []
        self.zonerows = self.zonecolumns = 0
        self._npzonedata = self._common_point = self._meshe = None

    def load(self, filepath):
        """ Load *.txt to memory.
            data = [index, data*8, horizontal, vertical]
        """

        with open(filepath, 'r') as txt:
            for line in txt.readlines():
                data = line.strip('\r\n').strip().split(',')
                if len(data) == 9:
                    data.extend([STL_HORIZONTAL, STL_VERTICAL])
                    self.zonedata.append(list(map(float, data)))
                else:
                    logging.error('Zone data is error ' + line)

        self._npzonedata = np.array(self.zonedata)
        self.zonerows, self.zonecolumns = self._npzonedata.shape
        return self._npzonedata

    def meshobject(self, npdata):
        """ Generate mesh object. """
        meshdata = np.zeros(8*self.zonerows, dtype=mesh.Mesh.dtype)

        self._calc_common_point()

        for row in range(0, self.zonerows):
            meshdata['vectors'][row*8 + 0] = npdata[row][np.array([[1, 2, 9], [3, 4, 9], [3, 4, 10]])]     #Back  Face V0
            meshdata['vectors'][row*8 + 1] = npdata[row][np.array([[3, 4, 10], [1, 2, 10], [1, 2, 9]])]    #Back  Face V1

            meshdata['vectors'][row*8 + 2] = npdata[row][np.array([[3, 4, 9], [5, 6, 9], [5, 6, 10]])]     #Right Face V0
            meshdata['vectors'][row*8 + 3] = npdata[row][np.array([[5, 6, 10], [3, 4, 10], [3, 4, 9]])]    #Right Face V1

            meshdata['vectors'][row*8 + 4] = npdata[row][np.array([[5, 6, 9], [7, 8, 9], [7, 8, 10]])]     #Front Face V0
            meshdata['vectors'][row*8 + 5] = npdata[row][np.array([[7, 8, 10], [5, 6, 10], [5, 6, 9]])]    #Front Face V1

            meshdata['vectors'][row*8 + 6] = npdata[row][np.array([[7, 8, 9], [1, 2, 9], [1, 2, 10]])]     #Left  Face V0
            meshdata['vectors'][row*8 + 7] = npdata[row][np.array([[1, 2, 10], [7, 8, 10], [7, 8, 9]])]    #Left  Face V1
        return meshdata

    def plot(self, meshdata):
        """Plot"""
        self._meshe = mesh.Mesh(meshdata.copy())
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self._meshe.vectors))
        # Auto scale to the mesh size
        scale = np.concatenate(self._meshe.points).flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        pyplot.show()

    def save(self, savepath, method='ASCII'):
        """ Save. """
        if method == 'ASCII':
            self._meshe.save(savepath, mode=stl.Mode.ASCII)
        else:
            self._meshe.save(savepath)

    def _calc_common_point(self):
        """"""
        npdata = self._npzonedata.copy()
        print(npdata)

        for row in range(0, self.zonerows-1):
            matrixrow = npdata[row, 1:9].reshape(4, 2)
            for col, item in enumerate(matrixrow):
                for rowx in range(row+1, self.zonerows):
                    matrixrowx = npdata[rowx, 1:9].reshape(4, 2)
                    for colx, itemx in enumerate(matrixrowx):
                        if np.array_equal(item, itemx):
                            point = np.concatenate((np.array([row, col, rowx, colx], dtype='float64'), item))
                            self._common_point = point.copy() if self._common_point is None else np.concatenate((self._common_point, point))


        # total = self._common_point.size
        # self._common_point = self._common_point.reshape(total//6, 6)
        # print(self._common_point)
        # for _, item in enumerate(self._common_point):
        #     x, y = item[4], item[5]
        #     data1 = npdata[int(item[0]), 1:9].reshape(4, 2)
        #     data2 = npdata[int(item[2]), 1:9].reshape(4, 2)
        #     for m, n in zip(data1, data2):
        #         if m[0] == x and m[1] != y:
        #             self._npzonedata[int(item[2]), 1 + int(item[3])*2 + 1] = m[1]
        #         if n[0] == x and n[1] != y:
        #             self._npzonedata[int(item[0]), 1 + int(item[1])*2 + 1] = n[1]

TEST = CoraSTL()
DATA = TEST.load('D:\\Python\\test.txt')
TEST.plot(TEST.meshobject(DATA))
