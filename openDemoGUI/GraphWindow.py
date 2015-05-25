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
from Configthethingsio import Configthethingsio
import GraphCanvas as GraphCanvas
from PlotThread import PlotThread

#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
#Classe de la finestra que mostra el gràfic de dades
class GraphWindow(QtGui.QDialog): 
    
    #Funció que es crida en prémer el botó Tornar
    #Tanca la finestra
    def back(self):
        self.close()
        
    #Funció que es crida en prémer el botó Gràfic 
    #Connecta amb l'aplicació Read que conté la llibreria thethings.iO, modifica el fitxer config.json amb el 
    #Thing_Token corresponent i crea i executa un objecte PlotThread connectant els "SIGNALS" notifyProgress i errorMessage
    def graph(self): 
        if not self.isGraph:            
            thethingsio=Configthethingsio(8002)        
            if thethingsio.connectLibraryTheThingsio():
                if thethingsio.modify("read",self.token):                    
                    self.isGraph=True
                    self.myLongTask = PlotThread(thethingsio,self.isTemp,self.isHum,self.startDate,self.endDate,self.hourUtcOffset,self.canvas)
                    self.myLongTask.notifyProgress.connect(self.onProgress)
                    self.myLongTask.errorMessage.connect(self.showErrorMessage)
                    self.myLongTask.start()
                else:
                    QtGui.QMessageBox.warning(None,"Error",u"No es pot mostrar el gràfic") 
            else:
                QtGui.QMessageBox.warning(None,"Error",u"No es pot mostrar el gràfic") 
            
    
    #Funció que es crida per rebre "SIGNAL" de la classe PlotThread
    #@param: strMessage: missatge d'error
    #Mostra una finestra QMessageBox amb el missatge d'error
    def showErrorMessage(self,strMessage):
        QtGui.QMessageBox.warning(None,"Error",strMessage) 
    
    #Constructor de la classe 
    #Inicialitzar GUI i les seves funcions
    #@param: token: string amb el Thing_Token de la mota
    #@param: isTemp: booleà per indicar que es vol mostrar la temperatura
    #@params: isHum: booleà per indicar que es vol mostrar l'humitat, startDate: string amb la data inicial
    #@params: endDate: string amb la data final, hourUtcOffset: integer amb el òfset horari respecte UTC        
    def __init__(self, token, isTemp, isHum, startDate, endDate, hourUtcOffset):        
        QtGui.QDialog.__init__(self)  
        self.index=0 
        self.token=token   
        self.isTemp= isTemp
        self.isHum = isHum
        self.startDate= startDate
        self.endDate = endDate
        self.hourUtcOffset=hourUtcOffset
        self.setupUI()       
        self.isGraph=False
        self.initProgressBar()           
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)
        self.connect(self.pushButton_Graph, QtCore.SIGNAL('clicked()'), self.graph)
     
    #Funció que es crida per rebre "SIGNAL" de la classe PlotThread   
    #Acutalitzar el valor de la barra de progrés    
    def onProgress(self):
        self.progressBar.setValue(self.progressBar.value()+1)        
        
    #Funció que inicialitza la barra de progrés 
    def initProgressBar(self):
        if self.isTemp and self.isHum:
            self.progressBar.setRange(0,4)            
        elif self.isTemp or self.isHum:
            self.progressBar.setRange(0,2) 
           
        self.progressBar.setValue(0)
            
    #Inicialització de la GUI    
    def setupUI(self):       
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.verticalLayout = QtGui.QVBoxLayout(self) 
               
        self.canvas=GraphCanvas.GraphCanvas()
        self.canvas.setFixedWidth(450)  
              
        self.progressBar = QtGui.QProgressBar(self)
        
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
                 
        self.verticalLayout.addWidget(self.canvas) 
        self.verticalLayout.addWidget(self.progressBar) 
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.verticalLayout.setAlignment(self.horizontalLayout, QtCore.Qt.AlignLeft)
    
            