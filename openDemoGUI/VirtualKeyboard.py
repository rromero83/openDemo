# -*- encoding: utf-8 -*-
'''
Created on May 12, 2015

UOC Treball Final de Màster

@author: roberto
'''
#Imports PyQT 
from PyQt4 import QtCore, QtGui
#Import icones
import icon_rc
#Funció creada per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
#Classe QPushButton personalitzada
class PushButton_Lletra(QtGui.QPushButton):
    def __init__(self, key):
        super(PushButton_Lletra, self).__init__()
        self._key = key        
        self.connect(self, QtCore.SIGNAL("clicked()"), self.emitKey)
        self.setFixedSize(30,30)      

    def emitKey(self):
        self.emit(QtCore.SIGNAL("sigKeyButtonClicked"), self._key)

#Classe de la Finestra Teclat Virtual
class VirtualKeyboard(QtGui.QDialog): 
    
    #Variable global
    editText = QtCore.pyqtSignal(int,str)
    
    #Funció que es crida en prémer el botó Majúscules  
    #"toggle" de l'activació de les majúscules
    def switchMaj(self):
        self.maj = not self.maj

    #Funció que es crida en prémer qualsevol lletra
    #Afegeix la lletra en el camp d'edició
    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.maj]
        self.inputLine.setText(self.inputString)
    
    #Funció que es crida en prémer el botó Esborrar
    #Esborra l'última lletra
    def delete(self):
        self.inputLine.backspace()
        self.inputString = self.inputString[:-1]
    
    #Funció que es crida en prémer el botó Tornar
    #Retornar a la Finestra Editar Configuració a través de "SIGNALS" del contingut del camp d'edició i tancar la finestra
    def back(self):
        self.editText.emit(self.identi,self.inputLine.text())       
        self.close()
    
    #Constructor de la classe 
    #@param: identi: identificador del camp a modificar 0 - camp descripció, 1 - camp Thing_Token
    #@param: text: contingut actual del camp descripció o Thing_Token
    #Inicialitzar GUI i les seves funcions  
    def __init__(self,identi,text):        
        QtGui.QDialog.__init__(self)
        self.identi =identi
        self.inputString = text
        self.maj = 0
        self.setupUI()
        self.inputLine.setText(self.inputString)
        self.keyListByLines = [
                    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','7','8','9'],
                    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '/','4','5','6'],
                    ['z', 'x', 'c', 'v', 'b', 'n', 'm',' ', '-', '0', '1','2','3'],
                ]
        
        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):           
                pushButton_Lletra = PushButton_Lletra(key)
                pushButton_Lletra.setText(key)
                pushButton_Lletra.setFont(self.fontText) 
                self.keyboardLayout.addWidget(pushButton_Lletra, self.keyListByLines.index(line), line.index(key))
                self.connect(pushButton_Lletra, QtCore.SIGNAL("sigKeyButtonClicked"), self.addInputByKey)
                #self.keyboardLayout.setColumnMinimumWidth(keyIndex, 25)
            #self.keyboardLayout.setRowMinimumHeight(lineIndex, 25)
        
        self.connect(self.pushButton_Maj, QtCore.SIGNAL("clicked()"), self.switchMaj)
        self.connect(self.pushButton_Del, QtCore.SIGNAL("clicked()"), self.delete)
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)  
        
    
    #Inicialització de la GUI    
    def setupUI(self):        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        
        self.keyboardLayout = QtGui.QGridLayout()
          
        self.fontText = QtGui.QFont()
        self.fontText.setPointSize(14)
        
        self.pushButton_Maj = QtGui.QPushButton()
        self.pushButton_Maj.setText(u'Majúscules')
        self.pushButton_Maj.setFont(self.fontText)
        
        self.pushButton_Del = QtGui.QPushButton()
        self.pushButton_Del.setText('Esborrar')
        self.pushButton_Del.setFont(self.fontText) 
            
        self.inputLine = QtGui.QLineEdit()       
        self.inputLine.setFont(self.fontText)            
        
        self.pushButton_Back = QtGui.QPushButton(self) 
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/back.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Back.setIcon(iconBack) 
        self.pushButton_Back.setIconSize(QtCore.QSize(60, 60))       
        self.pushButton_Back.setFixedSize(QtCore.QSize(70, 70))  
        
        self.horizontalLayout = QtGui.QHBoxLayout() 
        self.horizontalLayout.addWidget(self.pushButton_Del)
        self.horizontalLayout.addWidget(self.pushButton_Maj)       

        self.verticalLayout.addWidget(self.inputLine)
        self.verticalLayout.addLayout(self.keyboardLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)  
        self.verticalLayout.addWidget(self.pushButton_Back)     


  
