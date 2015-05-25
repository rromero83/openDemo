# -*- encoding: utf-8 -*-
'''
Created on May 3, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore, QtGui
#Import icones 
import icon_rc
#Imports openDemo
from ValuesThread import ValuesThread
from Database import Database
import ConvertValue

#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#Classe de la Finestra Valors
class ValuesWindow(QtGui.QDialog):
    
    #Funció que es crida en prémer el botó Tornar
    #Tanca la finestra
    def back(self):
        self.close()
    
    
    def getValors(self):
        if not self.isCollect:        
            
            indexes = self.listView.selectionModel().selectedIndexes()
            if len(indexes)==0:
                QtGui.QMessageBox.information(None,u"Informació",u"Ha de seleccionar un element de la llista")
            else:
                ipv6=None
                for index in indexes: 
                    self.desMota= str(index.data().toString())
                    ipv6 = self.diccDescripIpv6.get(self.desMota)
                if ipv6 is not None:
                    self.progressBar.setValue(0)
                    self.isCollect=True
                    self.myLongTask = ValuesThread(ipv6)           
                    self.myLongTask.getValues.connect(self.getValues)
                    self.myLongTask.start()                    
                else:
                    QtGui.QMessageBox.warning(None,"Error","No es poden obtenir els valors") 
        else:
            QtGui.QMessageBox.warning(None,"Error","Ha d'esperar a finalitzar la captura de "+self.desMota) 
    
    #Funció per obtenir un diccionari descripció-ipv6 de cada mota   
    def getDiccDescriptionIpv6(self):
        diccio=None
        if self.db.connect():
            diccio=self.db.getDiccDescriptionIpv6() 
        else:          
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades")    
        self.db.close()
        return diccio
    
    #Funció per acutalitzar el valor de la barra de progrés     
    def onProgress(self):
        self.progressBar.setValue(self.progressBar.value()+1)
    
    #Constructor de la classe 
    #Inicialitzar GUI i les seves funcions  
    def __init__(self):        
        QtGui.QDialog.__init__(self)
        self.setupUI()
        self.progressBar.setRange(0,2)
        self.progressBar.setValue(0)
        self.db=Database()
        self.diccDescripIpv6=self.getDiccDescriptionIpv6()
        self.isCollect=False
        self.desMota=''
        if self.diccDescripIpv6 is not None:
            model = QtGui.QStandardItemModel(self.listView)
            fontText = QtGui.QFont()
            fontText.setPointSize(14)
            for des in self.diccDescripIpv6.keys():
                item=QtGui.QStandardItem(des)   
                item.setFont(fontText)                  
                model.appendRow(item)
            self.listView.setModel(model)            
        
        self.listView.setSelectionMode(QtGui.QListView.SingleSelection)                 
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)
        self.connect(self.pushButton_Values, QtCore.SIGNAL('clicked()'), self.getValors)
   
      
    #Funció que es crida per rebre "SIGNAL" de ValuesThread   
    #Converteix els valors rebuts per la mota en valors reals de temepratura i himitat i els mostra en la GUI      
    def getValues(self, codi,value):            
        if codi == 0:
            if value is not None:
                tempValue = ConvertValue.getTemperature(value) 
                self.lcdNumberTemp.display(tempValue)  
            else:
                QtGui.QMessageBox.warning(None,"Error","No es pot obtenir el valor de temperatura")
            self.onProgress() 
        elif codi == 1:   
            if value is not None:
                humValue=ConvertValue.getHumidity(value)  
                self.lcdNumberHum.display(humValue)
            else:
                QtGui.QMessageBox.warning(None,"Error",u"No es pot obtenir el valor d'humitat")
            self.onProgress() 
            self.isCollect=False           
        elif codi == 2:
            self.isCollect=False            
            self.progressBar.setValue(2)
            QtGui.QMessageBox.warning(None,"Error",u"No hi ha comunicació amb la mota ")  
            
            
    #Inicialització de la GUI 
    def setupUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)        
        self.showFullScreen()            
        self.verticalLayout = QtGui.QVBoxLayout(self)
                         
        self.listView = QtGui.QListView()   
        self.listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)   
        self.listView.setFixedSize(QtCore.QSize(200, 200))
        self.listView.setSpacing(5)
        
        self.lcdNumberTemp = QtGui.QLCDNumber(self)              
        self.lcdNumberTemp.setNumDigits(2) 
        self.lcdNumberTemp.display(0)
        self.lcdNumberTemp.setFixedWidth(50)
        palette=self.lcdNumberTemp.palette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.red)        
        self.lcdNumberTemp.setPalette(palette)
        
        self.labelTemp = QtGui.QLabel(u"°C",self)
        font = QtGui.QFont("", 48, QtGui.QFont.Bold, False)
        self.labelTemp.setFont(font)
        self.labelTemp.setStyleSheet('color:red')
        
        self.lcdNumberHum = QtGui.QLCDNumber(self)             
        self.lcdNumberHum.setNumDigits(2) 
        self.lcdNumberHum.display(0)
        self.lcdNumberHum.setFixedWidth(50)
        palette=self.lcdNumberHum.palette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.blue)        
        self.lcdNumberHum.setPalette(palette)
        
        self.labelHum = QtGui.QLabel("%",self)
        self.labelHum.setFont(font)
        self.labelHum.setStyleSheet('color:blue')                        
        
        self.progressBar = QtGui.QProgressBar(self)
        
        self.pushButton_Back = QtGui.QPushButton(self) 
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/back.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Back.setIcon(iconBack)
        self.pushButton_Back.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Back.setFixedSize(QtCore.QSize(70, 70))
        
        self.pushButton_Values = QtGui.QPushButton(self)        
        iconValues = QtGui.QIcon()
        iconValues.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/temp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Values.setIcon(iconValues)
        self.pushButton_Values.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Values.setFixedSize(QtCore.QSize(70, 70))
        
        self.horizontalLayout_2 = QtGui.QHBoxLayout()         
        self.horizontalLayout_2.addWidget(self.lcdNumberTemp)
        self.horizontalLayout_2.addWidget(self.labelTemp) 
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.addWidget(self.lcdNumberHum)
        self.horizontalLayout_3.addWidget(self.labelHum)
        
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        
        self.horizontalLayout = QtGui.QHBoxLayout() 
        self.horizontalLayout.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setAlignment(self.listView, QtCore.Qt.AlignLeft)
        self.horizontalLayout.setAlignment(self.verticalLayout_2, QtCore.Qt.AlignLeft)
        
        self.horizontalLayout_4 = QtGui.QHBoxLayout() 
        self.horizontalLayout_4.addWidget(self.pushButton_Back)        
        self.horizontalLayout_4.addWidget(self.pushButton_Values)
        
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_4)  
        self.verticalLayout.setAlignment(self.horizontalLayout_4, QtCore.Qt.AlignLeft)
        