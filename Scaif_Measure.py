''
import csv
import time
import sys
import json
import matplotlib
import numpy as np
import logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, Qt

import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, savefig

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
from matplotlib.ticker import MultipleLocator
from usb_hid_test import hidHelper
import threading
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import  scaif_data_sys as sds
n = 0
x, y, x1, y1 = [], [], [], []
x2 = 0
x22 = 0
y2 = [-200, 300]
t = []
data_path = '../hori_check/img_data/img_data.csv'


class App( QMainWindow, ):
    def __init__(self):
        QWidget.__init__( self )

        self.usb_dev = hidHelper()
        self.usb_receive_count = 0
        self.usb_receive_count_x = 0
        self.order_lines = 0
        self.reverse_x = False
        self.seeking_times = 0
        self.hid_switch = True
        self.record_first = True
        self.turn_off = True
        self.thread_switch = True
        self.first_Line_Location = [0, 0, 0, 0]
        self.second_Line_Location = [0, 0, 0, 0]

        startAction = QAction( QIcon( 'fire1.png' ), '&starting', self )
        startAction.setShortcut( 'Alt+Q' )
        startAction.setStatusTip( 'Starting' )
        startAction.triggered.connect( self.on_start )
        quitAction = QAction( QIcon( 'quit.png' ), '&quit', self )
        quitAction.setShortcut( 'Alt+W' )
        quitAction.setStatusTip( 'quit' )
        quitAction.triggered.connect( quit )
        stopAction = QAction( QIcon( 'stop_b.png' ), '&stop', self )
        stopAction.setShortcut( 'Alt+E' )
        stopAction.setStatusTip( 'stop' )
        stopAction.triggered.connect( self.on_stop )
        blue_R_dropLineAction = QAction( QIcon( 'blue_arrow_right.png' ), '&move line', self )
        blue_R_dropLineAction.setShortcut( '2' )
        blue_R_dropLineAction.setStatusTip( 'move drop line' )
        blue_R_dropLineAction.triggered.connect( self.first_Line_Rmove )
        blue_L_dropLineAction = QAction( QIcon( 'blue_arrow_left.png' ), '&move line', self )
        blue_L_dropLineAction.setShortcut( '1' )
        blue_L_dropLineAction.setStatusTip( 'move drop line' )
        blue_L_dropLineAction.triggered.connect( self.first_Line_Lmove )
        black_R_dropLineAction = QAction( QIcon( 'black_arrow_right.png' ), '&move line', self )
        black_R_dropLineAction.setShortcut( '4' )
        black_R_dropLineAction.setStatusTip( 'move drop line' )
        black_R_dropLineAction.triggered.connect( self.second_Line_Rmove )
        black_L_dropLineAction = QAction( QIcon( 'black_arrow_left.png' ), '&move line', self )
        black_L_dropLineAction.setShortcut( '3' )
        black_L_dropLineAction.setStatusTip( 'move drop line' )
        black_L_dropLineAction.triggered.connect( self.second_Line_Lmove )
        saveLineAction = QAction( QIcon( 'saving_img.png' ), '&Save', self )
        saveLineAction.setShortcut( 'Alt+S' )
        saveLineAction.setStatusTip( 'Saving' )
        saveLineAction.triggered.connect( self.input_save_dialog)

        self.toolbar = self.addToolBar( 'toolMenu' )

        self.toolbar.addAction( saveLineAction )
        self.toolbar.addAction( startAction )
        self.toolbar.addAction( stopAction )
        self.toolbar.addAction( blue_L_dropLineAction )
        self.toolbar.addAction( blue_R_dropLineAction )
        self.toolbar.addAction( black_L_dropLineAction )
        self.toolbar.addAction( black_R_dropLineAction )
        self.toolbar.addAction( quitAction )  # ------------------------- tool bar ------

        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        self.setWindowTitle( 'Scaif Measure' )
        self.main_widget = QWidget( self )
        self.setGeometry( 0, 0, 980, 480 )

        hBox = QHBoxLayout( self.main_widget )  # 横着布局 --------------------- layout -------
        vBox = QVBoxLayout( self.main_widget )  # 竖着布局
        vBox_1 = QVBoxLayout( self.main_widget )

        self.grid_Option = QGroupBox( 'Option' )
        self.grid_Option.setMaximumSize( 150, 1080 )
        self.grid_Graph = QGroupBox( 'Graph' )
        # self.grid_Graph.setLayout(hBox)

        # self.linEdit = QLineEdit('100', self)

        self.f_Loc = QLabel( '  first_Line: ' )  # - --------------  Option label -------
        self.f_Loc_ = QLineEdit( 'f', self )
        self.s_Loc = QLabel( '  second_Line: ' )
        self.s_Loc_ = QLineEdit( 's', self )

        self.first_Loc_L = QLabel( '1' )
        self.first_lSlop = QLabel( '2' )
        self.second_Loc_L = QLabel( '3' )
        self.second_lSlop = QLabel( '4' )
        self.first_Loc_R = QLabel( '5' )
        self.second_Loc_R = QLabel( '6' )

        self.hid_button = QPushButton( 'run_hid', self )
        self.clear_button = QPushButton( 'clear', self )
        self.hid_button.clicked.connect( self.start_thread )
        self.clear_button.clicked.connect( self.input_save_dialog )
        vBox.addWidget( self.hid_button )
        vBox.addWidget( self.clear_button )
        vBox.addStretch( 1 )
        vBox.addWidget( self.f_Loc )
        vBox.addWidget( self.f_Loc_ )
        vBox.addWidget( self.first_Loc_L )
        vBox.addWidget( self.first_Loc_R )
        vBox.addWidget( self.first_lSlop )
        vBox.addWidget( self.s_Loc )
        vBox.addWidget( self.s_Loc_ )
        vBox.addWidget( self.second_Loc_L )
        vBox.addWidget( self.second_Loc_R )
        vBox.addWidget( self.second_lSlop )
        vBox.addStretch( 3 )

        self.canvas = figure_Plot( self.main_widget, width=5, height=4, dpi=100 )  # --- press action
        self.canvas.mpl_connect( 'button_release_event', self.OnClick_release )  # --- canvas
        self.canvas.mpl_connect( 'button_press_event', self.OnClick_press )
        vBox_1.addWidget( self.canvas )

        self.grid_Option.setLayout( vBox )
        self.grid_Graph.setLayout( vBox_1 )

        hBox.addWidget( self.grid_Option )
        hBox.addWidget( self.grid_Graph )
        # hBox.addLayout(vBox)
        self.setLayout( hBox )
        self.main_widget.setFocus()
        self.setCentralWidget( self.main_widget )

        self.scat, = self.canvas.ax.plot( [], [], color = 'green', label = 'trasdsad' , lw=1 )
        self.scat1, = self.canvas.ax.plot( [], [], lw=1 )
        self.scat2, = self.canvas.ax.plot( [], [], lw=1 )
        self.scat3, = self.canvas.ax.plot( [], [], lw=1 )
        #plt.legend()
        self.show()


    def update_function(self, i):  # --  ------------------  updating scat --
        global x, y, x1, y1, y2, x22
        if self.turn_off == False:
            self.scat.set_data( x, y )
            self.scat1.set_data( x1, y1 )
            self.scat2.set_data( x2, y2 )
            self.scat3.set_data( x22, y2 )
            self.scat2.set_color( 'black' )
            self.scat3.set_color( 'black' )
        #   self.label.setText('<h1>sdsd</h1>')

        # self.plt.axvline(100)
        # self.scat.xlabel('x')
        return self.scat, self.scat1, self.scat2, self.scat3,

    def start_thread(self):
        t = threading.Thread( target=self.run_Hid )
        t.setDaemon( True )
        t.start()

    def on_start(self):  # ----------------------------- start loading ----
        self.turn_off = False
        # if self.turn_off == True:
        self.hid_switch == False
        self.start_thread()
        if self.hid_switch == True:
            self.ani = animation.FuncAnimation( self.canvas.figure, self.update_function, frames=200,
                                                blit=True, interval=10 )

    def on_stop(self):
        try:
            self.usb_dev.stop()
            self.turn_off = True
            self.hid_switch = False# self.ani._stop()
        except BaseException as e:
            print( 'error' )

    def clear_Data(self):
        global x, y, x1, y1
        # self.usb_dev.stop()
        self.saveas( self.scat, 'kk.jpg' )
        # self.turn_off = True
        # self.hid_switch = False
        # x, y, x1, y1 = [],[],[],[]
        # self.usb_receive_count_x = 0
        # self.usb_receive_count = 0

    def shifting_Raster(self):
        print( 'staring first rastere' )

    def run_Hid(self):  # --------------------- running hid to catch the data from device
        self.usb_dev.start()
        if self.usb_dev.device:
            self.usb_dev.device.set_raw_data_handler( self.usb_on_data_received )

    def usb_on_data_received(self, data):  # --------------- return the data form device
        try:
            if self.turn_off == False:
                global x, y, x1, y1
                # with open('data1.txt','a') as f:
                #        f.write(str(x)+ str(y) +str(x1)+ str(y1)  + '\n')

                if self.order_lines == 0:  # ---------- first time line loading
                    if self.record_first == True:
                        y.append( data[3] )
                        x.append( self.usb_receive_count_x )
                    else:
                        y[self.usb_receive_count_x] = data[3]
                        x[self.usb_receive_count_x] = self.usb_receive_count_x
                        self.record_first = False
                    self.usb_receive_count_x += 1  # ------------- counting y value amount per time
                    self.usb_receive_count += 1
                    if self.usb_receive_count_x >= 200:  # --------- per time loading 200 y values
                        self.order_lines = 1

                if self.order_lines == 1:  # ------------ second time line loading
                    if self.record_first == True:
                        y1.append( data[3] )
                        x1.append( self.usb_receive_count_x )
                    else:
                        y1[self.usb_receive_count_x - 1] = data[3]
                        x1[self.usb_receive_count_x - 1] = self.usb_receive_count_x
                        self.record_first = False
                    self.usb_receive_count -= 1
                    self.usb_receive_count_x -= 1
                    if self.usb_receive_count_x <= 0:
                        self.order_lines = 0
                        self.record_first = False
        except Exception as e:
            logging.error( e )
            print( '----- y1' )
            print( y1 )
            print( '-- -- y' )
            # print(len(x))
            print( y )

    def second_Line_Rmove(self):
        try:
            global x22
            if x22 < 200 or x22 >= 0:
                x22 += 1
            self.scat2.set_data( x22, y2 )
            self.first_Loc_R.setText( 'F_Line_R: ' + '(' + str( x22 ) + ', ' + str( y[x22] ) + ')' )
            self.first_Line_Location[2] = x22
            self.first_Line_Location[3] = y[x22]
            self.second_Loc_R.setText( 'S_Line_R: ' + '(' + str( x22 ) + ', ' + str( y1[x22] ) + ')' )
            self.second_Line_Location[2] = x22
            self.second_Line_Location[3] = y1[x22]

            self.count_Slop()
            print( x2 )
        except BaseException as e:
            print( 'Second Line move problem! ' )

    def second_Line_Lmove(self):
        try:
            global x22
            if x22 < 200 or x22 >= 0:
                x22 -= 1
            self.scat2.set_data( x22, y2 )
            self.first_Loc_R.setText( 'F_Line_R: ' + '(' + str( x22 ) + ', ' + str( y[x22] ) + ')' )
            self.first_Line_Location[2] = x22
            self.first_Line_Location[3] = y[x22]
            self.second_Loc_R.setText( 'S_Line_R: ' + '(' + str( x22 ) + ', ' + str( y1[x22] ) + ')' )
            self.second_Line_Location[2] = x22
            self.second_Line_Location[3] = y1[x22]
            print( x2 )

            self.count_Slop()
        except BaseException as e:
            print( 'Second Line move problem! ' )

    def first_Line_Lmove(self):
        try:
            global x2
            if x2 < 200 or x2 >= 0:
                x2 -= 1
            self.scat2.set_data( x2, y2 )
            self.first_Loc_L.setText( 'F_Line_L: ' + '(' + str( x2 ) + ', ' + str( y[x2] ) + ')' )
            self.first_Line_Location[0] = x2
            self.first_Line_Location[1] = y[x2]
            self.second_Loc_L.setText( 'S_Line_L: ' + '(' + str( x2 ) + ', ' + str( y1[x2] ) + ')' )
            self.second_Line_Location[0] = x2
            self.second_Line_Location[1] = y1[x2]

            self.count_Slop()
            print( x2 )
        except BaseException as e:
            print( 'First Line move problem! ' )
        # if x2 >=200 or x2<0 :
        # x2-=2

    def first_Line_Rmove(self):
        try:
            global x2
            if x2 < 200 or x2 >= 0:
                x2 += 1
            self.scat2.set_data( x2, y2 )
            self.first_Loc_L.setText( 'F_Line_L: ' + '(' + str( x2 ) + ', ' + str( y[x2] ) + ')' )
            self.first_Line_Location[0] = x2
            self.first_Line_Location[1] = y[x2]
            self.second_Loc_L.setText( 'S_Line_L: ' + '(' + str( x2 ) + ', ' + str( y1[x2] ) + ')' )
            self.second_Line_Location[0] = x2
            self.second_Line_Location[1] = y1[x2]
            self.count_Slop()
            print( x2 )
        except BaseException as e:
            print( 'First Line move problem! ' )

    def input_save_dialog(self):
        try:
            global x
            value, ok = QInputDialog.getText( self, 'input', 'plz input: ', QLineEdit.Normal, 'default' )

            if ok:
                with open( data_path , 'a' , newline = '') as f:
                    writer = csv.writer( f,dialect = 'excel')
                    #data = ('Machine_num','time','x','y','x1','y1')
                    data = (value, time.asctime( time.localtime(time.time())) , x, y, x1 , y1 )
                    #data = [value, str(time.asctime( time.localtime(time.time()) )) , str(x) , str(y) , str(x1) , str(y1)]

                    writer.writerow(data)
                    #f.write( '\n' + str( x ) )
                self.s_Loc_.setText( 'save success' )

        except BaseException as e:
            print( 'errot on inpout dialog. ' )

    def Saving_data(self):
        global x, y, x1, y1
        print( y )
        print( y1 )
        #sds.compare_img.__init__()

    def closeEvent(self, event):
        reply = QMessageBox.question( self, 'Exit', 'Are you sure to exit?', QMessageBox.Yes | QMessageBox.Cancel )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_exit(self):  # ------------------------ close window
        self.close()

    def hid_Control_moving(self):
        send_list = [0x00 for i in range( 17 )]
        self.usb_dev.write( send_list )
        print( 'Processing data to control measure machine.' )

    def OnClick_press(self, event):  # -------------------------------- the event the mouse pressed inside the canvas
        try:
            # if self.turn_off:
            global y, x2, y1
            x2 = int( event.xdata )
            self.scat2.set_data( x2, y2 )
            print( y[x2] )
            self.first_Loc_L.setText('F_Line_L: ' + '(' + str( x2 ) + ', ' + str( y[x2] ) + ')' )
            self.first_Line_Location[0] = x2
            self.first_Line_Location[1] = y[x2]
            self.second_Loc_L.setText('S_Line_L: ' + '(' + str( x2 ) + ', ' + str( y1[x2] ) + ')' )
            self.second_Line_Location[0] = x2
            self.second_Line_Location[1] = y1[x2]
        except BaseException as e:
            print( e )
            print( 'error on press!' )

    def OnClick_release(self, event):  # -------------------------- the event the mouse releaseed inside the canvas
        try:
            # if self.turn_off:
            global x22, y, y1
            x22 = int( event.xdata )
            self.scat3.set_data( x22, y2 )
            self.first_Loc_R.setText('F_Line_R: ' + '(' + str( x22 ) + ', ' + str( y[x22] ) + ')' )
            self.first_Line_Location[2] = x22
            self.first_Line_Location[3] = y[x22]
            self.second_Loc_R.setText('S_Line_R: ' + '(' + str( x22 ) + ', ' + str( y1[x22] ) + ')' )
            self.second_Line_Location[2] = x22
            self.second_Line_Location[3] = y1[x22]
            self.count_Slop()
            print( self.second_Loc_L.text() )
            print( self.first_Line_Location )
            print( self.second_Line_Location )
        except BaseException as e:
            print( 'Error on release!' )
            print( self.first_Line_Location )
            print( self.second_Line_Location )

    def count_Slop(self):
        try:
            a = abs( (self.first_Line_Location[3] - self.first_Line_Location[1]) / (
                        self.first_Line_Location[2] - self.first_Line_Location[0]) )
            self.first_lSlop.setText( 'Slop: ' + str( round( a, 4 ) ) )
            b = (self.second_Line_Location[3] - self.second_Line_Location[1]) / (
                    self.second_Line_Location[2] - self.second_Line_Location[0])
            self.second_lSlop.setText( 'Slop: ' + str( round( b, 4 ) ) )
        except BaseException as e:
            print('Count slop error!!')



