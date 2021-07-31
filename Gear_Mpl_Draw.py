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
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=150):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MplWidget(QWidget):
    def __init__(self, parent=None, values=0):
        QWidget.__init__(self, parent)

        gear_location = values[0]
        gear_outline = values[1]
 
        fig = Figure()
        fig.tight_layout()
        self.canvas = MplCanvas(fig)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes.clear()

        if isinstance(gear_outline, list):
            x = 0
            y = 1
            for i in range(len(gear_outline)):
                x_gear = []
                y_gear = []
                rr = False  # Switch to detect difference between gear format and Radius (shaft or rim) format data
                # print('valor I: ', i)
                for j in range(len(gear_outline[i][1])):
                    # print('valor J:', j)
                    if isinstance(gear_outline[i][1][j], list) and rr == False:
                        x_gear.append(gear_outline[i][1][j][x])
                        y_gear.append(gear_outline[i][1][j][y])
                    elif gear_outline[i][1][j] == 'R':
                        radio = gear_outline[i][1][j + 1]
                        x_location = gear_location[i][1][x]
                        y_location = gear_location[i][1][y]
                        rr = True

                self.canvas.axes.add_patch(plt.Circle((x_location, y_location), radio, fill=False))
                self.canvas.axes.plot(x_gear, y_gear)
                print('print value ' + str(i))
                print(x_gear)

        # self.canvas.axes = self.canvas.figure.add_subplot(111)
        # self.canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setLayout(vertical_layout)


# class MainWindow(QMainWindow):
    
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

#         # Create the maptlotlib FigureCanvas object,
#         # which defines a single set of axes as self.axes.
#         sc = MplWidget(self, width=5, height=4, dpi=100)
#         sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
#         self.setCentralWidget(sc)


# class MainWindow(QMainWindow):
    
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         self.layout = QVBoxLayout()
#         self.mplW = MplWidget()
#         self.layout.addWidget(self.mplW)


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()