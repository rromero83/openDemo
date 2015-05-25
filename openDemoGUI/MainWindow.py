# -*- coding: utf-8 -*-
'''
Created on May 2, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore, QtGui
#Import icones 
import icon_rc
#Imports openDemo
from ValuesWindow import ValuesWindow
from SettingsWindow import SettingsWindow
from HistoryWindow import HistoryWindow
from Database import Database

#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s   

#Classe de la Finestra Principal        
class MainWindow(QtGui.QMainWindow):
    
    #Funció que accedeix a la base de dades per obtenir el valor de consigna de temperatura
    def getTempConsigna(self,db):
        temp=0
        if db.connect():
            temp=db.getTemperaturaConsigna()  
        else:            
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades")       
        db.close()
        return temp 
    
    #Funció que actualitza en la base de dades el valor de consigna de temperatura
    def updateTemperaturaConsigna (self,db,temp):
        ok=False
        if db.connect():
            ok = db.updateTemperaturaConsigna(temp)
        else:
            QtGui.QMessageBox.warning(self,"Error","No es pot connectar amb la base de dades") 
        db.close()
        return ok
    
    #Funció que es crida en prémer el botó Pujar
    #Incrementar en un grau el valor de consigna de temperatura en la GUI i la base de dades
    def up_temp(self):
            self.tempConsigna=self.tempConsigna+1
            if self.updateTemperaturaConsigna (self.db,self.tempConsigna):
                self.lcdNumber.display(self.tempConsigna)
            else:
                self.tempConsigna=self.tempConsigna-1            
    
    #Funció que es crida en prémer el botó Baixar   
    #Disminuir en un grau el valor de consigna de temperatura en la GUI i la base de dades     
    def down_temp(self):
            self.tempConsigna=self.tempConsigna-1
            if self.updateTemperaturaConsigna (self.db,self.tempConsigna):
                self.lcdNumber.display(self.tempConsigna)
            else:
                self.tempConsigna=self.tempConsigna+1
    
    #Funció que es crida en prémer el botó Valors
    #Crear i obrir la Finestra Valors         
    def values_window(self):
        valuesWindow= ValuesWindow()
        valuesWindow.show()
        valuesWindow.exec_()
        
    #Funció que es crida en prémer el botó Configuració
    #Crear i obrir la Finestra Configuració           
    def settings_window(self):
        settingsWindow= SettingsWindow()
        settingsWindow.show()
        settingsWindow.exec_()
    
    #Funció que es crida en prémer el botó Històric
    #Crear i obrir la Finestra Històric             
    def history_window(self):
        historyWindow= HistoryWindow()
        historyWindow.show()
        historyWindow.exec_()
    
    #Constructor de la classe 
    #Inicialitzar GUI i les seves funcions 
    def __init__(self):        
        QtGui.QMainWindow.__init__(self)
        self.setupUI()
        self.db=Database()
        self.tempConsigna=self.getTempConsigna(self.db)        
        self.lcdNumber.display(self.tempConsigna)
        self.connect(self.pushButton_up, QtCore.SIGNAL('clicked()'), self.up_temp)
        self.connect(self.pushButton_down, QtCore.SIGNAL('clicked()'), self.down_temp)
        self.connect(self.pushButton_Settings, QtCore.SIGNAL('clicked()'), self.settings_window)
        self.connect(self.pushButton_History, QtCore.SIGNAL('clicked()'), self.history_window)
        self.connect(self.pushButton_Values, QtCore.SIGNAL('clicked()'), self.values_window)

    #Inicialització de la GUI 
    def setupUI(self):
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)         
        self.showFullScreen()
        self.main_Widget = QtGui.QWidget()
          
        self.verticalLayout = QtGui.QVBoxLayout(self.main_Widget)
                                       
        self.lcdNumber = QtGui.QLCDNumber(self.main_Widget)      
        self.lcdNumber.setNumDigits(2)                        
        palette=self.lcdNumber.palette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.red)        
        self.lcdNumber.setPalette(palette) 
               
        self.labelTemp = QtGui.QLabel(u"°C",self)
        font = QtGui.QFont("", 100, QtGui.QFont.Bold, False)
        self.labelTemp.setFont(font)
        self.labelTemp.setStyleSheet('color:red')
                
        self.pushButton_up = QtGui.QPushButton(self.main_Widget)        
        iconUp = QtGui.QIcon()      
        iconUp.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_up.setIcon(iconUp)
        self.pushButton_up.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_up.setFixedSize(QtCore.QSize(70, 70))
        
        self.pushButton_down = QtGui.QPushButton(self.main_Widget)        
        iconDown = QtGui.QIcon()
        iconDown.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/down.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_down.setIcon(iconDown)
        self.pushButton_down.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_down.setFixedSize(QtCore.QSize(70, 70))                     
       
        self.pushButton_Settings = QtGui.QPushButton(self.main_Widget)                
        iconSettings = QtGui.QIcon()
        iconSettings.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Settings.setIcon(iconSettings)
        self.pushButton_Settings.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Settings.setFixedSize(QtCore.QSize(70, 70))
                
        self.pushButton_History = QtGui.QPushButton(self.main_Widget)        
        iconHistory = QtGui.QIcon()
        iconHistory.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/line_chart_icon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_History.setIcon(iconHistory)
        self.pushButton_History.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_History.setFixedSize(QtCore.QSize(70, 70))
        
        self.pushButton_Values = QtGui.QPushButton(self.main_Widget)        
        iconValues = QtGui.QIcon()
        iconValues.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/temp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Values.setIcon(iconValues)
        self.pushButton_Values.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Values.setFixedSize(QtCore.QSize(70, 70))
                
        self.horizontalLayout_1 = QtGui.QHBoxLayout()         
        self.horizontalLayout_1.addWidget(self.lcdNumber)   
        self.horizontalLayout_1.addWidget(self.labelTemp)    
                
        self.verticalLayout_2 = QtGui.QVBoxLayout()   
        self.verticalLayout_2.addWidget(self.pushButton_up)
        self.verticalLayout_2.addWidget(self.pushButton_down)
        self.horizontalLayout_1.addLayout(self.verticalLayout_2)  
        
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.pushButton_Settings)
        self.horizontalLayout_2.addWidget(self.pushButton_History)
        self.horizontalLayout_2.addWidget(self.pushButton_Values)
        
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.setCentralWidget(self.main_Widget)