from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QErrorMessage, QMessageBox
from collections import deque
import pyqtgraph as pg
import pandas as pd
import sys
import os
import time

class PLotLine():
    def __init__(self):
        self.data = None
        self.index = 0
        self.data_line = None
        self.pen = None
        #self.timer

PlotLines1 = []
PlotLines2 = []

ext = ('.txt', '.csv')
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #loading ui file
        self.ui=uic.loadUi('GUI.ui', self)
        # Connect widgets to methods here
        #self.actionZoomOut.triggered.connect(self.print)
        self.actionChannel1.triggered.connect(self.DrawChannel1)
        self.actionChannel2.triggered.connect(self.DrawChannel2)
        self.actionShow_Hide.triggered.connect(self.showHideChannel1)
        self.actionHide2.triggered.connect(self.showHideChannel2)
        self.actionZoomIn.triggered.connect(self.ZoomIn)
        self.actionZoomOut.triggered.connect(self.ZoomOut)
        self.actionMoveSignal1.triggered.connect(self.MoveSignal1)
        self.data_moved = False

        #setting plotting graph color to grey
        pg.setConfigOption('background', '#1f1f1f')
        pd.options.display.max_rows = 999999
        #creating plot widget
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget1.setMaximumSize(1000,1000)
        self.graphWidget1.setMinimumSize(400,400)
        self.graphWidget2.setMinimumSize(400,400)
        self.graphWidget2.setMaximumSize(1000,1000)
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)

        self.data_line =  None
        self.ishidden1 = 0
        self.ishidden2 = 0

    def DrawChannel1(self):
        self.load1()
        newplot = PlotLines1[-1]
        pen = pg.mkPen(color=(255, 0, 0))
        newplot.data_line = self.graphWidget1.plot(pen=pen)
        self.index = 0

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plots)  # Connect to a single update method
        self.timer.start()

    def DrawChannel2(self):
        self.load2()
        newplot = PlotLines2[-1]
        pen = pg.mkPen(color=(255, 0, 0))
        newplot.data_line = self.graphWidget2.plot(pen=pen)
        self.index = 0

        self.timer = QtCore.QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.update_plots)  # Connect to a single update method
        self.timer.start()

    def load1(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        if path.endswith(ext):
            if path.endswith('.txt'):
                with open( path , 'r') as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PLotLine()
                newplot.data=pd.DataFrame({'time':x,'amplitude':y})
                PlotLines1.append(newplot)
            else:
                newplot = PLotLine()
                newplot.data = pd.read_csv(path, usecols=['time', 'amplitude'])
                PlotLines1.append(newplot)
        else:
            self.ErrorLoadingFile()

    def load2(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        if path.endswith(ext):
            if path.endswith('.txt'):
                with open( path , 'r') as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PLotLine()
                newplot.data=pd.DataFrame({'time':x,'amplitude':y})
                PlotLines2.append(newplot)
            else:
                newplot = PLotLine()
                newplot.data = pd.read_csv(path, usecols=['time', 'amplitude'])
                PlotLines2.append(newplot)
        else:
            self.ErrorLoadingFile()


    def showHideChannel1(self):
        if self.ishidden1==0:
         self.graphWidget1.hide()
         self.ishidden1=1
        else:
         self.graphWidget1.show()
         self.ishidden1=0

    def showHideChannel2(self):
        if self.ishidden2==0:
         self.graphWidget2.hide()
         self.ishidden2=1
        else:
         self.graphWidget2.show()
         self.ishidden2=0

    def ErrorLoadingFile(self):
        msg=QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("You can only load .txt or .csv files.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def update_plots(self):
        # if newplot != None:
            for newplot in PlotLines1:
                if newplot.index < len(newplot.data):
                    newplot.data_line.setData(newplot.data['time'][:newplot.index + 1], newplot.data['amplitude'][:newplot.index + 1])
                    self.graphWidget1.setXRange(newplot.data['time'][newplot.index], newplot.data['time'][newplot.index],padding=0)
                    # self.graphWidget1.setYRange(newplot.data['amplitude'][newplot.index], newplot.data['amplitude'][newplot.index],padding=0)
                    newplot.index += 1
                else:
                    self.graphWidget1.setXRange(newplot.data['time'][1], newplot.data['time'][newplot.index],padding=0)




            for newplot in PlotLines2:
                if newplot.index < len(newplot.data):
                    newplot.data_line.setData(newplot.data['time'][:newplot.index + 1], newplot.data['amplitude'][:newplot.index + 1])
                    newplot.index += 1

            # Check if all data is plotted; if so, stop the timer
            if all(newplot.index >= len(newplot.data) for newplot in PlotLines1) and all(newplot.index >= len(newplot.data) for newplot in PlotLines2):
                self.timer.stop()


    def ZoomIn(self):
        viewbox = self.graphWidget1.getViewBox()

        # Decrease the scale (range) of the X and Y axes to zoom in
        new_x_range = viewbox.viewRange()[0]
        new_y_range = viewbox.viewRange()[1]

        new_x_range = (new_x_range[0] * 0.8, new_x_range[1] * 0.8)
        new_y_range = (new_y_range[0] * 0.8, new_y_range[1] * 0.8)

        viewbox.setXRange(*new_x_range)
        viewbox.setYRange(*new_y_range)

        # viewbox = self.graphWidget1.getViewBox()
        # x_range, y_range = viewbox.viewRange()
        # self.graphWidget1.setScale(scale=2)
    def ZoomOut(self):
        viewbox = self.graphWidget1.getViewBox()

        # Decrease the scale (range) of the X and Y axes to zoom in
        new_x_range = viewbox.viewRange()[0]
        new_y_range = viewbox.viewRange()[1]

        new_x_range = (new_x_range[0] * 1.2, new_x_range[1] * 1.2)
        new_y_range = (new_y_range[0] * 1.2, new_y_range[1] * 1.2)

        viewbox.setXRange(*new_x_range)
        viewbox.setYRange(*new_y_range)

    def MoveSignal1(self):
        if PlotLines1 and not self.data_moved:
            newplot = PlotLines1[-1]
            if newplot.data is not None:
                # Copy data from the first channel (channel 1) to the second channel (channel 2)
                new_channel = PLotLine()
                new_channel.data = newplot.data.copy()
                PlotLines2.append(new_channel)

                # Clear the existing data in channel 2 and plot the new data
                self.graphWidget2.clear()
                pen = pg.mkPen(color=(255, 0, 0))
                new_channel.data_line = self.graphWidget2.plot(pen=pen)
                new_channel.index = 0
                self.data_moved = True

                # PlotLines1[-1].data = None
                # self.graphWidget1.clear()

                # self.data_moved = True



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())