from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget , QInputDialog
import pyqtgraph as pg
import pandas as pd
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi('sheboandm7md.ui', self)
        # Connect widgets to methods here
        self.actionZoomOut.triggered.connect(self.print)
        # self.actionChannel_1.triggered.connect(self.load)
        pg.setConfigOption('background', '#1f1f1f')
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)
        self.actionChannel1.triggered.connect(self.actionChannel1_handler)
        self.actionChannel2.triggered.connect(self.actionChannel2_handler)


    def open_dialog_box(self):
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
     


    def actionChannel1_handler(self):
          # print("button pressed")
     self.open_dialog_box()
     
    def actionChannel2_handler(self):
          # print("button pressed")
     self.open_dialog_box()
    
          
    def print(self):
        print("clicked")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())