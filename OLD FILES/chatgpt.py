import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer


class MedicalSignalViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePlot)

        self.signal_data = {"time": [], "signal": []}
        self.plot_data = None

    def initUI(self):
        self.setWindowTitle("Medical Signal Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.plotWidget = plt.figure()

        self.loadButton = QPushButton("Load Medical Signal")
        self.loadButton.clicked.connect(self.loadMedicalSignal)

        self.layout.addWidget(self.plotWidget.canvas)
        self.layout.addWidget(self.loadButton)

    def loadMedicalSignal(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Medical Signal File", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)", options=options
        )

        if file_path:
            data = np.genfromtxt(file_path, delimiter=',')
            self.signal_data["time"] = data[:, 0]
            self.signal_data["signal"] = data[:, 1]

            self.plot_data = plt.plot(self.signal_data["time"], self.signal_data["signal"])[0]
            plt.xlabel("Time")
            plt.ylabel("Signal Amplitude")
            plt.title("Medical Signal")
            plt.grid(True)

            self.timer.start(1000)  # Start the timer to update the plot every 1 second

    def updatePlot(self):
        if self.plot_data is not None:
            num_points = len(self.signal_data["time"])
            if self.plot_data.get_xdata().size < num_points:
                new_xdata = self.signal_data["time"][self.plot_data.get_xdata().size:]
                new_ydata = self.signal_data["signal"][self.plot_data.get_xdata().size:]
                self.plot_data.set_xdata(np.append(self.plot_data.get_xdata(), new_xdata))
                self.plot_data.set_ydata(np.append(self.plot_data.get_ydata(), new_ydata))
                self.plotWidget.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = MedicalSignalViewer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
