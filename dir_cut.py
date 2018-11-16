from PIL import ImageGrab
from PIL import Image
import pytesseract as pyt
import time
import matplotlib.pyplot as plt
import cv2
from PyQt5.QtWidgets import *
import threading
import os
import pyautogui as pyg
import numpy as np
from queue import Queue
import pyqtgraph as pg

import sys
dic_target_data = []
text = ''
c = 0
path = '../hori_check/'
time_switch = True
analysis_switch = True
queue = Queue()
list_data = []

class App(QDialog, QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("project")
        self.setGeometry(300,100,2000,400)

        grid = QGridLayout()
        grid.setSpacing(14)


        self.listwidght = QListWidget(self)
        grid.addWidget(self.listwidght,6,0,6,2)

        self.log_data = QListWidget(self)
        grid.addWidget(self.log_data, 6, 3, 6, 4)



        search_data = QLabel('search_data')#------------------- search data --------------------
        self.search_data_value = QLineEdit(self)

        grid.addWidget(search_data, 1, 0)
        grid.addWidget(self.search_data_value, 1, 1)

        num_need = QLabel('num_need')  # ------------------- search data _num_need --------------------
        self.num_need_value = QLineEdit(self)

        grid.addWidget(num_need, 1, 2)
        grid.addWidget(self.num_need_value, 1, 3)


        search_data_button  = QPushButton('search',self)# ----------- search data button ----------
        search_data_button.setCheckable(True)
        search_data_button.clicked.connect(self.search)

        grid.addWidget(search_data_button, 1, 5)

        Location = QLabel('Location')#------------------ Location -------------
        self.Location1 = QLineEdit()
        self.Location2 = QLineEdit()
        self.Location3 = QLineEdit()
        self.Location4 = QLineEdit()

        grid.addWidget(Location, 2, 0)
        grid.addWidget(self.Location1, 2, 1)
        grid.addWidget(self.Location2, 2, 2)
        grid.addWidget(self.Location3, 2, 3)
        grid.addWidget(self.Location4, 2, 4)

        start_locate = QPushButton('start_locate',self)# ----------- location button ----------
        start_locate.clicked.connect(self.location)
        grid.addWidget(start_locate,2,5)

        analysis_button = QPushButton('start_analysis', self)  # ----------- analysis button ----------
        analysis_button.clicked.connect(self.analysis_threading)
        grid.addWidget(analysis_button, 4, 0)

        stop_analysis_button = QPushButton('stop_analysis', self)  # ----------- Stop analysis button ----------
        stop_analysis_button.clicked.connect(self.stop_analysis)
        grid.addWidget(stop_analysis_button, 4, 1)

        #convert_bt = QPushButton('convert_16', self)  # ----------- convert 16 to 10 system ----------
        #convert_bt.clicked.connect(self.convert_decimal)
        #grid.addWidget(convert_bt, 4, 4)

        first_position_button = QPushButton('first_position', self)  # ----------- first position_button ----------
        first_position_button.clicked.connect(self.get_first_position)
        grid.addWidget(first_position_button, 3, 1)

        sec_position_button = QPushButton('sec_position', self)  # ----------- sec position_button ----------
        sec_position_button.clicked.connect(self.get_sec_position)
        grid.addWidget(sec_position_button, 3, 3)

        time_switch_off_button = QPushButton('stop_locate', self)  # ----------- time_loop off button ----------
        time_switch_off_button.clicked.connect(self.time_switch_off)
        grid.addWidget(time_switch_off_button,3,5)

        made_plot = QPushButton('Plot', self)  # --------- made plot button ----------
        made_plot.clicked.connect(self.made_PLOT)
        grid.addWidget(made_plot, 4, 5)

        reset_app = QPushButton('Reset', self)  # ----------- restart app button ----------
        reset_app.clicked.connect(self.reset_APP)

        self.setLayout(grid)
        self.show()


    def location(self): # -------------------------- locate target , built a sub thread
        #print(self.Location1.text())
        global time_switch
        time_switch = True
        t = threading.Thread(target=self.catch_loop)
        t.setDaemon(True)
        t.start()


    def search(self):
        print('lalala')

    def catch_loop(self):   # -------------------------- looping catch image

        while time_switch:
            self.catch()
            print('current{}'.format(threading.active_count()))
            time.sleep(1)


    def time_switch_off(self): #------------------- control loading image on/off
        global time_switch
        if time_switch is True:
            time_switch = False
        else:
            time_switch = True
    def catch(self):
        global c
        l1 = int(self.Location1.text())
        l2 = int(self.Location2.text())
        l3 = int(self.Location3.text())
        l4 = int(self.Location4.text())
        size = (l1,l2,l3,l4)
        im = ImageGrab.grab(size)
        im.save(path + str(c) + '.png', 'PNG', quality=100)
        # im.save('C:/Users/Shaoyu Hu/Desktop/hori_check' + str(c) + '.jpg', 'JPEG')

        self.log_data.addItem('successful catch ' + str(c) + ' image')

        self.listwidght.scrollToBottom()
        self.log_data.scrollToBottom()
        c = c+1

    # I:\hori_check

    def analysis(self):
        global text
        global analysis_switch
        global list_data
        analysis_switch = True
        for filename in os.listdir(path):
            self.log_data.addItem('Analysis switch is: ' + str(analysis_switch))
            if analysis_switch is False:
                break
            if filename.endswith('png'):
                    self.log_data.addItem('Successful generate: '+filename)
                    ana = Image.open('wechat_data1.jpg')
                    text = pyt.image_to_string(ana, lang='eng')
                    text = text.replace(" ", "")
                    text = text.replace("\n", "")
                    self.log_data.addItem(text)
                    self.listwidght.addItem(text[0:10])
                    list_data.append(text[0:5])
                    self.listwidght.scrollToBottom()
                    self.log_data.scrollToBottom()


        # for i in range(len(text)):
        #   print (text[i]+'__'+'/n')

    def analysis_threading(self):
            t = threading.Thread(target=self.analysis)
            t.setDaemon(True)
            t.start()

    def stop_analysis(self):
        global analysis_switch
        analysis_switch = False

    def serch_data(self, data, num_need):
        data = self.search_data_value.text()
        num_need = self.num_need_value.text()
        global text
        result = text.index(data)
        print(result)
        if text is None:
            print('without this data!!!')
        else:
            result = result + len(data)
            result1 = result + num_need
            print(text[result:result1])

    def save_file(filename, contents):
        fh = open(filename, 'w')
        fh.write(contents)
        fh.close()
        fh.save('filename', 'somestuff')

        #I:\hori_check
    def get_first_position(self):
        time.sleep(2)
        x, y = pyg.position()
        self.log_data.addItem('Generate position: ' + str(x) + ',' + str(y))
        self.Location1.setText(str(x))
        self.Location2.setText(str(y))

    def get_sec_position(self):
        time.sleep(2)
        x, y = pyg.position()
        self.log_data.addItem('Generate position: ' + str(x) + ',' + str(y))
        self.Location3.setText(str(x))
        self.Location4.setText(str(y))

    def reset_APP(self):
        global time_switch
        time_switch = True
        rese = sys.executable
        os.execl(rese,rese,*sys.argv)

    def made_PLOT(self):
        try:
            print(list_data)
            x = np.linspace(0, c)
            y = 2*x +1
            plt.plot(x,y)
            plt.show()
        except BaseException as e:
            self.log_data.addItem('Fail to print plot, it is not a num.')

    def convert_decimal(self):
        global list_data
        try:
            for i in range(len(list_data)):
                list_data[i] = int(list_data[i],16)
        except  BaseException as e:
            print('ERROR DATA!!')








if __name__ =='__main__':
    #while c<3:
    #    schedule.run_pending()
    #    c = c+1
    #    time.sleep(1)
    #else:
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())
        #print('done')
        #analysis()
        #rint(text)
        #print('-------------------------------------------------------==')
        #serch_data('save',4)
        #exit()
if cv2.waitKey() == 27:
    exit()
