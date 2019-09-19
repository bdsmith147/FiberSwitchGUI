# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:48:18 2018

@author: Benjamin Smith
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
#from PyQt5.Core import Qt
import PyQt5.uic as uic

import serial
#from time import sleep

Ui_MainWindow, QtBaseClass = uic.loadUiType('switch_widget2.ui')

class SwitchController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SwitchController, self).__init__()
        self.setupUi(self)
        #print('start')
        
        self.setWindowTitle('Fiber Switch Controller')
        portnames = ['COM3', 'COM4', 'COM5', 'COM6', 'COM7']
        self.PortComboBox.insertItems(portnames)
        self.PortComboBox.setCurrentIndex(2) #for COM5
        self.PortComboBox.activated.connect(self.InitSerial)
        self.InitSerial()
        self.echoOn = False
        self.WriteSerial('echo')
        self.ConfigurePushButton.clicked.connect(self.set_channel)
        self.show()
        
    def InitSerial(self):
        try:
            self.ser = serial.Serial(
                    port = self.PortComboBox.currentText(),
                    baudrate = 115200,
                    timeout = 1,
                    bytesize = serial.EIGHTBITS,
                    stopbits = serial.STOPBITS_ONE
                    )
            self.currChannel = self.WriteSerial(c='get')
        except:
            print('Cannot connect with port ' + self.PortComboBox.currentText())
    
    def get_channel(self):
        cmd = b'I1?\r'
        self.ser.write(cmd)
        response = self.ser.read(100)
        print('Current Channel: ' + response)
        return response   


    def set_channel(self):
        chan = self.ChannelSpinBox.value()
        cmd = b'I1 ' + str(chan) + '\r'
        self.ser.write(cmd)
        print('Channel set to: ' + str(chan))
        
        self.CurrentChannelLabel.setText()
    
    
    def echo_toggle(self):
        self.echoOn = not self.echoOn
        cmd = b'EO ' + str(int(self.echoOn))
        
        self.ser.write(cmd)
        response = self.ser.read(100)
        print('Echo: ' + response)
        return response
    
 
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    switch = SwitchController()
    app.exec_()