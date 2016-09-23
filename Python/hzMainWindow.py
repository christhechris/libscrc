# -*- coding:utf8 -*-
#!/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Qt5 Main Window
# History:  2016-09-24

import sys
import os
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui     import QFont
from PyQt5 import QtGui, uic, QtCore

Ui_MainWindow, QtBaseClass = uic.loadUiType("MainWindows.ui") 

class hzMainWindowsDlg(QMainWindow, Ui_MainWindow) :
    signelStart = QtCore.pyqtSignal(list)
    signeltableWidget = QtCore.pyqtSignal(list)

    def __init__(self, parent=None) :
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # UI textEdit Init
        self.fileExt_textEdit.setText(".c | .h")
        self.fileName_textEdit.setText("*UART*")
        self.keyWords_textEdit.setText("UART")

        self.folderBrowseBtn.clicked.connect(self.folderBrowse)
        self.exportBrowseBtn.clicked.connect(self.exportBrowse)
        self.startBtn.clicked.connect(self.startButton)

        # UI TableWidget
        header = ["Regex","Result"]
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.horizontalHeader().setStretchLastSection(True) # Last column autosize

        # self.tableWidget.setItem(0,0,QTableWidgetItem("Jan1"));

        # newRowCount = self.tableWidget.rowCount()
        # self.tableWidget.insertRow(newRowCount)
        # self.tableWidget.setItem(1,0,QTableWidgetItem("Jan2"));

        self.tableWidget.show()

        # UI ProgressBar
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)


    def folderBrowse(self) :
        '''
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  (Used Module) from PyQt5.QtWidgets import QFileDialog
				2016-09-24 V1.0[Heyn]
        '''
        directory = QFileDialog.getExistingDirectory(self, "Regex Folder", QtCore.QDir.currentPath())
        self.folder_textEdit.setText(directory)  

    def exportBrowse(self) :
        '''
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  (Used Module) from PyQt5.QtWidgets import QFileDialog
				2016-09-24 V1.0[Heyn]
        '''
        exportExcel = QFileDialog(self,filter = "*.xls")
        if exportExcel.exec() == QDialog.Accepted :
            # self.export_textEdit.setText(os.path.basename(exportExcel.selectedFiles()[0]))
            self.export_textEdit.setText(exportExcel.selectedFiles()[0])

    def setProgressbarRange(self, maxValue) :
        self.progressBar.setRange(0,maxValue)
    
    def setProgressbarsetValue(self, value) :
        self.progressBar.setValue(value)

    def startButton(self) :
        msgList = []
        msgList.append(self.folder_textEdit.toPlainText().strip())
        msgList.append(self.export_textEdit.toPlainText().strip())
        msgList.append(self.fileExt_textEdit.toPlainText().strip())
        msgList.append(self.fileName_textEdit.toPlainText().strip())
        msgList.append(self.keyWords_textEdit.toPlainText().strip())
        if (msgList[0] == "") or (msgList[1] == "") :
            QMessageBox.warning(self,
                    "Warning",
                    "Folder or Export is null",
                    QMessageBox.Yes)
        else :
            self.signelStart.emit(msgList)

    def signeltableWidgetUpdate(self, msgList) :

        for index in range(len(msgList[0])) :
            newRowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(newRowCount)
            self.tableWidget.setItem(newRowCount,0,QTableWidgetItem(msgList[index][0]));
            self.tableWidget.setItem(newRowCount,1,QTableWidgetItem(msgList[index][1]));       
        pass

    def signelConnectStartBtn(self, handlerProc) :
        '''
		Argument(s): 
					None
		Return(s): 
					None
		Notes:  Caller : Init function
				2016-09-24 V1.0[Heyn]
        '''        
        self.signelStart.connect(handlerProc)
        self.signeltableWidget.connect(self.signeltableWidgetUpdate)


# app = QApplication(sys.argv)
# dlg = hzMainWindowsDlg()
# dlg.show()
# sys.exit(app.exec_())