class figure_Plot( FigureCanvas ):
    def __init__(self, parent=None, width=20, height=16, dpi=100):
        fig = Figure( figsize=(width, height), dpi=dpi )
        self.ax = fig.add_subplot( 111 )
        self.ax.set_xlim( 0, 200 )
        self.ax.set_ylim( -100, 300 )
        self.xmajorLocator = MultipleLocator( 10 );
        self.ymajorLocator = MultipleLocator( 50 );
        self.ax.xaxis.set_major_locator( self.xmajorLocator )
        self.ax.yaxis.set_major_locator( self.ymajorLocator )
        # self.ax.sa

        self.ax.grid( True )

        FigureCanvas.__init__( self, fig )
        self.setParent( parent )
        # fig.canvas.mpl_connect('button_press_event',self.OnClick_press)
        # fig.canvas.mpl_connect('button_release_event', self.OnClick_release)
        FigureCanvas.setSizePolicy( self,
                                    QSizePolicy.Expanding,
                                    QSizePolicy.Expanding )
        FigureCanvas.updateGeometry( self )

    # def OnClick_press(self, event):
    # global x2
    # x2 = int(event.xdata)
    # App.self.scat2.set_data(x2, y2)
    # print(int(event.xdata))

    # def OnClick_release(self, event):
    # global x22
    # x22 = int(event.xdata)
    # App.self.scat3.set_data(x22,y2)

    # print(int(event.xdata))


