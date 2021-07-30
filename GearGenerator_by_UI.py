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

# --------------------------Mpl Import------------
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from math import radians, degrees, atan, hypot, sin, cos
# import numpy as np
import random

# ---------------Internal modules import--------------
from gear_calc import createGearOutline, createIntGearOutline, displace, rotate

# ----------------------------------------

class mainWindow(QMainWindow):
    def __init__(self):
        self.ErrInt = True
        self.ErrFloat = True
        self.ErrPitchDiam = True
        super(mainWindow, self).__init__()
        loadUi('Gear_Generator.ui', self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        check_box = internal(self)
        check_box.stateChanged.connect(self._clickCheckBox)
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
        self._gearGraphic()

        # self.Graph = CanvasGraph(self.mplWidget)
        # self.Graph.setObjectName("Gear-View")

        # ---------------------------------------------------------------------------

        # ------------Signals-----------------------------------
        self.add_gear.clicked.connect(self._addRow)
        self.remove_gear.clicked.connect(self._removeRow)
        self.generate_gear.clicked.connect(self._gearGraphic)
        self.tableWidget.itemChanged.connect(self._cellChange)

        self._dataRevision()
        # self._cancel.clicked.connect(self._close)
        # self.add_gear.clicked.connect(self._addRow)

    def _gearGraphic(self):
        gear_outline = self._gearCalculation()
        # self.mplW = MplWidget(self.mplWidget)
        # self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(mplW.canvas, self))
        self.Graph = MplWidget(self.mplWidget, gear_outline)


    def _clickCheckBox(self):
        check_row = self.tableWidget.currentRow()
        check = self.tableWidget.cellWidget(check_row, 0).getCheckValue()
        print(check)
        if check:
            self.statusLabel.setText('Row: ' + str(check_row + 1) + ' - ' + 'Draw Internal Gear')
            self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
        else:
            self.statusLabel.setText('Row: ' + str(check_row + 1) + ' - ' + 'Draw Normal Gear')
            self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
        

    def _comboBoxRevision(self):
        combo_row = self.tableWidget.currentRow()
        # current_col = self.tableWidget.currentRow()
        mesh_row_value_pointed = self.tableWidget.cellWidget(combo_row, 6).currentText()
        print('actual cell: ', combo_row)
        print('valor apuntado: ', mesh_row_value_pointed)

        if mesh_row_value_pointed == 'Not Linked':
            Acell = self.tableWidget.item(combo_row, 7).text()
            print(Acell)
            Acell = QtWidgets.QTableWidgetItem(Acell)
            Acell.setFlags(QtCore.Qt.ItemIsEnabled)
            Acell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 7, Acell)
            
            Xcell = self.tableWidget.item(combo_row, 8).text()
            Xcell = QtWidgets.QTableWidgetItem(Xcell)
            # Xcell.setFlags(QtCore.Qt.ItemIsEnabled)
            Xcell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 8, Xcell)

            Ycell = self.tableWidget.item(combo_row, 9).text()
            Ycell = QtWidgets.QTableWidgetItem(Ycell)
            # Ycell.setFlags(QtCore.Qt.ItemIsEnabled)
            Ycell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 9, Ycell)
            
            self.statusLabel.setText('Row: ' + str(combo_row + 1) + ' - Gear is ' + mesh_row_value_pointed)
            self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
            print(mesh_row_value_pointed)
            self.ErrPitchDiam = True

        else:
            try:
                A_pitchDiam = float(self.tableWidget.item(combo_row, 1).text())                 

            except ValueError:
                Acell = '0'
                Xcell ='0'
                Ycell = '0'
                self.meshMessage = 'Pith diameter missing in current row (' + str(combo_row + 1) + ')'
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(122, 55, 55)")
                print('Pith diameter missing in current row (' + str(combo_row + 1) + ')')
                self.ErrPitchDiam = False
            
            else:
                try:
                    A_pitchDiam_pointed = float(self.tableWidget.item(int(mesh_row_value_pointed) - 1, 1).text())

                    Acell = float(self.tableWidget.item(combo_row, 7).text())
                    Xcell = float(self.tableWidget.item(combo_row, 8).text())
                    Ycell = float(self.tableWidget.item(combo_row, 9).text())
                    
                    Acell_pointed = float(self.tableWidget.item(int(mesh_row_value_pointed) - 1, 7).text())
                    Xcell_pointed = float(self.tableWidget.item(int(mesh_row_value_pointed) - 1, 8).text())
                    Ycell_pointed = float(self.tableWidget.item(int(mesh_row_value_pointed) - 1, 9).text())

                    pitchDiam_dist = (A_pitchDiam / 2) + (A_pitchDiam_pointed / 2)

                    Xcell = str(Xcell_pointed + pitchDiam_dist * cos(radians(Acell)))
                    Ycell = str(Ycell_pointed + pitchDiam_dist * sin(radians(Acell)))
                    Acell = str(Acell)

                    self.ErrPitchDiam = True

                except:
                    Acell = '0'
                    Xcell ='0'
                    Ycell = '0'
                    self.meshMessage = 'Pith diameter missing in row (' + str(mesh_row_value_pointed) + ')'
                    print('Pith diameter missing in row (' + str(mesh_row_value_pointed) + ')')
                    self.ErrPitchDiam = False

            # Acell = self.tableWidget.item(combo_row, 7).text()
            Acell = QtWidgets.QTableWidgetItem(Acell)
            # Acell.setFlags(QtCore.Qt.ItemIsEnabled)
            Acell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 7, Acell)
            
            # Xcell = self.tableWidget.item(combo_row, 8).text()
            Xcell = QtWidgets.QTableWidgetItem(Xcell)
            Xcell.setFlags(QtCore.Qt.ItemIsEnabled)
            Xcell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 8, Xcell)

            # Ycell = self.tableWidget.item(combo_row, 9).text()
            Ycell = QtWidgets.QTableWidgetItem(Ycell)
            Ycell.setFlags(QtCore.Qt.ItemIsEnabled)
            Ycell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(combo_row, 9, Ycell)

            if self.ErrPitchDiam:
                self.statusLabel.setText('Row: ' + str(combo_row + 1) + ' - ' + 'meshing with row ' + mesh_row_value_pointed + ' gear')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
                print('meshing with ', mesh_row_value_pointed)
            else:
                self.statusLabel.setText(self.meshMessage + '  |  Row: ' + str(combo_row + 1) + ' - ' + 'meshing with row ' + mesh_row_value_pointed + ' gear')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(122, 55, 55)")
                print('meshing with ', mesh_row_value_pointed)
    

    def _dataRevision(self):
        self.ErrInt = True
        self.ErrFloat = True
        verification = []
        row_rev = self.tableWidget.rowCount()
        print(row_rev)

        for r in range(row_rev):
            try:
                check_val_rev = self.tableWidget.cellWidget(r, 0).getCheckValue()
                teeth_pitch_diam_rev = int(self.tableWidget.item(r, 1).text())
                teeth_n_rev = int(self.tableWidget.item(r, 2).text())
                pressure_ang_rev = float(self.tableWidget.item(r, 3).text())
                s_or_r_radius_rev = float(self.tableWidget.item(r, 4).text()) / 2
                module_g_rev = float(self.tableWidget.item(r, 5).text())
                mesh_rev = self.tableWidget.cellWidget(r, 6).currentText()
                angle_rev = float(self.tableWidget.item(r, 7).text())
                x_rev = float(self.tableWidget.item(r, 8).text())
                y_rev = float(self.tableWidget.item(r, 9).text())

                if mesh_rev != 'Not Linked':
                    pass
     
                verification.append(True)

            except:
                verification.append(False)
        
        return verification


    def _gearCalculation(self):
        # verif = [True, False, True]
        verif = self._dataRevision()
        gears=[]

        for row_g in range(len(verif)):
            gears.append([row_g + 1])
            print('intento: ', verif[row_g])

            if (verif[row_g]):
                teeth_n = int(self.tableWidget.item(row_g, 2).text())
                pressure_ang = float(self.tableWidget.item(row_g, 3).text())
                s_or_r_radius = float(self.tableWidget.item(row_g, 4).text()) / 2
                module_g = float(self.tableWidget.item(row_g, 5).text())
                check_val = self.tableWidget.cellWidget(row_g, 0).getCheckValue()
                Xcell = float(self.tableWidget.item(row_g, 8).text())
                Ycell = float(self.tableWidget.item(row_g, 9).text())
                
                if check_val:
                    outline = createIntGearOutline(module_g, teeth_n, pressure_ang, s_or_r_radius)

                else:
                    outline = createGearOutline(module_g, teeth_n, pressure_ang, s_or_r_radius)

                if Xcell != 0 or Ycell != 0:
                    outline_diplaced = displace(outline, Xcell, Ycell)
                    outline = outline_diplaced
                    
                gears[row_g].append(outline)
                print('True: ', row_g + 1)

            else:
                gears[row_g].append([False])
                print('False: ', row_g + 1)
        
        print(gears)
        return gears       

    def _cellChange(self):
        items = self.tableWidget.selectedItems()
        col = self.tableWidget.currentColumn()
        row = self.tableWidget.currentRow()
        print('_cellChange: ', row, col)
        enteros = [1, 2]
        decimales = [3, 4, 5, 7, 8, 9]

        if col in enteros:
            try:
                cellType  = int(items[0].text())
                self.ErrInt = True
                self.statusLabel.setText('OK: Current cell data is an integer')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
            except ValueError:
                self.ErrInt = False
                self.statusLabel.setText('Error: Value cell most be an integer')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(122, 55, 55)")
                return self.alertDialog('integer')
        elif col in decimales:
            try:
                cellType = float(items[0].text())
                self.ErrFloat = True
                self.statusLabel.setText('OK: Current cell data is a float')
                self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color: rgb(0, 0, 0)")
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
                    check_box.stateChanged.connect(self._clickCheckBox)
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
                elif col == 7:
                    Acell = QtWidgets.QTableWidgetItem('0')
                    Acell.setFlags(QtCore.Qt.ItemIsEnabled)
                    Acell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, Acell)
                elif col == 8:
                    Xcell = QtWidgets.QTableWidgetItem('0')
                    # Xcell.setFlags(QtCore.Qt.ItemIsEnabled)
                    Xcell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, Xcell)
                elif col == 9:
                    Ycell = QtWidgets.QTableWidgetItem('0')
                    # Ycell.setFlags(QtCore.Qt.ItemIsEnabled)
                    Ycell.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, Ycell)
                else:
                    cellCenter = QtWidgets.QTableWidgetItem()
                    cellCenter.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(rowCount, col, cellCenter)
        
            self.statusLabel.setText('OK: Row just added')
            self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color:rgb(0, 0, 0)")

    
    def _removeRow(self):
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(self.tableWidget.rowCount()-1)

            self.statusLabel.setText('OK: Row just deleted')
            self.statusLabel.setStyleSheet("background-color:rgba(122, 167, 146, 150); color:rgb(0, 0, 0)")

    

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