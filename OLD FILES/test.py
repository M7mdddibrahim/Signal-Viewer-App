from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time
from matplotlib import animation
import sys


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # loading ui file
        self.ui = uic.loadUi("sheboandm7md.ui", self)
        # Connect widgets to methods here
        self.actionZoomOut.triggered.connect(self.print)
        self.actionChannel1.triggered.connect(self.draw1)
        self.actionChannel2.triggered.connect(self.draw2)
        self.actionShow_Hide.triggered.connect(self.showHideChannel1)
        self.actionHide2.triggered.connect(self.showHideChannel2)
        # setting plotting graph color to grey
        pg.setConfigOption("background", "#1f1f1f")
        # creating plot widget
        self.graphWidget1 = MplCanvas(self, width=5, height=8, dpi=100)
        self.graphWidget2 = MplCanvas(self, width=5, height=8, dpi=100)
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)
        self.ishidden1 = 0
        self.ishidden2 = 0
        self.animation = None
        self.path1 = ""
        self.path2 = ""

    # this is considerd the new load function using matplotlib
    def draw1(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        self.path1 = filename[0]
        self.graphWidget1.axes.clear()
        data = pd.read_csv(self.path1)
        x = data["time"].tolist()
        y = data["amplitude"].tolist()

        self.graphWidget1.axes.clear()

        self.graphWidget1.draw()

        self.animation = animation.FuncAnimation(
            self.graphWidget1.figure,
            self.update_plot1,
            frames=len(x),
            interval=1500,
            repeat=False,
        )

    # this function is called every 1 secoud to update plot
    def update_plot1(self, frame):
        # Update the plot with new data for the current frame (e.g., simulate streaming data)
        data = pd.read_csv(self.path1)
        x = data["time"].tolist()[: frame + 1]
        y = data["amplitude"].tolist()[: frame + 1]
        self.graphWidget1.axes.clear()
        self.graphWidget1.axes.plot(x, y)
        self.graphWidget1.draw()

    # this the old function in case we need it
    def draw2(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        self.path2 = filename[0]
        self.graphWidget1.axes.clear()
        data = pd.read_csv(self.path2)
        x = data["time"].tolist()
        y = data["amplitude"].tolist()

        self.graphWidget2.axes.clear()

        self.graphWidget2.draw()

        self.animation = animation.FuncAnimation(
            self.graphWidget2.figure,
            self.update_plot2,
            frames=len(x),
            interval=800,
            repeat=False,
        )

    def update_plot2(self, frame):
        # Update the plot with new data for the current frame (e.g., simulate streaming data)
        data = pd.read_csv(self.path2)
        x = data["time"].tolist()[: frame + 1]
        y = data["amplitude"].tolist()[: frame + 1]
        self.graphWidget2.axes.clear()
        self.graphWidget2.axes.plot(x, y)
        self.graphWidget2.draw()

    def loadChannel1(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)
        with open(path, "r") as data:
            x = []
            y = []
            for line in data:
                p = line.split()
                x.append(float(p[0]))
                y.append(float(p[1]))
            self.graphWidget1.plot(x, y)

    def loadChannel2(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)
        with open(path, "r") as data:
            x = []
            y = []
            for line in data:
                p = line.split()
                x.append(float(p[0]))
                y.append(float(p[1]))
            self.graphWidget2.plot(x, y)

    def showHideChannel1(self):
        if self.ishidden1 == 0:
            self.graphWidget1.hide()
            self.ishidden1 = 1
        else:
            self.graphWidget1.show()
            self.ishidden1 = 0

    def showHideChannel2(self):
        if self.ishidden2 == 0:
            self.graphWidget2.hide()
            self.ishidden2 = 1
        else:
            self.graphWidget2.show()
            self.ishidden2 = 0

    def print(self):
        print("clicked")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
