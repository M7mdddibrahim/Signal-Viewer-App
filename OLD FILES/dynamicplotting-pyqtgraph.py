from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import pandas as pd

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.data = pd.read_csv('ECG1.csv')  # Replace 'your_data.csv' with the actual file path
        self.index = 0

    def update_plot_data(self):
        if self.index < len(self.data):
            self.data_line.setData(self.data['time'][:self.index + 1], self.data['amplitude'][:self.index + 1])
            self.index += 1
        else:
            self.timer.stop()
        
        self.graphWidget.setXRange(0,0.004)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
