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
from EditSettingsWindow import EditSettingsWindow
from Database import Database

#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#Classe de la Finestra COnfiguració
class SettingsWindow(QtGui.QDialog):    
    #Variable global
    listTipusMota=['Sensor','Actuador']
    
    #Funció que es crida en prémer el botó Tornar
    #Tanca la finestra
    def back(self):
        self.close()
    
    #Funció que es crida en prémer el botó Editar
    #Crear i mostrar la Finestra Editar Configuració   
    def edit(self):
        indexRow=self.tableView.selectionModel().currentIndex().row()
        if indexRow >=0:         
            idindex = self.dicIndexRowId.get(indexRow)
            if idindex is not None:
                editsettingsWindow= EditSettingsWindow(idindex)
                editsettingsWindow.update.connect(self.getModel)
                editsettingsWindow.show()
                editsettingsWindow.exec_()        
            else:
                QtGui.QMessageBox.warning(None,"Error",u"No es pot accedir a l'edició") 
        else:
            QtGui.QMessageBox.information(None,u"Informació",u"Ha de seleccionar un element de la llista")
     
    #Constructor de la classe 
    #Inicialitzar GUI i les seves funcions         
    def __init__(self):        
        QtGui.QDialog.__init__(self)
        self.setupUI()
        self.db=Database()
        self.model = QtGui.QStandardItemModel(self.tableView)                    
        self.tableView.setModel(self.model)  
        self.tableView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.getModel()        
        self.connect(self.pushButton_Update, QtCore.SIGNAL('clicked()'), self.getModel)
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)
        self.connect(self.pushButton_Edit, QtCore.SIGNAL('clicked()'), self.edit)
        
    #Funció que es crida en prémer el botó Actualitzar i per rebre "SIGNAL" de la Finestra Editar Configuració
    #Funció que accedeix a la base de dades per obtenir el model (dades) de la taula
    def getModel(self):
        self.model.clear()
        self.setHeaders()
        if self.db.connect():
            data = self.db.select("SELECT description,thingToken,type,id FROM motes")
            self.dicIndexRowId=dict()
            indexRow=0
            for d in data:
                row = []
                for x in range (0,4):            
                    valor=d[x]
                    if x == 2:
                        valor = self.listTipusMota[(int(valor))]
                    elif x==3:
                        self.dicIndexRowId[indexRow]=valor
                    else:
                        if valor is None:
                            valor=""     
                    if x !=3:                
                        item = QtGui.QStandardItem(str(valor))
                        item.setEditable(False)                
                        row.append(item)                            
                self.model.appendRow(row)
                indexRow=indexRow+1
        else:
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades")             
        self.db.close()
    
    #Funció per configurar les capçaleres de la taula    
    def setHeaders(self):
        headerNames = []
        headerNames.append(u"Descripció")       
        headerNames.append("Thing_Token")
        headerNames.append("Tipus")
        self.model.setHorizontalHeaderLabels(headerNames)
    
    #Inicialització de la GUI        
    def setupUI(self):
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.verticalLayout = QtGui.QVBoxLayout(self)
        
        self.pushButton_Update = QtGui.QPushButton(self) 
        iconUpdate = QtGui.QIcon()
        iconUpdate.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/update.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Update.setIcon(iconUpdate)
        self.pushButton_Update.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Update.setFixedSize(QtCore.QSize(70, 70)) 
              
        self.tableView = QtGui.QTableView(self)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.resizeColumnsToContents()
        self.tableView.setFixedWidth(305)
        
        self.pushButton_Back = QtGui.QPushButton(self) 
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/back.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Back.setIcon(iconBack)
        self.pushButton_Back.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Back.setFixedSize(QtCore.QSize(70, 70)) 
         
        self.pushButton_Edit = QtGui.QPushButton(self) 
        iconEdit = QtGui.QIcon()
        iconEdit.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Edit.setIcon(iconEdit)
        self.pushButton_Edit.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Edit.setFixedSize(QtCore.QSize(70, 70))
        
        self.horizontalLayout = QtGui.QHBoxLayout() 
        self.horizontalLayout.addWidget(self.pushButton_Back)        
        self.horizontalLayout.addWidget(self.pushButton_Edit)   
             
        self.verticalLayout.addWidget(self.pushButton_Update)
        self.verticalLayout.setAlignment(self.pushButton_Update, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setAlignment(self.horizontalLayout, QtCore.Qt.AlignLeft)
        