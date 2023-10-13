from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import pyqtgraph as pg
import pandas as pd
import sys
import numpy 
from PyQt5.QtCore import QTimer 

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #loading ui file
        self.ui=uic.loadUi('sheboandm7md.ui', self)
        # Connect widgets to methods here
        self.actionZoomOut.triggered.connect(self.print)
        self.actionChannel1.triggered.connect(self.loadChannel1)
        self.actionChannel2.triggered.connect(self.loadChannel2)
        self.actionShow_Hide.triggered.connect(self.showHideChannel1)
        self.actionHide2.triggered.connect(self.showHideChannel2)
        #setting plotting graph color to grey
        pg.setConfigOption('background', '#1f1f1f')
        #creating plot widget 
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget1.setMaximumSize(1000,1000)
        self.graphWidget1.setMinimumSize(400,400)
        self.graphWidget2.setMinimumSize(400,400)
        self.graphWidget2.setMaximumSize(1000,1000)
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)
        self.ishidden1=0
        self.ishidden2=0
    def loadChannel1(self):
       filename = QtWidgets.QFileDialog.getOpenFileName()
       path = filename[0]
       print(path)
       with open( path , 'r') as data:
         x = []
         y = []
         for line in data:
            p = line.split()
            x.append(float(p[0]))   
            y.append(float(p[1]))
            self.graphWidget1.plot(x,y)
            # timer = QTimer()
            # timer.timeout.connect(self.graphWidget1.plot(x,y))
            # timer.start(1000)  # Update the plot every 1000 milliseconds (1 second)


    # def update_plot():
    # # Update your data (e.g., by reading new data from the .txt file)
    #     filename = QtWidgets.QFileDialog.getOpenFileName()
    #     path = filename[0]
    #     print(path)
    #     new_data = numpy.loadtxt(path)
    
    # # Clear the old data from the plot
    #     plot_widget.clear()
    
    # # Create a new scatter plot with the updated data
    #     scatter_plot = pg.ScatterPlotItem(data=new_data, pen=None, brush='b', symbol='o', size=5)
    #     plot_widget.addItem(scatter_plot)


        
    def loadChannel2(self):
       filename = QtWidgets.QFileDialog.getOpenFileName()
       path = filename[0]
       print(path)
       with open( path , 'r') as data:
         x = []
         y = []
         for line in data:
            p = line.split()
            x.append(float(p[0]))   
            y.append(float(p[1]))
         self.graphWidget2.plot(x,y)
     
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
    def print(self):
        print("clicked")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())