#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:         Gear Generator
# Purpose:      Just for fun
#
# Author:       Manuel Astros
# Email:        manuel.astros1980@gmail.com
# Web:          https://sites.google.com/view/interpolation/home
#
# Created:     25/06/2021
# Copyright:   (c) astros 2021
# Licence:     MIT
# Based on:    Gear Drawing with Bézier Curves (https://www.arc.id.au/GearDrawing.html)
# -------------------------------------------------------------------------------
#
# Reelases:
# 0.1: First Release
# ______________________________________________________________________________________


import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCloseEvent, QFont
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QHeaderView, \
                            QCheckBox, QComboBox, QMessageBox, QWidget, QVBoxLayout

from Gear_Mpl_Draw import MplWidget

#--------------------------New Import------------
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
import numpy as np
import random
#----------------------------------------

class mainWindow(QMainWindow):
    def __init__(self):
        self.ErrInt = True
        self.ErrFloat = True
        super(mainWindow, self).__init__()
        loadUi('Gear_Generator.ui', self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        check_box = internal(self)
        check_box.stateChanged.connect(self._clickBox)
        self.tableWidget.setCellWidget(0, 0, check_box)

        angle = QtWidgets.QTableWidgetItem(str(20))
        angle.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, angle)

        lista = ['Not Linked'] + [str(i) for i in range(1, self.tableWidget.rowCount())]
        mesh = Mesh(self, lista)
        self.tableWidget.setCellWidget(0, 6, mesh)

        # m: module, m = pitch diameter / teeth number
        m = float(self.tableWidget.item(0, 1).text()) / float(self.tableWidget.item(0, 2).text())
        m = QtWidgets.QTableWidgetItem(str(m))
        m.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 5, m)

        Acell = QtWidgets.QTableWidgetItem('0')
        Acell.setFlags(QtCore.Qt.ItemIsEnabled)
        Acell.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 7, Acell)


        # ------------------------------------Mpl Widget insertion---------------------------------------
        mplW = MplWidget()
        self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(mplW.canvas, self))

        self.Graph = MplWidget(self.mplWidget)
        # self.Graph = CanvasGraph(self.mplWidget)
        self.Graph.setObjectName("Gear-View")

        # ---------------------------------------------------------------------------

        # ------------Signals-----------------------------------
        self.add_gear.clicked.connect(self._addRow)
        self.remove_gear.clicked.connect(self._removeRow)

        self.tableWidget.itemChanged.connect(self._cellChange)

        self._dataRevision()
        # self._cancel.clicked.connect(self._close)
        # self.add_gear.clicked.connect(self._addRow)

    def _clickBox(self):
        print('funcionó')
        Acell = self.tableWidget.item(0, 7).text()
        print(Acell)
        Acell = QtWidgets.QTableWidgetItem(Acell)
        # Acell.setFlags(QtCore.Qt.ItemIsEnabled)
        Acell.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 7, Acell)



    def _dataRevision(self):
        # if self.tableWidget.item(0,0).text() ==
        print(str(self.tableWidget.item(0, 0).text()))
        pass

    def _comboBoxRevision(self):
        current_row = self.tableWidget.currentRow()
        value = self.tableWidget.cellWidget(current_row, 6)
        value2 = value.currentText()
        print('este valor: ', value2)
        if type(value) is None:
            print('Valor none seleccionado')

        #     print("None")
        #     Xcell = QtWidgets.QTableWidgetItem('0')
        #     # Xcell.setFlags(QtCore.Qt.ItemIsEnabled)
        #     Xcell.setTextAlignment(QtCore.Qt.AlignCenter)
        #     self.tableWidget.setItem(1, 8, Xcell)
        #
        #     Ycell = QtWidgets.QTableWidgetItem('0')
        #     # Ycell.setFlags(QtCore.Qt.ItemIsEnabled)
        #     Ycell.setTextAlignment(QtCore.Qt.AlignCenter)
        #     self.tableWidget.setItem(1, 9, Ycell)
        #
        #     Acell = QtWidgets.QTableWidgetItem('0')
        #     # Acell.setFlags(QtCore.Qt.ItemIsEnabled)
        #     Acell.setTextAlignment(QtCore.Qt.AlignCenter)
        #     self.tableWidget.setItem(1, 7, Acell)
        pass

    def _cellChange(self):
        items = self.tableWidget.selectedItems()
        col = self.tableWidget.currentColumn()
        row = self.tableWidget.currentRow()
        print(row, col)
        enteros = [1, 2]
        decimales = [3, 4, 5, 7, 8, 9]

        if col in enteros:
            try:
                cellType  = int(items[0].text())
            except ValueError:
                self.ErrInt = False
                self.statusLabel.setText('Error: Value cell most be an integer')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(122, 55, 55)")
                return self.alertDialog('integer')
        elif col in decimales:
            try:
                cellType = float(items[0].text())
            except ValueError:
                self.ErrFloat = False
                self.statusLabel.setText('Error: Value cell most be an Float')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(122, 55, 55)")
                return self.alertDialog('Float')
        # print(str(items[0].text()))



    def alertDialog(self, val):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        message = val + " input is required"
        msgBox.setText(message)
        msgBox.setWindowTitle("Input Error")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')



    def _addRow(self):
        if self.ErrInt or self.ErrFloat:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            columnCount = self.tableWidget.columnCount()

            for col in range(columnCount):
                print(col)
                if col == 0:
                    check_box = internal(self)
                    check_box.stateChanged.connect(self._clickBox)
                    self.tableWidget.setCellWidget(rowCount, col, check_box)
                elif col == 3:
                    angle = QtWidgets.QTableWidgetItem('20')
                    angle.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, angle)
                elif col == 6:
                    lista = ['Not Linked'] + [str(i) for i in range(1, self.tableWidget.rowCount())]
                    mesh = Mesh(self, lista)
                    self.tableWidget.setCellWidget(rowCount, col, mesh)
                    mesh.currentIndexChanged.connect(self._comboBoxRevision)
                elif col == 8:
                    Xcell = QtWidgets.QTableWidgetItem('0')
                    Xcell.setFlags(QtCore.Qt.ItemIsEnabled)
                    Xcell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, Xcell)
                elif col == 9:
                    Ycell = QtWidgets.QTableWidgetItem('0')
                    Ycell.setFlags(QtCore.Qt.ItemIsEnabled)
                    Ycell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, Ycell)
                else:
                    cellCenter = QtWidgets.QTableWidgetItem()
                    cellCenter.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, cellCenter)


    def _removeRow(self):
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(self.tableWidget.rowCount()-1)



# ----------------Events----------------------------------------------
# Properly defined in the future
#     def closeEvent(self, event):
#         reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
#                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#
#         if reply == QMessageBox.Yes:
#             event.accept()
#             # self.action_close_window.triggered.emit(True)
#             print('Window closed')
#         else:
#             event.ignore()
#
#         def resizeEvent(self, event):
#             print("resize")
#             QMainWindow.resizeEvent(self, event)
# ----------------------------------------------------------------------------



class internal(QCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.stateChanged.connect(self.getCheckValue)
    def getCheckValue(self):
        if self.isChecked() == True:
            print('Check Value Active')
            return True
        elif self.isChecked() == False:
            print('Check Value Deactivated')
            return False


class Mesh(QComboBox):
    def __init__(self, parent, aa):
        super().__init__(parent)
        self.addItems(aa)
        self.currentIndexChanged.connect(self.getComboValue)
    def getComboValue(self):
        print(self.currentText())
        return self.currentText()


app = QApplication(sys.argv)
main_window = mainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_window)
# widget.setFixedHeight(300)
# widget.setFixedWidth(1060)
widget.resize(658, 650)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')