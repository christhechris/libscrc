# -*- coding:utf-8 -*-
""" PBox Tool """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  PBox Tool.
# History:  2017-12-01 V1.0.0 [Heyn]
#           2017-12-04 V1.0.1 [Heyn] pyinstaller -F -w --onefile Panasert.py --icon 513.ico
#                                    pyuic5 -o D:\Python\Tools\Panasert\MainWindows.py -x D:\Python\Tools\Panasert\MainWindows.ui
#           2017-12-05 V1.0.2 [Heyn] Optimized code.

import sys
import time
import logging
import threading
import ipaddress

from MainWindows import Ui_MainWindow
from PBoxPanasert import PBoxPanasertTCP

from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem


FORMATOPT = '[%(asctime)s] %(message)s'
logging.basicConfig(filename='logging.txt', level=logging.ERROR, format=FORMATOPT)


class PboxTool(QMainWindow, Ui_MainWindow):
    """PBox tool class."""
    # pylint: disable=C0103
    # pylint: disable=C0301
    signalwidgetupdate = pyqtSignal(dict)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self._order = 'C1M000'
        self._period = 0

        # # Property
        self._line_edit_property()
        self._checkbox_property()
        self._combobox_property()
        self._pushbutton_property()
        self._table_widget_property()

        self.signalwidgetupdate.connect(self.__slot_tablewidgetupdate)

        # # Init.
        self.panasertcp = PBoxPanasertTCP()
        self.btnstart_flag = False
        self.BtnStart.setEnabled(False)

    def closeEvent(self, event):
        """ PyQt Close Event. """
        self.panasertcp.disconnect()
        event.accept()

    def keyPressEvent(self, event):
        """ PyQt keyPress Event. """
        pass

    def _pushbutton_property(self):
        """ PushButton Property. """

        self.BtnStart.clicked.connect(self.btn_start)
        self.BtnConnect.clicked.connect(self.btn_connect)

    def _combobox_property(self):
        """ ComboBox Property. """
        # Commands init.
        self.comboBoxOrders.addItems(['C1M000', 'C1M000P', 'C1N000', 'C1Z000', 'C3'])
        self.comboBoxOrders.setCurrentIndex(1)
        self.comboBoxOrders.currentIndexChanged.connect(self._slot_indexchange_order)
        self._slot_indexchange_order()
        self._order = self.comboBoxOrders.currentText()
        # Period init.
        self.comboBoxPeriod.addItems(['0', '1', '5', '10', '30', '60', '120', '300'])
        self.comboBoxPeriod.currentIndexChanged.connect(self._slot_indexchange_period)

    def _line_edit_property(self):
        """ lineEdit Property. """
        self.lineEditPort.setInputMask('99999')
        self.lineEditIP.setInputMask('999.999.999.999')

        self.lineEditPort.setPlaceholderText('49152')

        self.lineEditPort.setText('54321')
        self.lineEditIP.setText('192.168.11.1')

        self.lineEditProgName.setMaxLength(16)
        self.lineEditProgName.setEnabled(False)

    def _table_widget_property(self):
        """ QTableWidget Property. """
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setSortingEnabled(False)

        # # UI TableWidget
        self.tableWidget.setHorizontalHeaderLabels(['Value'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # Last column autosize
        self.tableWidget.show()


    def _checkbox_property(self):
        """ QCheckBox Property. """
        self.checkBoxSaveLog.stateChanged.connect(self._slot_checkbox_state)

    def _slot_checkbox_state(self):
        """ CheckBox Signals. """
        if self.checkBoxSaveLog.isChecked():
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.getLogger().setLevel(logging.ERROR)

    def _slot_indexchange_order(self):
        """ ComboBox Signals. """
        self._order = self.comboBoxOrders.currentText()
        self.lineEditProgName.clear()

        if 'C1M000P' in self._order:
            self.lineEditProgName.setEnabled(True)
            self.lineEditProgName.setMaxLength(15)
            self.lineEditProgName.setPlaceholderText('203082A')
        elif 'C3' in self._order:
            self.lineEditProgName.setEnabled(True)
            self.lineEditProgName.setMaxLength(16)
            self.lineEditProgName.setPlaceholderText('(P.D.C)xxx...xxx')
        else:
            self.lineEditProgName.setPlaceholderText('')
            self.lineEditProgName.setEnabled(False)

    def _slot_indexchange_period(self):
        self._period = int(self.comboBoxPeriod.currentText())

    def btn_connect_status(self, enable=True):
        """ Connect button's status. """
        self.BtnStart.setEnabled(enable)
        self.lineEditIP.setEnabled(not enable)
        self.lineEditPort.setEnabled(not enable)
        self.BtnConnect.setText('Disconnect' if enable else 'Connect')

    def btn_start_status(self, enable=True):
        """ Start button's status. """
        self.btnstart_flag = enable
        self.BtnConnect.setEnabled(not enable)
        self.comboBoxOrders.setEnabled(not enable)
        self.comboBoxPeriod.setEnabled(not enable)
        self.checkBoxSaveLog.setEnabled(not enable)
        self.lineEditProgName.setEnabled(not enable if ('C1M000P' in self._order) or ('C3' in self._order) else False)
        self.BtnStart.setText('Stop(&O)' if enable else 'Start(&S)')

    def btn_connect(self):
        """ Connect to PBox. """
        try:
            ipaddr = str(self.lineEditIP.text().strip())
            ipaddress.ip_address(ipaddr)
        except ValueError as err:
            QMessageBox.warning(self, 'PBoxTool', '%s'%err)
            return False

        if self.lineEditPort.text().strip() == '':
            QMessageBox.warning(self, 'PBoxTool', 'Port number can not be empty')
            return False

        port = int(self.lineEditPort.text().strip())

        if not 0 < port <= 65535:
            QMessageBox.warning(self, 'PBoxTool', 'Port range (1 - 65535)')
            return False

        if self.panasertcp.isopened:
            self.panasertcp.disconnect()
            self.btn_connect_status(False)
            return True

        self.BtnConnect.setText('Disconnect')
        self.panasertcp.connect(ipaddr, port, block=False)
        if self.panasertcp.isopened is False:
            QMessageBox.warning(self, 'PBoxTool', 'Connect <%s:%d> failure!'%(ipaddr, port))
        self.btn_connect_status(self.panasertcp.isopened)

    def btn_start(self):
        """ Start Collect Data From Device. """
        self.btnstart_flag = not self.btnstart_flag
        self._order = self.comboBoxOrders.currentText() + self.lineEditProgName.text().strip()

        if self.btnstart_flag:
            threads = threading.Thread(target=self.worker)
            threads.start()

        self.btn_start_status(not self.btnstart_flag if self._period == 0 else self.btnstart_flag)

    def worker(self):
        """ Thread worker. """
        while self.btnstart_flag and self.panasertcp.isopened:
            self.signalwidgetupdate.emit(self.panasertcp.getdata(self._order))
            time.sleep(self._period)

        if self.panasertcp.isopened is False:
            self.panasertcp.disconnect()
            self.btn_connect_status(False)
            self.btn_start_status(False)


    def __slot_tablewidgetupdate(self, msgdict):
        """Show information to widgets"""
        self.tableWidget.setRowCount(0)
        logging.info(msgdict)

        for index, item in enumerate(msgdict.get('data').splitlines()):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(item))

APP = QApplication(sys.argv)
DLG = PboxTool()

ICON = QIcon()
ICON.addPixmap(QPixmap("513.ico"), QIcon.Normal, QIcon.Off)
DLG.setWindowIcon(ICON)

DLG.show()
sys.exit(APP.exec_())
