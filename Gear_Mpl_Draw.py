
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

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class CanvasGraph(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
                    title='About as simple as it gets, folks')
        self.ax.grid()
        # self.show()



class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        fig = Figure()
        fig.tight_layout()
        self.canvas = FigureCanvas(fig)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        # self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
