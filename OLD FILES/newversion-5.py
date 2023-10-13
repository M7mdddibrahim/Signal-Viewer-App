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


class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)
        self.setWindowTitle("Input Dialog")

        layout = QtWidgets.QVBoxLayout(self)

        self.input_label = QtWidgets.QLabel("Enter title:")
        self.input_text = QtWidgets.QLineEdit(self)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)

        self.ok_button = QtWidgets.QPushButton("OK", self)
        layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.reject)


class PLotLine:
    def __init__(self):
        self.data = None
        self.index = 0
        self.data_line = None
        self.pen = None
        self.name = None
        self.ishidden = False
        self.ChannelNum = None
        # self.timer


PlotLines1 = []
PlotLines2 = []
snapshots1 = []
snapshots2 = []

ext = (".txt", ".csv")


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # loading ui file
        self.ui = uic.loadUi("GUI-3.ui", self)
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
        self.actionSave_As_PDF.triggered.connect(self.create_pdf_with_qimages)
        self.actionConnect.triggered.connect(self.ConnectGraphs)
        # setting plotting graph color to grey
        pg.setConfigOption("background", "#1f1f1f")
        pd.options.display.max_rows = 999999
        # creating plot widget
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget1.setMaximumSize(1000, 1000)
        self.graphWidget1.setMinimumSize(400, 400)
        self.graphWidget2.setMinimumSize(400, 400)
        self.graphWidget2.setMaximumSize(1000, 1000)
        self.ui.gridLayout_2.addWidget(self.graphWidget1)
        self.ui.gridLayout_3.addWidget(self.graphWidget2)
        self.data_line = None
        self.ishidden1 = 0
        self.ishidden2 = 0
        self.zoomFactorChannel1 = 1.0
        self.zoomFactorChannel2 = 1.0
        self.ispaused1 = 0
        self.ispaused2 = 0
        self.signal1speed = 1
        self.signal2speed = 1
        self.actionmove.triggered.connect(self.Move1)
        self.actionMove2.triggered.connect(self.Move2)
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

    def DrawChannel1(self):
        self.load1()
        newplot = PlotLines1[-1]
        pen = pg.mkPen(color=(255, 0, 0))
        name = "Signal" + str(len(PlotLines1))
        newplot.data_line = self.graphWidget1.plot(pen=pen, name=name)
        self.index = 0
        newplot.name = "Signal " + str(len(PlotLines1))
        list = []
        list.append(newplot.name)
        self.comboBox.addItems(list)

        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(int(50 / self.signal1speed))
        self.timer1.timeout.connect(
            self.update_plots1
        )  # Connect to a single update method
        self.timer1.start()

    def DrawChannel2(self):
        self.load2()
        newplot = PlotLines2[-1]
        pen = pg.mkPen(color=(255, 0, 0))
        name = "Signal" + str(len(PlotLines2))
        newplot.data_line = self.graphWidget2.plot(pen=pen, name=name)
        self.index = 0
        newplot.name = "Signal " + str(len(PlotLines2))
        list = []
        list.append(newplot.name)
        self.comboBox_2.addItems(list)

        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(int(50 / self.signal2speed))
        self.timer2.timeout.connect(
            self.update_plots2
        )  # Connect to a single update method
        self.timer2.start()

    def load1(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        if path.endswith(ext):
            if path.endswith(".txt"):
                with open(path, "r") as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PLotLine()
                newplot.data = pd.DataFrame({"time": x, "amplitude": y})
                PlotLines1.append(newplot)
                newplot.ChannelNum = 1
            else:
                newplot = PLotLine()
                newplot.data = pd.read_csv(path, usecols=["time", "amplitude"])
                PlotLines1.append(newplot)
                newplot.ChannelNum = 1
        else:
            self.ErrorMsg("You can only load .txt or .csv files.")

    def load2(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        if path.endswith(ext):
            if path.endswith(".txt"):
                with open(path, "r") as data:
                    x = []
                    y = []
                    for line in data:
                        p = line.split()
                        x.append(float(p[0]))
                        y.append(float(p[1]))
                newplot = PLotLine()
                newplot.data = pd.DataFrame({"time": x, "amplitude": y})
                PlotLines2.append(newplot)
                newplot.ChannelNum = 2
            else:
                newplot = PLotLine()
                newplot.data = pd.read_csv(path, usecols=["time", "amplitude"])
                PlotLines2.append(newplot)
                newplot.ChannelNum = 2
        else:
            self.ErrorMsg("You can only load .txt or .csv files.")

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

    def ErrorMsg(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def update_plots1(self):
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(int(50 / self.signal1speed))
        self.timer1.timeout.connect(
            self.update_plots1
        )  # Connect to a single update method
        self.timer1.start()

        # Connect to a single update method
        if self.ispaused1 == 0:
            for newplot in PlotLines1:
                if newplot.index < len(newplot.data):
                    x_data = newplot.data["time"][: newplot.index + 1]
                    y_data = (
                        newplot.data["amplitude"][: newplot.index + 1]
                        * self.zoomFactorChannel1
                    )
                    newplot.data_line.setData(x_data, y_data)
                    self.graphWidget1.setXRange(
                        newplot.data["time"][newplot.index],
                        newplot.data["time"][newplot.index],
                        padding=0,
                    )

                    newplot.index += 1
        elif self.ispaused1 == 1:
            pass

            # Check if all data is plotted; if so, stop the timer
        if all(newplot.index >= len(newplot.data) for newplot in PlotLines1) and all(
            newplot.index >= len(newplot.data) for newplot in PlotLines2
        ):
            self.graphWidget1.setXRange(
                newplot.data["time"][0],
                newplot.data["time"][len(newplot.data["time"]) - 1],
            )
            self.timer1.stop()

    def update_plots2(self):
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(int(50 / self.signal2speed))
        self.timer2.timeout.connect(
            self.update_plots2
        )  # Connect to a single update method
        self.timer2.start()

        if self.ispaused2 == 0:
            for newplot in PlotLines2:
                if newplot.index < len(newplot.data):
                    x_data = newplot.data["time"][: newplot.index + 1]
                    y_data = (
                        newplot.data["amplitude"][: newplot.index + 1]
                        * self.zoomFactorChannel2
                    )
                    newplot.data_line.setData(x_data, y_data)
                    self.graphWidget2.setXRange(
                        newplot.data["time"][newplot.index],
                        newplot.data["time"][newplot.index],
                        padding=0,
                    )

                    newplot.index += 1
        elif self.ispaused2 == 1:
            pass
        if all(newplot.index >= len(newplot.data) for newplot in PlotLines2):
            self.graphWidget2.setXRange(
                newplot.data["time"][0],
                newplot.data["time"][len(newplot.data["time"]) - 1],
            )
            self.timer2.stop()

    def zoomInChannel1(self):
        self.zoomFactorChannel1 *= 2.0  # Adjust the zoom factor as needed
        self.update_plots1()

    def zoomInChannel2(self):
        self.zoomFactorChannel2 *= 2.0  # Adjust the zoom factor as needed
        self.update_plots2()

    def zoomOutChannel1(self):
        self.zoomFactorChannel1 /= 2.0  # Adjust the zoom factor as needed
        self.update_plots1()

    def zoomOutChannel2(self):
        self.zoomFactorChannel2 /= 2.0  # Adjust the zoom factor as needed
        self.update_plots2()

    def paused1(self):
        if self.ispaused1 == 0:
            self.ispaused1 = 1
        else:
            self.ispaused1 = 0

    def paused2(self):
        if self.ispaused2 == 0:
            self.ispaused2 = 1
        else:
            self.ispaused2 = 0


    def Move1(self):
        oldplot = self.GetChosenPlotLine1()
        if len(PlotLines1) == 0 or oldplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return

        newplot = PLotLine()
        newplot.data = oldplot.data  # Copy the data from the first plot to the new plot

        pen = pg.mkPen(color=(255, 0, 0))
        name = "Signal" + str(len(PlotLines2))
        newplot.data_line = self.graphWidget2.plot(pen=pen, name=name)

        # Make sure the data is within the visible range of the second graph
        self.graphWidget2.setXRange(newplot.data["time"].min(), newplot.data["time"].max())

        PlotLines2.append(newplot)
        newplot.index = 0
        newplot.ChannelNum = 2

        # Clear the old data in the first graph if needed
        oldplot.data_line.clear()

        # Update the second graph to ensure the data is plotted
        self.update_plots2()

    def Move2(self):
        oldplot = self.GetChosenPlotLine2()
        if len(PlotLines2) == 0 or oldplot == -1:
            self.ErrorMsg("No Signal Chosen")
            return

        newplot = PLotLine()
        newplot.data = oldplot.data  # Copy the data from the second plot to the new plot

        pen = pg.mkPen(color=(255, 0, 0))
        name = "Signal" + str(len(PlotLines1))
        newplot.data_line = self.graphWidget1.plot(pen=pen, name=name)

        # Make sure the data is within the visible range of the first graph
        self.graphWidget1.setXRange(newplot.data["time"].min(), newplot.data["time"].max())

        PlotLines1.append(newplot)
        newplot.index = 0
        newplot.ChannelNum = 1

        # Clear the old data in the second graph if needed
        oldplot.data_line.clear()

        # Update the first graph to ensure the data is plotted
        self.update_plots1()

    # def ConnectGraphs(self):
    #     # Get properties of the first graph (graphWidget1)
    #     x_range1 = self.graphWidget1.getViewBox().viewRange()[0]
    #     signal1_speed = self.signal1speed

    #     # Apply properties to the second graph (graphWidget2)
    #     self.graphWidget2.setXRange(x_range1[0], x_range1[1], padding=0)
    #     self.signal2speed = signal1_speed
    #     self.update_plots2()

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

    def changesignal1speed50(self):
        self.signal1speed = 0.5

    def changesignal1speed100(self):
        self.signal1speed = 1

    def changesignal1speed150(self):
        self.signal1speed = 1.5

    def changesignal1speed200(self):
        self.signal1speed = 2

    def changesignal2speed25(self):
        self.signal2speed = 0.25

    def changesignal2speed50(self):
        self.signal2speed = 0.5

    def changesignal2speed100(self):
        self.signal2speed = 1

    def changesignal2speed150(self):
        self.signal2speed = 1.5

    def changesignal2speed200(self):
        self.signal2speed = 2

    def clear1(self):
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
        image.save("snapshot_channel1" + str(len(snapshots1)) + ".png")

        # Display a message to the user
        msg = QMessageBox()
        msg.setWindowTitle("Snapshot Saved")
        msg.setText("Snapshot_channel1" + str(len(snapshots1)) + ".png")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def SnapshotChannel2(self):
        # Capture the content of the graphWidget1 widget
        pixmap = self.graphWidget2.grab()
        image = pixmap.toImage()
        snapshots2.append(image)
        image.save("snapshot_channel2" + str(len(snapshots2)) + ".png")

        # Display a message to the user
        msg = QMessageBox()
        msg.setWindowTitle("Snapshot Saved")
        msg.setText("Snapshot_channel2" + str(len(self.snapshots2)) + ".png")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def create_pdf_with_qimages(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(
            "Arial",
            size=10,
        )
        pdf.cell(200, 5, align="C", txt="Signal Viewer Report", ln=True)
        mypdf = "Signal Viewer Report" + str(len(snapshots1) + len(snapshots2))
        i = 0
        while i < len(snapshots1):
            image_width = 50  # Set the desired image width
            image_height = 50  # Set the desired image height
            page_width = pdf.w - 2 * pdf.l_margin
            page_height = pdf.h - 2 * pdf.t_margin

            x = (page_width - image_width) / 2
            y = (page_height - image_height) / 2
            pdf.image(
                "snapshot_channel1" + str(i + 1) + ".png",
                x=(x * i),
                y=90,
                w=image_width,
                h=image_height,
            )
            i += 1
        c = 0
        while c < len(snapshots2):
            image_width = 50  # Set the desired image width
            image_height = 50  # Set the desired image height
            page_width = pdf.w - 2 * pdf.l_margin
            page_height = pdf.h - 2 * pdf.t_margin

            x = (page_width - image_width) / 2
            y = (page_height - image_height) / 2
            pdf.image(
                "snapshot_channel2" + str(c + 1) + ".png",
                x=(x * c),
                y=150,
                w=image_width,
                h=image_height,
            )
            c += 1
        self.channelstatistics()
        data = [
            [
                "Channel 1 time mean",
                "Channel 2 time mean",
                "Channel 1 amplitude mean",
                "Channel 2 amplitude mean",
            ],  # 'testing','size'],
            [
                self.time_mean1,
                self.time_mean2,
                self.amplitude_mean1,
                self.amplitude_mean2,
            ],  # 'testing','size'],
        ]
        Data = [
            [
                "Channel 1 max time",
                "Channel 2 max time",
                "Channel 1 min time",
                "Channel 2 min time",
            ],  # 'testing','size'],
            [
                self.max1,
                self.max2,
                self.min1,
                self.min2,
            ],  # 'testing','size'],
        ]
        col_width = pdf.w / 4.5
        row_height = 20

        pdf.set_y(25)
        # Add a table at the bottom
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1, ln=False)
            pdf.ln(row_height)
        # Calculate the vertical position (y) to align at the bottom
        y = pdf.h - 10 - pdf.b_margin - len(data) * row_height
        pdf.set_y(y)
        for row in Data:
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1, ln=False)
            pdf.ln(row_height)

        pdf.output(mypdf)

    def channelstatistics(self):
        channel1plot = PlotLines1[-1]
        channel2plot = PlotLines2[-1]
        self.channel1_time_sum = channel1plot.data["time"].sum()
        self.channel1_amplitude_sum = channel1plot.data["amplitude"].sum()
        self.channel2_time_sum = channel2plot.data["time"].sum()
        self.channel2_amplitude_sum = channel2plot.data["amplitude"].sum()
        self.time_mean1 = self.channel1_time_sum / len(channel1plot.data["time"])
        self.time_mean2 = self.channel1_time_sum / len(channel2plot.data["time"])
        self.amplitude_mean1 = self.channel1_amplitude_sum / len(
            channel1plot.data["amplitude"]
        )
        self.amplitude_mean2 = self.channel2_amplitude_sum / len(
            channel2plot.data["amplitude"]
        )
        self.max1 = channel1plot.data["time"].max()
        self.max2 = channel2plot.data["time"].max()
        self.min1 = channel1plot.data["time"].min()
        self.min2 = channel2plot.data["time"].min()

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
        else:
            self.ErrorMsg("No Chosen Color")

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
