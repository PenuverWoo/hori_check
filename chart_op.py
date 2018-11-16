import datetime
import threading

import matplotlib
import matplotlib.animation as animation
# Make sure that we are using QT5
#matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
import sys
import logging
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2
from usb_hid_test import hidHelper
#pl.mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
#import test5

X = [1, 2, 3, 4, 5, 6]
Y = [5,2,0,5,2,0]

class ShowWindow(QWidget):
    def __init__(self):
        super(ShowWindow, self).__init__()
        self.initUI()
        self.usb_dev = None
        self.usb_receive_count = 0
        self.temp_list = []
        self.dym_data = None
        self.xdata,self.ydata = [],[]

    def initUI(self):

        self.setWindowTitle('Chart')
        self.inputLabel = QLabel("请输入文件路径:")
        self.editLine = QLineEdit()
        self.selectButton = QPushButton("...")

        self.selectButton.clicked.connect(self.selectFile)

        grid = QGridLayout()
        grid.setSpacing(10)

        # a figure instance to plot on
        self.figure = plt.figure()  # - - - - - - PlT FIGURE - - - - - - -
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas,0,0,4,3)


        self.button = QPushButton('Plot') # - - - - draw FIGURE button - - - - -
        self.button.clicked.connect(self.animation)
        grid.addWidget(self.button,0,3)


        self.log = QListWidget(self) # - - - - - - Made list View - - - - - - -
        grid.addWidget(self.log, 5,0,3,3)

        start_hid = QPushButton('start_hid')# - - - - - - hid start receive data
        start_hid.clicked.connect(self.hid_start)
        grid.addWidget(start_hid, 1,3)

        stop_hid = QPushButton('stop_hid')  # - - - - - - hid start receive data
        stop_hid.clicked.connect(self.usb_on_data_received_stop)
        grid.addWidget(stop_hid, 2, 3)


        self.plotLayout = QVBoxLayout()  # 垂直
        inputLayout = QHBoxLayout()  # 水平

        self.setLayout(grid)
        self.show()

    # 选择图形数据文件存放地址
    def selectFile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(fileName1, filetype)
        self.editLine.setText(fileName1)

    # 画图
    def animation(self):
        global Y
        self.ax1 = self.figure.add_subplot(111)
        #self.line, = self.ax1.plot([],[],lw=2)
        self.ax1.clear()
        self.ax1.plot(Y,X)
        Y.append(1)
        self.canvas.draw()
        #plt.show()
        #self.sss = dyna_img()
        #self.sss.ss()
        #ani = animation.FuncAnimation(self.figure,self.update,self.data_gen,interval=100)
        #plt.show()


    def data_gen(self):
        while True:
            yield np.random.rand(10)
        print('ge')

    def updata(self,data):
        self.line.set_data(data)
        print('up')
        return self.line,

    def plotText(self):
        #global Y
        ##for i in range(len(X)):
        #    Y.append(i+1)
        #input_file = self.editLine.text()
        # input_file = r'E:\pyqt\1.txt'

        Ax = self.figure.add_subplot(111)  # Create a `axes' instance in the figure
        Ax.clear()
        Ax.set_ylabel('High')
        Ax.set_xlabel('Time')
        Ax.plot(Y, X)
        self.canvas.draw()

    def hid_start(self):

        self.usb_dev = hidHelper()
        self.usb_dev.start()
        if self.usb_dev.device:
            self.usb_dev.device.set_raw_data_handler(self.usb_on_data_received)

    def usb_on_data_received(self,data):
        try:
            self.temp_list = data[1:]
            self.usb_receive_count += 1
            #logging.info("<<<[" + str(self.usb_receive_count) + "]" + " ".join([hex(x)[3:].rjust(2, "0").upper() for x in temp_list]))
            self.log.addItem("<<<[" + str(self.usb_receive_count) + "]" + " "+
                str(self.temp_list))
            self.log.scrollToBottom()
            self.dym_data = self.temp_list[3]


        except Exception as e:
            logging.error(e)

    def usb_on_data_received_stop(self):
        try:
            self.usb_dev.stop()

        except BaseException as e:
            self.log.addItem('fail to turn off!!')

    def run(self,data):
        t, y = data

        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()

        if t >= xmax:
            self.ax.set_xlim(xmin, 2 * xmax)
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)

        return self.line,

    def update(self,data):
        self.line.set_ydata(data)
        return self.line,



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShowWindow()
    sys.exit(app.exec_())

if cv2.waitKey() == 27:
    exit()