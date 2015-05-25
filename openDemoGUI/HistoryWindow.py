# -*- encoding: utf-8 -*-
'''
Created on May 5, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore, QtGui
#Import icones 
import icon_rc
#Imports openDemo
from GraphWindow import GraphWindow
from Database import Database
#Imports genèrics
from pytz import timezone
import datetime
#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    

#Classe de la Finestra Històric    
class HistoryWindow(QtGui.QDialog): 
    
    #Funció que es crida en prémer el botó Tornar
    #Tanca la finestra
    def back(self):
        self.close()
        
    #Funció que es crida en prémer el botó Gràfic
    #Obtenir els paràmetres necessaris per crear i obrir una Finestra Gràfic   
    def graph(self):        
        
        indexes = self.listView.selectionModel().selectedIndexes()
        if len(indexes)==0:
            QtGui.QMessageBox.information(None,u"Informació",u"Ha de seleccionar un element de la llista") 
        else:
            isCheckedTemp = self.checkBoxTemp.isChecked()
            isCheckedHum = self.checkBoxHum.isChecked()
            if isCheckedTemp or isCheckedHum:
                token=None
                for index in indexes:            
                    token= self.diccDescripToken.get(str(index.data().toString()))       
                if token is not None:
                    year=self.dateEdit.date().year()
                    month= self.dateEdit.date().month()                     
                    day= self.dateEdit.date().day()-1
                    tz=timezone('Europe/Madrid')    
                    hourUtcOffset=int(str(tz.utcoffset(datetime.datetime(year,month,day))).split(':')[0])
                    dayNext=self.checkDate(str(day+1))
                    month= self.checkDate(str(month))
                    day=self.checkDate(str(day))
                    min=str(24-hourUtcOffset)
                    graphWindow= GraphWindow(token, isCheckedTemp,isCheckedHum,str(year)+month+day+min+'0000' ,str(year)+month+dayNext+min+'0000',hourUtcOffset )
                    graphWindow.show()
                    graphWindow.exec_()
                else:
                    QtGui.QMessageBox.warning(None,"Error",u"No es pot mostrar el gràfic") 
            else:
                QtGui.QMessageBox.information(None,u"Informació",u"Ha de seleccionar Temperatura i/o Humitat")
    
    #Funció que verifica si ha d'afegir un zero davant 
    #@param: data: string amb el valor del mes o el dia            
    def checkDate(self,data):
        if len(data)==1:
            data='0'+data
        return data
     
    #Funció per obtenir un diccionari descripció-Thing_Token de cada mota              
    def getDiccDescriptionToken(self):
        diccio =None
        if self.db.connect():
            diccio=self.db.getDiccDescriptionToken()   
        else:
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades")  
        self.db.close()
        return diccio
    
    #Constructor de la classe 
    #Inicialitzar GUI i les seves funcions    
    def __init__(self):        
        QtGui.QDialog.__init__(self)       
        self.setupUI()
        self.db=Database()
        self.diccDescripToken=self.getDiccDescriptionToken()        
        if self.diccDescripToken is not None:
            model = QtGui.QStandardItemModel(self.listView)
            fontText = QtGui.QFont()
            fontText.setPointSize(14)
            for des in self.diccDescripToken.keys():
                item=QtGui.QStandardItem(des) 
                item.setFont(fontText)             
                model.appendRow(item)
            self.listView.setModel(model)            
        
        self.listView.setSelectionMode(QtGui.QListView.SingleSelection) 
         
        self.checkBoxTemp.setChecked(True)
        self.checkBoxHum.setChecked(True)   
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)
        self.connect(self.pushButton_Graph, QtCore.SIGNAL('clicked()'), self.graph)
        
    #Inicialització de la GUI      
    def setupUI(self):        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.horizontalLayout_2 = QtGui.QHBoxLayout() 
        
        self.listView = QtGui.QListView()   
        self.listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)   
        self.listView.setFixedSize(QtCore.QSize(200, 200))
        self.listView.setSpacing(5)        
                
        self.dateEdit = QtGui.QDateEdit(self)
        self.dateEdit.setCalendarPopup(True) 
        self.dateEdit.setDate(QtCore.QDate.currentDate())   
        self.dateEdit.calendarWidget().setFirstDayOfWeek(QtCore.Qt.Monday) 
        self.dateEdit.setDisplayFormat('dd/MM/yyyy')    
        self.dateEdit.calendarWidget().setLocale (QtCore.QLocale(QtCore.QLocale.Catalan)) 
        
        self.fontText = QtGui.QFont()
        self.fontText.setPointSize(14)
        
        self.checkBoxTemp = QtGui.QCheckBox('Temperatura', self)
        self.checkBoxTemp.setFont(self.fontText)
        
        self.checkBoxHum = QtGui.QCheckBox('Humitat', self)
        self.checkBoxHum.setFont(self.fontText)
        
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.addWidget(self.dateEdit)
        self.verticalLayout_2.addWidget(self.checkBoxTemp)
        self.verticalLayout_2.addWidget(self.checkBoxHum)
        
        self.horizontalLayout_2.addWidget(self.listView) 
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setAlignment(self.listView, QtCore.Qt.AlignLeft)
        self.horizontalLayout_2.setAlignment(self.verticalLayout_2, QtCore.Qt.AlignLeft)
        
        self.pushButton_Back = QtGui.QPushButton(self) 
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/back.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Back.setIcon(iconBack)
        self.pushButton_Back.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Back.setFixedSize(QtCore.QSize(70, 70))
          
        self.pushButton_Graph = QtGui.QPushButton(self) 
        iconGraph = QtGui.QIcon()
        iconGraph.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/line_chart_icon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Graph.setIcon(iconGraph)
        self.pushButton_Graph.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Graph.setFixedSize(QtCore.QSize(70, 70))
        
        self.horizontalLayout = QtGui.QHBoxLayout() 
        self.horizontalLayout.addWidget(self.pushButton_Back)        
        self.horizontalLayout.addWidget(self.pushButton_Graph)
                
        self.verticalLayout.addLayout(self.horizontalLayout_2)         
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.verticalLayout.setAlignment(self.horizontalLayout, QtCore.Qt.AlignLeft)
        