if __name__ == '__main__':
    app = QApplication( sys.argv )
    ex = App()
    sys.exit( app.exec_() )

'''
            if self.usb_receive_count < 120:
                y.append(data1)
                x.append(self.usb_receive_count_x)
                self.usb_receive_count_x += 1
                #print(str(self.usb_receive_count_x), '-----', str(len(y)))
            #elif self.usb_receive_count == 120:
            #    x1, y1 = [],[]
            #    print(self.usb_receive_count_x)
            elif self.usb_receive_count>120 and self.usb_receive_count<=240:
                y1.append(data1)
                x1.append(self.usb_receive_count_x)
                self.usb_receive_count_x -= 1
                #print(str(self.usb_receive_count_x), '-----', str(len(y1)))
            #elif self.usb_receive_count == 240:
            #    x2, y2 = [], []
             #   print(self.usb_receive_count_x)
            elif self.usb_receive_count>240 and self.usb_receive_count<=360:
                y2.append(data1)
                x2.append(self.usb_receive_count_x)
                self.usb_receive_count_x += 1
                #print(str(self.usb_receive_count_x) , '-----' ,str(len(y2)))
            #elif self.usb_receive_count == 360:
            #    x3, y3 = [], []
            #    print(self.usb_receive_count_x)
            elif self.usb_receive_count>=360 and self.usb_receive_count<=480:
                y3.append(data1)
                x3.append(self.usb_receive_count_x)
                self.usb_receive_count_x -= 1
                #print(str(self.usb_receive_count_x), '-----', str(len(y3)))
            #elif self.usb_receive_count == 480:
            #   x, y = [], []
            #    print(self.usb_receive_count_x)
            elif self.usb_receive_count == 481:
                self.usb_receive_count = 0
                print(self.usb_receive_count_x)
            self.usb_receive_count +=1
            #temp_list = data[3]
            #print(data)
            #logging.info("<<<[" + str(self.usb_receive_count) + "]" + " ".join([hex(x)[3:].rjust(2, "0").upper() for x in temp_list]))
            #self.log.addItem("<<<[" + str(self.usb_receive_count) + "]" + " " +
            #                 str(self.temp_list))
            #self.log.scrollToBottom()
            #self.dym_data = self.temp_list[3]
            '''
