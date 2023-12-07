from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QErrorMessage,
    QMessageBox,
    QDialog,
    QScrollBar
)
from collections import deque
import pyqtgraph as pg
import pandas as pd
import sys
import os
import time
from PIL import Image
import tkinter as tk
from tkinter import colorchooser
from PyQt5.QtGui import QImage
import io
from PIL import Image as PILImage
import PIL
import tempfile
from fpdf import FPDF
import random
from PlotLine import *
from InputDialog import *

PlotLines1 = []
PlotLines2 = []
snapshots1 = []
snapshots2 = []

ext = (".txt", ".csv")

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # loading ui file
        self.ui = uic.loadUi("GUI.ui", self)
        # Connect widgets to methods here
        # self.actionZoomOut.triggered.connect(self.print)
        self.actionChannel1.triggered.connect(self.DrawChannel1)
        self.actionChannel2.triggered.connect(self.DrawChannel2)
        self.actionShow_Hide.triggered.connect(self.showHideChannel1)
        self.actionHide2.triggered.connect(self.showHideChannel2)
        self.actionZoomIn.triggered.connect(self.zoomInChannel1)
        self.actionZoomOut.triggered.connect(self.zoomOutChannel1)
        self.actionZoomIn2.triggered.connect(self.zoomInChannel2)
        self.actionZoomOut2.triggered.connect(self.zoomOutChannel2)
        self.actionPlay_Pause.triggered.connect(self.paused1)
        self.actionPlay_Pause2.triggered.connect(self.paused2)
        self.actionmove.triggered.connect(self.Move1)
        self.actionMove2.triggered.connect(self.Move2)
        self.action25x_1.triggered.connect(self.changesignal1speed25)
        self.action50x_1.triggered.connect(self.changesignal1speed50)
        self.action100x_1.triggered.connect(self.changesignal1speed100)
        self.action150x_1.triggered.connect(self.changesignal1speed150)
        self.action200x_1.triggered.connect(self.changesignal1speed200)
        self.action25x_2.triggered.connect(self.changesignal2speed25)
        self.action50x_2.triggered.connect(self.changesignal2speed50)
        self.action100x_2.triggered.connect(self.changesignal2speed100)
        self.action150x_2.triggered.connect(self.changesignal2speed150)
        self.action200x_2.triggered.connect(self.changesignal2speed200)
        self.actionChannel_1.triggered.connect(self.clear1)
        self.actionChannel_2.triggered.connect(self.clear2)
        self.actionChannel_5.triggered.connect(self.addtitle1)
        self.actionChannel_6.triggered.connect(self.addtitle2)
        self.actionChannel3.triggered.connect(self.SnapshotChannel1)
        self.actionChannel4.triggered.connect(self.SnapshotChannel2)
        self.Color1.triggered.connect(self.ChangeColor1)
        self.Color2.triggered.connect(self.ChangeColor2)
        self.actionRewind1.triggered.connect(self.rewind1)
        self.actionrewind2.triggered.connect(self.rewind2)
        self.actionSave_As_PDF.triggered.connect(self.create_pdf_with_qimages)
        self.actionConnect.triggered.connect(self.ConnectGraphs)
        self.horizontalScrollBar.actionTriggered.connect(self.ScrollChannel1)
        self.horizontalScrollBar_2.actionTriggered.connect(self.ScrollChannel2)


        # self.setHorizontalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        # self.setVerticalScrollBar(QScrollBar(QtCore.Vertical, self))
        # self.setVerticalScrollBarPolicy(QtCore.ScrollBarAlwaysOn)
        # self.verticalScrollBar().valueChanged.connect(self.scroll_graph)


        # setting plotting graph color to grey
        pg.setConfigOption("background", "#1f1f1f")
        pd.options.display.max_rows = 999999
        # creating plot widget
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget1.setMaximumSize(1000, 1000)
        self.graphWidget1.setMinimumSize(400, 400)
        self.graphWidget1.setXRange(0,100,padding=0)
        self.graphWidget2.setMinimumSize(400, 400)
        self.graphWidget2.setMaximumSize(1000, 1000)
        self.graphWidget2.setXRange(0,100,padding=0)
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)
        self.graphWidget1.setMouseEnabled(x=False,y=True)
        self.graphWidget2.setMouseEnabled(x=False,y=True)
        self.data_line = None
        self.ishidden1 = 0
        self.ishidden2 = 0
        self.zoomFactorChannel1 = 0
        self.zoomFactorChannel2 = 0
        self.ispaused1 = 0
        self.ispaused2 = 0
        self.signal1speed = 1
        self.signal2speed = 1
        self.data_moved = False
        self.snapshots1 = []
        self.snapshots2 = []
        self.time_mean1 = 0
        self.time_mean2 = 0
        self.amplitude_mean1 = 0
        self.amplitude_mean2 = 0
        self.median1 = 0
        self.median2 = 0
        self.max1 = 0
        self.min1 = 0
        self.max2 = 0
        self.min2 = 0
        self.connect_status = False
        self.Xmin1 = self.Xmin2 = 0.0
        self.Ymin1 = self.Ymin2 = float('inf')
        self.Xmax1 = self.Xmax2 = self.Ymax1 = self.Ymax2 = float('-inf')
        self.legend1 = self.graphWidget1.addLegend()
        self.graphWidget1.showGrid(x=True,y=True)
        self.legend2 = self.graphWidget2.addLegend()
        self.graphWidget2.showGrid(x=True,y=True)
        self.graphWidget1.setLimits(xMin=0)
        self.graphWidget2.setLimits(xMin=0)
        self.graphWidget2.setLabel("left", "Amplitude")
        self.graphWidget2.setLabel("bottom", "Time")
        self.graphWidget1.setLabel("left", "Amplitude")
        self.graphWidget1.setLabel("bottom", "Time")


    def DrawChannel1(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        self.load1(path=path)
        if path == '':
            return
        random_rgb = self.random_color()
        newplot = PlotLines1[-1]
        newplot.pen = pg.mkPen(color = random_rgb)
        newplot.name = "Signal " + str(len(PlotLines1))
        newplot.data_line = self.graphWidget1.plot(pen=newplot.pen, name=newplot.name)
        self.index = 0
        list = []
        list.append(newplot.name)
        self.comboBox.addItems(list)
        self.horizontalScrollBar.setMinimum(0)

        # self.timer1 = QtCore.QTimer()
        # self.timer1.setInterval(int(50 / self.signal1speed))
        # self.timer1.timeout.connect(
        #     self.update_plots1
        # )  # Connect to a single update method
        # self.timer1.start()
        self.update_plots1()

    def random_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        
        return (red,green,blue)

    def Draw1(self,newplot):
        newplot.index = 0
        pen = newplot.pen
        newplot.data_line = self.graphWidget1.plot(pen=pen)
        self.horizontalScrollBar.setMinimum(0)

        # self.timer1 = QtCore.QTimer()
        # self.timer1.setInterval(int(50 / self.signal1speed))
        # self.timer1.timeout.connect(
        #     self.update_plots1
        # )  # Connect to a single update method
        # self.timer1.start()
        self.update_plots1()

    def DrawChannel2(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        self.load2(path=path)
        if path == '':
            return
        random_rgb = self.random_color()
        newplot = PlotLines2[-1]
        newplot.pen = pg.mkPen(color = random_rgb)
        newplot.name = "Signal " + str(len(PlotLines2))
        newplot.data_line = self.graphWidget2.plot(pen=newplot.pen, name=newplot.name)
        self.index = 0
        list = []
        list.append(newplot.name)
        self.comboBox_2.addItems(list)
        self.horizontalScrollBar_2.setMinimum(0)

        # self.timer2 = QtCore.QTimer()
        # self.timer2.setInterval(int(50 / self.signal2speed))
        # self.timer2.timeout.connect(
        #     self.update_plots2
        # )  # Connect to a single update method
        # self.timer2.start()
        self.update_plots2()

    def Draw2(self,newplot):
        newplot.index = 0
        pen = newplot.pen
        newplot.data_line = self.graphWidget2.plot(pen=pen)
        self.horizontalScrollBar_2.setMinimum(0)

        # self.timer2 = QtCore.QTimer()
        # self.timer2.setInterval(int(50 / self.signal2speed))
        # self.timer2.timeout.connect(
        #     self.update_plots2
        # )  # Connect to a single update method
        # self.timer2.start()
        self.update_plots2()

    def load1(self,path):
        if path.endswith(ext):
            if path.endswith(".txt"):
                with open(path, "r") as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PlotLine()
                newplot.data = pd.DataFrame({"time": x, "amplitude": y})
                PlotLines1.append(newplot)
                newplot.ChannelNum = 1
            else:
                newplot = PlotLine()
                newplot.data = pd.read_csv(path, usecols=["time", "amplitude"])
                PlotLines1.append(newplot)
                newplot.ChannelNum = 1
        else:
            self.ErrorMsg("You can only load .txt or .csv files.")
        if path == '':
            return
        if newplot.data["time"][len(newplot.data["time"]) - 1] > self.Xmax1:
            self.Xmax1 = newplot.data["time"][len(newplot.data["time"]) - 1]
        if newplot.data["amplitude"].min() < self.Ymin1:
            self.Ymin1 = newplot.data["amplitude"].min()
        if newplot.data["amplitude"].max() > self.Ymax1:
            self.Ymax1 = newplot.data["amplitude"].max()
        self.graphWidget1.setLimits(xMin = self.Xmin1, xMax = self.Xmax1, yMin = self.Ymin1, yMax = self.Ymax1)
        self.horizontalScrollBar.setMaximum(int(self.Xmax1))
        self.graphWidget1.setYRange(self.Ymin1,self.Ymax1)

    def load2(self,path):
        if path.endswith(ext):
            if path.endswith(".txt"):
                with open(path, "r") as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PlotLine()
                newplot.data = pd.DataFrame({"time": x, "amplitude": y})
                PlotLines2.append(newplot)
                newplot.ChannelNum = 2
            else:
                newplot = PlotLine()
                newplot.data = pd.read_csv(path, usecols=["time", "amplitude"])
                PlotLines2.append(newplot)
                newplot.ChannelNum = 2
        else:
            self.ErrorMsg("You can only load .txt or .csv files.")
        if path == '':
            return
        if newplot.data["time"][len(newplot.data["time"]) - 1] > self.Xmax2:
            self.Xmax2 = newplot.data["time"][len(newplot.data["time"]) - 1]
        if newplot.data["amplitude"].min() < self.Ymin2:
            self.Ymin2 = newplot.data["amplitude"].min()
        if newplot.data["amplitude"].max() > self.Ymax2:
            self.Ymax2 = newplot.data["amplitude"].max()
        self.graphWidget2.setLimits(xMin = self.Xmin2, xMax = self.Xmax2, yMin = self.Ymin2, yMax = self.Ymax2)
        self.horizontalScrollBar_2.setMaximum(self.Xmax2)
        self.graphWidget2.setYRange(self.Ymin2,self.Ymax2)
        
    def showHideChannel1(self):
        newplot = self.GetChosenPlotLine1()
        if newplot == -1 or len(PlotLines1) == 0:
            self.ErrorMsg("No Signal Chosen")
            return
        if newplot.ishidden == False:
            newplot.data_line.hide()
            newplot.ishidden = True
        else:
            newplot.data_line.show()
            newplot.ishidden = False
        if self.connect_status:
            newplot2 = self.GetChosenPlotLine2()
            if newplot2 == -1 or len(PlotLines2) == 0:
                self.ErrorMsg("No Signal Chosen")
                return
            if newplot2.ishidden == False:
                newplot2.data_line.hide()
                newplot2.ishidden = True
            else:
                newplot2.data_line.show()
                newplot2.ishidden = False


    def showHideChannel2(self):
        newplot = self.GetChosenPlotLine2()
        if newplot == -1 or len(PlotLines2) == 0:
            self.ErrorMsg("No Signal Chosen")
            return
        if newplot.ishidden == False:
            newplot.data_line.hide()
            newplot.ishidden = True
        else:
            newplot.data_line.show()
            newplot.ishidden = False
        if self.connect_status:
            newplot2 = self.GetChosenPlotLine1()
            if newplot2 == -1 or len(PlotLines1) == 0:
                self.ErrorMsg("No Signal Chosen")
                return
            if newplot2.ishidden == False:
                newplot2.data_line.hide()
                newplot2.ishidden = True
            else:
                newplot2.data_line.show()
                newplot2.ishidden = False

    def rewind1(self):
        newplot = self.GetChosenPlotLine1()
        if newplot == -1 or len(PlotLines1) == 0:
            self.ErrorMsg("No Signal Chosen")
            return
        if self.timer1.isActive() and newplot.isstopped == False:
            newplot.isstopped = True
        elif self.timer1.isActive() == False:
            newplot.isstopped = False
            self.graphWidget1.removeItem(newplot.data_line)
            self.Draw1(newplot)
            self.zoomFactorChannel1 = 0
        else:
            newplot.isstopped = False
            newplot.index = 0
            self.zoomFactorChannel1 = 0

    def rewind2(self):
        newplot = self.GetChosenPlotLine2()
        if newplot == -1 or len(PlotLines2) == 0:
            self.ErrorMsg("No Signal Chosen")
            return
        if self.timer2.isActive() and newplot.isstopped == False:
            newplot.isstopped = True
        elif self.timer2.isActive() == False:
            newplot.isstopped = False
            self.graphWidget2.removeItem(newplot.data_line)
            self.Draw2(newplot)
            self.zoomFactorChannel2 = 0
        else:
            newplot.isstopped = False
            newplot.index = 0
            self.zoomFactorChannel2 = 0

    def ErrorMsg(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def  update_plots1(self):
        self.horizontalScrollBar.setMaximum(int(self.Xmax1))
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(int(50 / self.signal1speed))
        self.timer1.timeout.connect(
            self.update_plots1
        )  # Connect to a single update method
        self.timer1.start()
        # Connect to a single update method
        if self.ispaused1 == 0:
            self.graphWidget1.setLimits(xMin = self.Xmin1, xMax = self.Xmax1, yMin = self.Ymin1, yMax = self.Ymax1)
            global newplot
            for newplot in PlotLines1:
                if newplot.isstopped == False:
                    if newplot.index < (len(newplot.data)-1):
                        x_data = newplot.data["time"][: newplot.index + 1]
                        y_data = newplot.data["amplitude"][: newplot.index + 1]
                        newplot.data_line.setData(x_data, y_data)
                        #x_range = self.graphWidget1.getViewBox().viewRange()[0][1] - self.graphWidget1.getViewBox().viewRange()[0][0]
                        if (newplot.index-100) >= 0 and newplot.index+1 <= newplot.data["time"].max():
                            self.graphWidget1.setXRange(
                                newplot.data["time"][int(newplot.index-100+self.zoomFactorChannel1)],
                                newplot.data["time"][newplot.index+1],
                                padding=0
                            )
                        else:
                            self.graphWidget1.setXRange(0+self.zoomFactorChannel1,100,padding=0)
                        self.horizontalScrollBar.setValue(int(self.graphWidget1.getViewBox().viewRange()[0][0]))
                        newplot.index += 1
        elif self.ispaused1 == 1:
            xmax = 0
            if newplot.data["time"][newplot.index] > 100:
                if newplot.data["time"][newplot.index] > xmax:
                    xmax = newplot.data["time"][newplot.index]
                self.graphWidget1.setLimits(xMin = 0, xMax = xmax)
            # Check if all data is plotted; if so, stop the timer
        if len(PlotLines1) > 0:
            if all(newplot.index >= (len(newplot.data)-1) for newplot in PlotLines1):
                self.graphWidget1.setXRange(
                    newplot.data["time"].min(),
                    newplot.data["time"].max(),
                )
                self.horizontalScrollBar.setMaximum(0)
                self.graphWidget1.setYRange(
                    newplot.data["amplitude"].min(),
                    newplot.data["amplitude"].max(),
                )
                self.timer1.stop()

    def update_plots2(self):
        self.horizontalScrollBar_2.setMaximum(int(self.Xmax2))
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(int(50 / self.signal2speed))
        self.timer2.timeout.connect(
            self.update_plots2
        )  # Connect to a single update method
        self.timer2.start()
        if self.ispaused2 == 0:
            self.graphWidget2.setLimits(xMin = self.Xmin2, xMax = self.Xmax2, yMin = self.Ymin2, yMax = self.Ymax2)
            global newplot
            for newplot in PlotLines2:
                if newplot.isstopped == False:
                    if newplot.index < (len(newplot.data)-1):
                        x_data = newplot.data["time"][: newplot.index + 1]
                        y_data = newplot.data["amplitude"][: newplot.index + 1]
                        newplot.data_line.setData(x_data, y_data)
                        if newplot.index >=100 and newplot.index+1 <= newplot.data["time"].max():
                            self.graphWidget2.setXRange(
                                newplot.data["time"][int(newplot.index-100+self.zoomFactorChannel2)],
                                newplot.data["time"][newplot.index+1],
                                padding=0
                            )
                        else:
                            self.graphWidget2.setXRange(0+self.zoomFactorChannel2,100,padding=0)
                        self.horizontalScrollBar_2.setValue(int(self.graphWidget2.getViewBox().viewRange()[0][0]))
                        newplot.index += 1
        elif self.ispaused2 == 1:
            xmax = 0
            if newplot.data["time"][newplot.index] > 100:
                if newplot.data["time"][newplot.index] > xmax:
                    xmax = newplot.data["time"][newplot.index]
                self.graphWidget2.setLimits(xMin = 0, xMax = xmax)
        if len(PlotLines2) > 0:
            if all(newplot.index >= (len(newplot.data)-1) for newplot in PlotLines2):
                self.graphWidget2.setXRange(
                    newplot.data["time"].min(),
                    newplot.data["time"].max(),
                )
                self.horizontalScrollBar_2.setMaximum(0)
                self.graphWidget2.setYRange(
                    newplot.data["amplitude"].min(),
                    newplot.data["amplitude"].max(),
                )
                self.timer2.stop()

    def UpdateGraphWidgets(self):
        for newplot in PlotLines1:
            if newplot.isstopped == False:
                if newplot.index <= (len(newplot.data)-1):
                    x_data = newplot.data["time"][: newplot.index]
                    y_data = newplot.data["amplitude"][: newplot.index]
                    newplot.data_line.setData(x_data, y_data)
                    if newplot.index >=100 and newplot.index <= newplot.data["time"].max():
                        self.graphWidget1.setXRange(newplot.data["time"][int(newplot.index-100+self.zoomFactorChannel2)],newplot.data["time"][newplot.index],padding=0)
        for newplot in PlotLines2:
            if newplot.isstopped == False:
                if newplot.index <= (len(newplot.data)-1):
                    x_data = newplot.data["time"][: newplot.index]
                    y_data = newplot.data["amplitude"][: newplot.index]
                    newplot.data_line.setData(x_data, y_data)
                    if newplot.index >=100 and newplot.index <= newplot.data["time"].max():
                        self.graphWidget2.setXRange(newplot.data["time"][int(newplot.index-100+self.zoomFactorChannel2)],newplot.data["time"][newplot.index],padding=0)


    def zoomInChannel1(self):
        x_min, x_max = self.graphWidget1.getViewBox().viewRange()[0]
        y_min, y_max = self.graphWidget1.getViewBox().viewRange()[1]
        if x_min+10 < x_max:
            self.zoomFactorChannel1 += 10
            self.graphWidget1.setXRange(x_min+10, x_max, padding=0)
        self.graphWidget1.setYRange(y_min*0.8, y_max*0.8)

        if self.connect_status:
                x_min, x_max = self.graphWidget2.getViewBox().viewRange()[0]
                y_min, y_max = self.graphWidget2.getViewBox().viewRange()[1]
                if x_min+10 < x_max:
                    self.zoomFactorChannel2 += 10
                    self.graphWidget2.setXRange(x_min+10, x_max, padding=0)
                self.graphWidget2.setYRange(y_min*0.8, y_max*0.8)


    def zoomInChannel2(self):
        x_min, x_max = self.graphWidget2.getViewBox().viewRange()[0]
        y_min, y_max = self.graphWidget2.getViewBox().viewRange()[1]
        if x_min+10 < x_max:
            self.zoomFactorChannel1 += 10
            self.graphWidget2.setXRange(x_min+10, x_max, padding=0)
        self.graphWidget2.setYRange(y_min*0.8, y_max*0.8)

        if self.connect_status:
                x_min, x_max = self.graphWidget1.getViewBox().viewRange()[0]
                y_min, y_max = self.graphWidget1.getViewBox().viewRange()[1]
                if x_min+10 < x_max:
                    self.zoomFactorChannel1 += 10
                    self.graphWidget1.setXRange(x_min+10, x_max, padding=0)
                self.graphWidget1.setYRange(y_min*0.8, y_max*0.8)

    def zoomOutChannel1(self):
        x_min, x_max = self.graphWidget1.getViewBox().viewRange()[0]
        y_min, y_max = self.graphWidget1.getViewBox().viewRange()[1]
        if x_min-10 < 0:
            self.graphWidget1.setYRange(y_min/0.8, y_max/0.8)
            self.graphWidget1.setXRange(0,x_max,padding=0)
        else:
            self.zoomFactorChannel1 -= 10
            self.graphWidget1.setXRange(x_min-10, x_max, padding=0)
            self.graphWidget1.setYRange(y_min/0.8, y_max/0.8)

        if self.connect_status:
            x_min, x_max = self.graphWidget2.getViewBox().viewRange()[0]
            y_min, y_max = self.graphWidget2.getViewBox().viewRange()[1]
            if x_min-10 < 0:
                self.graphWidget2.setYRange(y_min/0.8, y_max/0.8)
                self.graphWidget2.setXRange(0,x_max,padding=0)
            else:
                self.zoomFactorChannel2 -= 10
                self.graphWidget2.setXRange(x_min-10, x_max, padding=0)
                self.graphWidget2.setYRange(y_min/0.8, y_max/0.8)


    def zoomOutChannel2(self):
        x_min, x_max = self.graphWidget2.getViewBox().viewRange()[0]
        y_min, y_max = self.graphWidget2.getViewBox().viewRange()[1]
        if x_min-10 < 0:
            self.graphWidget2.setYRange(y_min/0.8, y_max/0.8)
            self.graphWidget2.setXRange(0,x_max,padding=0)
        else:
            self.zoomFactorChannel2 -= 10
            self.graphWidget2.setXRange(x_min-10, x_max, padding=0)
            self.graphWidget2.setYRange(y_min/0.8, y_max/0.8)

        if self.connect_status:
            x_min, x_max = self.graphWidget1.getViewBox().viewRange()[0]
            y_min, y_max = self.graphWidget1.getViewBox().viewRange()[1]
            if x_min-10 < 0:
                self.graphWidget1.setYRange(y_min/0.8, y_max/0.8)
                self.graphWidget1.setXRange(0,x_max,padding=0)
            else:
                self.zoomFactorChannel1 -= 10
                self.graphWidget1.setXRange(x_min-10, x_max, padding=0)
                self.graphWidget1.setYRange(y_min/0.8, y_max/0.8)


    def paused1(self):
        if self.ispaused1 == 0:
            self.ispaused1 = 1
        else:
            self.ispaused1 = 0

        if self.connect_status:
            if self.ispaused2 == 0:
             self.ispaused2 = 1
            else:
             self.ispaused2 = 0

    def paused2(self):
        if self.ispaused2 == 0:
            self.ispaused2 = 1
        else:
            self.ispaused2 = 0

        if self.connect_status:
            if self.ispaused1 == 0:
                self.ispaused1 = 1
            else:
                self.ispaused1 = 0


    def Move1(self):
        oldplot = self.GetChosenPlotLine1()
        if len(PlotLines1) == 0 or oldplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return
        newplot = PlotLine()
        newplot.data = oldplot.data  # Copy the data from the first plot to the new plot
        newplot.pen = oldplot.pen
        PlotLines2.append(newplot)
        newplot.name = "Signal " + str(len(PlotLines2))
        newplot.data_line = self.graphWidget2.plot(pen=newplot.pen,name=newplot.name)
        newplot.index = oldplot.index
        newplot.ChannelNum = 2
        # Clear the old data in the first graph if needed
        oldplot.index=0
        index = self.GetChosenIndex1()
        if index != -1:
            PlotLines1.pop(index)
        self.graphWidget1.removeItem(oldplot.data_line)
        list = []
        list.append(newplot.name)
        self.comboBox_2.addItems(list)
        self.comboBox.clear()
        self.legend1.clear()
        list= []
        list.append("Choose Channel")
        self.comboBox.addItems(list)
        if newplot.data["time"][len(newplot.data["time"]) - 1] > self.Xmax2:
            self.Xmax2 = newplot.data["time"][len(newplot.data["time"]) - 1]
        if newplot.data["amplitude"].min() < self.Ymin2:
            self.Ymin2 = newplot.data["amplitude"].min()
        if newplot.data["amplitude"].max() > self.Ymax2:
            self.Ymax2 = newplot.data["amplitude"].max()
        self.graphWidget2.setLimits(xMin = self.Xmin2, xMax = self.Xmax2, yMin = self.Ymin2, yMax = self.Ymax2)
        self.horizontalScrollBar_2.setMaximum(int(self.Xmax2))
        self.graphWidget2.setYRange(self.Ymin2,self.Ymax2)
        i = 0
        for newplot in PlotLines1:
            if newplot:
                newplot.name = "Signal " + str(i+1)
                newplot.data_line.setData(name=newplot.name)
                list=[]
                list.append(newplot.name)
                self.comboBox.addItems(list)
                self.legend1.addItem(newplot.data_line,name=newplot.name)
                i += 1
        # Clear the combo box and then get length and loop for names
        # Update the second graph to ensure the data is plotted
        if newplot.index >= (len(newplot.data)-1):
            newplot.data_line.setData(newplot.data["time"],newplot.data["amplitude"])
        self.UpdateGraphWidgets()
        self.update_plots2()

    def Move2(self):
        oldplot = self.GetChosenPlotLine2()
        if len(PlotLines2) == 0 or oldplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return
        newplot = PlotLine()
        newplot.data = oldplot.data  # Copy the data from the first plot to the new plot
        newplot.pen = oldplot.pen
        PlotLines1.append(newplot)
        newplot.name = "Signal " + str(len(PlotLines1))
        newplot.data_line = self.graphWidget1.plot(pen=newplot.pen,name=newplot.name)
        newplot.index = oldplot.index
        newplot.ChannelNum = 1
        # Clear the old data in the first graph if needed
        oldplot.index=0
        index = self.GetChosenIndex2()
        if index != -1:
            PlotLines2.pop(index)
        self.graphWidget2.removeItem(oldplot.data_line)
        list = []
        list.append(newplot.name)
        self.comboBox.addItems(list)
        self.comboBox_2.clear()
        self.legend2.clear()
        list= []
        list.append("Choose Channel")
        self.comboBox_2.addItems(list)
        if newplot.data["time"][len(newplot.data["time"]) - 1] > self.Xmax1:
            self.Xmax1 = newplot.data["time"][len(newplot.data["time"]) - 1]
        if newplot.data["amplitude"].min() < self.Ymin1:
            self.Ymin1 = newplot.data["amplitude"].min()
        if newplot.data["amplitude"].max() > self.Ymax1:
            self.Ymax1 = newplot.data["amplitude"].max()
        self.graphWidget1.setLimits(xMin = self.Xmin1, xMax = self.Xmax1, yMin = self.Ymin1, yMax = self.Ymax1)
        self.horizontalScrollBar.setMaximum(int(self.Xmax1))
        self.graphWidget1.setYRange(self.Ymin2,self.Ymax2)
        i = 0
        for newplot in PlotLines2:
            if newplot:
                newplot.name = "Signal " + str(i+1)
                newplot.data_line.setData(name=newplot.name)
                list=[]
                list.append(newplot.name)
                self.comboBox_2.addItems(list)
                self.legend2.addItem(newplot.data_line,name=newplot.name)
                i += 1
        # Clear the combo box and then get length and loop for names
        # Update the second graph to ensure the data is plotted
        if newplot.index >= (len(newplot.data)-1):
            newplot.data_line.setData(newplot.data["time"],newplot.data["amplitude"])
        self.UpdateGraphWidgets()
        self.update_plots1()


    def ConnectGraphs(self):
        if self.connect_status:
            # Disconnect the graphs
            self.connect_status = False
            if self.saved_view_range:
                x_range1, y_range1 = self.saved_view_range
                self.graphWidget1.setXRange(*x_range1, padding=0)
                self.graphWidget1.setYRange(*y_range1, padding=0)
                self.graphWidget2.getViewBox().disableAutoRange()
        else:
            # Connect the graphs
            self.connect_status = True
            self.ispaused2 = self.ispaused1
            # Save the current view range of the first graph
            x_range1, y_range1 = self.graphWidget1.getViewBox().viewRange()
            self.saved_view_range = (x_range1, y_range1)

            # Set the view range and signal speed of the second graph to match the first
            x_range1, y_range1 = self.saved_view_range
            signal1_speed = self.signal1speed

            self.graphWidget1.setXRange(*x_range1, padding=0)
            self.graphWidget1.setYRange(*y_range1, padding=0)
            self.graphWidget2.setXRange(*x_range1, padding=0)
            self.signal2speed = signal1_speed

    def changesignal1speed25(self):
        self.signal1speed = 0.25
        if self.connect_status:
            self.signal2speed = 0.25

    def changesignal1speed50(self):
        self.signal1speed = 0.5
        if self.connect_status:
            self.signal2speed = 0.5

    def changesignal1speed100(self):
        self.signal1speed = 1
        if self.connect_status:
            self.signal2speed = 1

    def changesignal1speed150(self):
        self.signal1speed = 1.5
        if self.connect_status:
            self.signal2speed = 1.5

    def changesignal1speed200(self):
        self.signal1speed = 2
        if self.connect_status:
            self.signal2speed = 2

    def changesignal2speed25(self):
        self.signal2speed = 0.25
        if self.connect_status:
            self.signal1speed = 0.25

    def changesignal2speed50(self):
        self.signal2speed = 0.5
        if self.connect_status:
            self.signal1speed = 0.5

    def changesignal2speed100(self):
        self.signal2speed = 1
        if self.connect_status:
            self.signal1speed = 1

    def changesignal2speed150(self):
        self.signal2speed = 1.5
        if self.connect_status:
            self.signal1speed = 1.5

    def changesignal2speed200(self):
        self.signal2speed = 2
        if self.connect_status:
            self.signal1speed = 2

    def clear1(self):
        if self.timer1.isActive() == True:
            self.timer1.stop()
        self.graphWidget1.clear()
        self.graphWidget1.setXRange(0, 1)
        global PlotLines1
        for item in PlotLines1:
            del item
        PlotLines1 = []
        self.comboBox.clear()
        list = ["Choose Channel"]
        self.comboBox.addItems(list)

    def clear2(self):
        if self.timer2.isActive() == True:
            self.timer2.stop()
        global PlotLines2
        self.graphWidget2.clear()
        self.graphWidget2.setXRange(0, 1)
        for item in PlotLines2:
            del item
        PlotLines2 = []
        self.comboBox_2.clear()
        list = ["Choose Channel"]
        self.comboBox_2.addItems(list)

    def addtitle1(self):
        dialog = InputDialog(self)
        result = dialog.exec_()  # This will block until the user closes the dialog

        if result == QtWidgets.QDialog.Accepted:
            user_input = dialog.input_text.text()
            # Do something with the user input, e.g., display it in a message box
            self.label.setText(user_input)
            msg = QMessageBox()
            msg.setWindowTitle("User Input")
            msg.setText("You entered: " + user_input)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

    def addtitle2(self):
        dialog = InputDialog(self)
        result = dialog.exec_()  # This will block until the user closes the dialog

        if result == QtWidgets.QDialog.Accepted:
            user_input = dialog.input_text.text()
            # Do something with the user input, e.g., display it in a message box
            self.label_2.setText(user_input)
            msg = QMessageBox()
            msg.setWindowTitle("User Input")
            msg.setText("You entered: " + user_input)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

    def SnapshotChannel1(self):
        # Capture the content of the graphWidget1 widget
        pixmap = self.graphWidget1.grab() 
        image = pixmap.toImage()
        snapshots1.append(image)
        while len(snapshots1)>3:
            snapshots1.pop()
        image.save("snapshot_channel1" + str(len(snapshots1)) + ".png")
        # Display a message to the user
        msg = QMessageBox()
        msg.setWindowTitle("Snapshot Saved")
        msg.setText("Snapshot_channel1" + str(len(snapshots1)) + ".png")
        msg.setInformativeText("Note That the Maxiumum viewable Snapshots in the report is 3.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        

    def SnapshotChannel2(self):
        # Capture the content of the graphWidget1 widget
        pixmap = self.graphWidget2.grab()
        image = pixmap.toImage()
        snapshots2.append(image)
        while len(snapshots2)>3:
            snapshots2.pop()
        image.save("snapshot_channel2" + str(len(snapshots2)) + ".png")
        # Display a message to the user
        msg = QMessageBox()
        msg.setWindowTitle("Snapshot Saved")
        msg.setText("Snapshot_channel2" + str(len(snapshots2)) + ".png")
        msg.setInformativeText("Note That the Maxiumum viewable Snapshots in the report is 3.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def create_pdf_with_qimages(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 15)
        pdf.cell(200, 5, align="C", txt="Signal Viewer Report", ln=True)
        
        pdf.set_y(30)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 5, align="C", txt="Plotwidget 1 Snapshots ", ln=True)
        mypdf = "Signal Viewer Report" + str(len(snapshots1) + len(snapshots2)) +".pdf"
        i = 0
        if len(snapshots1)>=3:
            while i < len(snapshots1):
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+10
                y = (page_height - image_height) / 2
                pdf.image(
                    "snapshot_channel1" + str(i + 1) + ".png",
                    x=(x * i),
                    y=50,
                    w=image_width,
                    h=image_height,
                )
                i += 1
        elif len(snapshots1)==2:
             while i < len(snapshots1):
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+50
                y = (page_height - image_height) / 2
                if i==0:
                     pdf.image(
                    "snapshot_channel1" + str(i + 1) + ".png",
                    x=((page_width - image_width) / 2)-20,
                    y=50,
                    w=image_width,
                    h=image_height,
                )
                else:
                    
                    pdf.image(
                        "snapshot_channel1" + str(i + 1) + ".png",
                        x=(x * i),
                        y=50,
                        w=image_width,
                        h=image_height,
                    )
                i += 1
        elif len(snapshots1)==1:
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+16
                y = (page_height - image_height) / 2
                pdf.image(
                    "snapshot_channel1" + str(i + 1) + ".png",
                    x=(x),
                    y=50,
                    w=image_width,
                    h=image_height,
                )
            
            
        pdf.set_y(120)
        pdf.cell(200, 5, align="C", txt="Plotwidget 2 Snapshots ", ln=True)
        pdf.set_font(
            "Arial",
            size=10,
        )
        i = 0
        if len(snapshots2)>=3:
            while i < len(snapshots2):
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+10
                y = (page_height - image_height) / 2
                pdf.image(
                    "snapshot_channel2" + str(i + 1) + ".png",
                    x=(x * i),
                    y=140,
                    w=image_width,
                    h=image_height,
                )
                i += 1
        elif len(snapshots2)==2:
             while i < len(snapshots2):
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+50
                y = (page_height - image_height) / 2
                if i==0:
                     pdf.image(
                    "snapshot_channel2" + str(i + 1) + ".png",
                    x=((page_width - image_width) / 2)-20,
                    y=140,
                    w=image_width,
                    h=image_height,
                )
                else:
                    
                    pdf.image(
                        "snapshot_channel2" + str(i + 1) + ".png",
                        x=(x * i),
                        y=140,
                        w=image_width,
                        h=image_height,
                    )
                i += 1
        elif len(snapshots2)==1:
                image_width = 50  # Set the desired image width
                image_height = 50  # Set the desired image height
                page_width = pdf.w - 2 * pdf.l_margin
                page_height = pdf.h - 2 * pdf.t_margin

                x = ((page_width - image_width) / 2)+16
                y = (page_height - image_height) / 2
                pdf.image(
                    "snapshot_channel2" + str(i + 1) + ".png",
                    x=(x),
                    y=140,
                    w=image_width,
                    h=image_height,
                )
        
        self.channelstatistics()
        counter2=0
        for plotline1 in PlotLines1:
            counter2+=1
            plotline1.StatisticalData=[
                [
                 "Signal "+str(counter2)+" "+"time mean",
                 "Signal "+str(counter2)+" "+"amplitude mean",
                 "Signal "+str(counter2)+" "+"maximum time",
                 "Signal "+str(counter2)+" "+"maximum amplitude",

                ],
                [
                    plotline1.timeMean,
                    plotline1.amplitudeMean,
                    plotline1.maxmiumTime,
                    plotline1.maxmiumAmplitude,
                ]
            ]
            counter3=0
            for plotline2 in PlotLines2:
             counter3+=1
             plotline2.StatisticalData=[
                [
                 "Signal "+str(counter3)+" "+"time mean",
                 "Signal "+str(counter3)+" "+"amplitude mean",
                 "Signal "+str(counter3)+" "+"maximum time",
                 "Signal "+str(counter3)+" "+"maximum amplitude",

                ],
                [
                    plotline2.timeMean,
                    plotline2.amplitudeMean,
                    plotline2.maxmiumTime,
                    plotline2.maxmiumAmplitude,
                ]
            ]
        pdf.set_y(200)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 5, align="C", txt="Plot widget 1 Signals Statistics", ln=True)
        pdf.set_font(
            "Arial",
            size=10,
        )
        col_width = pdf.w / 4.5
        row_height = 20

        pdf.set_y(220)
        x=220
        # Add a table at the bottom
        for plotline1 in PlotLines1:
            
            x+=60
            for row in plotline1.StatisticalData:
                if plotline1.StatisticalData.index(row) == 0:
                    pdf.set_font("Arial", "B", 9)
                else:
                    pdf.set_font("Arial", size=9)
                for item in row:
                    pdf.cell(col_width, row_height, str(item), border=1, ln=False)
                pdf.ln(row_height)
            pdf.set_y(x)
        x-=250
        pdf.set_y(x)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 5, align="C", txt="Plot widget 2 Signals Statistics", ln=True)
        pdf.set_font(
            "Arial",
            size=10,
        )
        x-=260
        pdf.set_y(x)
        

        for plotline2 in PlotLines2:
            x+=60
            for row in plotline2.StatisticalData:
                if plotline2.StatisticalData.index(row) == 0:
                    pdf.set_font("Arial", "B", 9)
                else:
                    pdf.set_font("Arial", size=9)
                for item in row:
                    pdf.cell(col_width, row_height, str(item), border=1, ln=False)
                pdf.ln(row_height)
            pdf.set_y(x)
        pdf.output(mypdf)

    def channelstatistics(self):
            for plotline1 in PlotLines1:
                timesum=round(plotline1.data["time"].sum(),2)
                amplitude_sum=round(plotline1.data["amplitude"].sum(),2)
                plotline1.timeMean=round(timesum/len(plotline1.data["time"]),2)
                plotline1.amplitudeMean=round(amplitude_sum/len(plotline1.data["amplitude"]),2)
                plotline1.maxmiumAmplitude=round(plotline1.data["amplitude"].max(),2)
                plotline1.minimumAmplitude=round(plotline1.data["amplitude"].min(),2)
                plotline1.maxmiumTime=round(plotline1.data["time"].max(),2)
            
            for plotline2 in PlotLines2:
                timesum=round(plotline2.data["time"].sum(),2)
                amplitude_sum=round(plotline2.data["amplitude"].sum(),2)
                plotline2.timeMean=round(timesum/len(plotline2.data["time"]),2)
                plotline2.amplitudeMean=round(amplitude_sum/len(plotline2.data["amplitude"]),2)
                plotline2.maxmiumAmplitude=round(plotline2.data["amplitude"].max(),2)
                plotline2.minimumAmplitude=round(plotline2.data["amplitude"].min(),2)
                plotline2.maxmiumTime=round(plotline2.data["time"].max(),2)

    def GetChosenPlotLine1(self):
        Index = self.comboBox.currentIndex()
        if Index != 0:
            return PlotLines1[Index - 1]
        else:
            return -1

    def GetChosenPlotLine2(self):
        Index = self.comboBox_2.currentIndex()
        if Index != 0:
            return PlotLines2[Index - 1]
        else:
            return -1
        
    def GetChosenIndex1(self):
        Index = self.comboBox.currentIndex()
        if Index != 0:
            return Index - 1
        else:
            return -1
    
    def GetChosenIndex2(self):
        Index = self.comboBox_2.currentIndex()
        if Index != 0:
            return Index -1
        else:
            return -1

    def ChangeColor1(self):
        newplot = self.GetChosenPlotLine1()
        if len(PlotLines1) == 0 or newplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return
        color = colorchooser.askcolor()
        if color[1]:
            selected_color = color[0]
            r, g, b = map(int, selected_color)  # Extract RGB values
            newplot.data_line.setPen(pg.mkPen(color=(r, g, b)))
            newplot.pen = pg.mkPen(color=(r, g, b))
        else:
            self.ErrorMsg("No Chosen Color")

    def ChangeColor2(self):
        newplot = self.GetChosenPlotLine2()
        if len(PlotLines2) == 0 or newplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return
        color = colorchooser.askcolor()
        if color[1]:
            selected_color = color[0]
            r, g, b = map(int, selected_color)  # Extract RGB values

            newplot.data_line.setPen(pg.mkPen(color=(r, g, b)))
            newplot.pen = pg.mkPen(color=(r, g, b))
        else:
            self.ErrorMsg("No Chosen Color")


    def ScrollChannel1(self):
        if self.ispaused1 == 1:
            scroll_value = self.horizontalScrollBar.value()
            # Calculate the new view range based on the scroll value and zoom factor
            xmin = self.graphWidget1.getViewBox().viewRange()[0][0]
            xmax = self.graphWidget1.getViewBox().viewRange()[0][1]
            xrange = xmax - xmin
            if scroll_value - xrange >= 0:
                new_x_min = scroll_value - xrange
                new_x_max = scroll_value    
            else:
                new_x_min=0
                new_x_max=xrange
                scroll_value = 0
                # Update the view range of the plot widget to scroll the graph window
            self.graphWidget1.setXRange(new_x_min, new_x_max, padding=0)
            if self.connect_status == True:
                self.horizontalScrollBar_2.setValue(scroll_value)
                self.graphWidget2.setXRange(new_x_min,new_x_max,padding=0)

    def ScrollChannel2(self):
        if self.ispaused2 == 1:
            scroll_value = self.horizontalScrollBar_2.value()
            # Calculate the new view range based on the scroll value and zoom factor
            xmin = self.graphWidget2.getViewBox().viewRange()[0][0]
            xmax = self.graphWidget2.getViewBox().viewRange()[0][1]
            xrange = xmax - xmin
            if scroll_value - xrange >= 0:
                new_x_min = scroll_value - xrange
                new_x_max = scroll_value    
            else:
                new_x_min=0
                new_x_max=xrange
                scroll_value = 0
            # Update the view range of the plot widget to scroll the graph window
            self.graphWidget2.setXRange(new_x_min, new_x_max, padding=0)
            if self.connect_status == True:
                self.horizontalScrollBar.setValue(scroll_value)
                self.graphWidget1.setXRange(new_x_min,new_x_max,padding=0)