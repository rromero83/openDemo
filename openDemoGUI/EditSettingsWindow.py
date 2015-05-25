# -*- encoding: utf-8 -*-
'''
Created on May 4, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore, QtGui

#Import icones 
import icon_rc

#Imports openDemo
from Database import Database
from VirtualKeyboard import VirtualKeyboard

#Funció afegida per Qt Creator
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#Classe de la Finestra d'Edició de la Configuració
class EditSettingsWindow(QtGui.QDialog):
    #Variables globals
    listTipusMota=['Sensor','Actuador']    
    update = QtCore.pyqtSignal()
    
    #Funció que es crida en prémer el botó Tornar
    #Tanca la finestra
    def back(self):
        self.close()        
    
    #Funció que es crida per rebre "SIGNAL" de la Finestra Teclat Virtual
    #@param: identi: 0 - camp descripció, 1 - camp Thing_Token
    #@param: text: contingut del camp
    #Modifica el camp descripció o  Thing_Token amb el contingut del camp  
    def editText(self, identi, text):
        if identi == 0:
            self.line_des.setText(text)            
        else:
            self.line_token.setText(text)
        
    #Funció que es crida en prémer el botó Editar en el camp de la descripció 
    #Obre la Finestra Teclat Virtual amb el contingut del camp descripció
    def editDes(self):
        virtualKeyboard= VirtualKeyboard(0,str(self.line_des.text()))
        virtualKeyboard.editText.connect(self.editText)
        virtualKeyboard.show()
        virtualKeyboard.exec_()
    
    #Funció que es crida en prémer el botó Editar en el camp del Thing_Token 
    #Obre la finestra del Teclat Virtual amb el contingut del camp Thing_Token
    def editToken(self):
        virtualKeyboard= VirtualKeyboard(1,str(self.line_token.text()))
        virtualKeyboard.editText.connect(self.editText)
        virtualKeyboard.show()
        virtualKeyboard.exec_()
        
    def checkDescription(self,des):
        isChecked=True
        if self.desAnt != des:
            if self.db.descripExist(des):
                isChecked=False
        return isChecked
    
    #Funció que es crida en prémer el botó Guardar
    #Actualitza els canvis en la base de dades i envia una "senyal" a la Finestra Configuració   
    def save(self):        
        des = str(self.line_des.text())
        if self.db.connect():
            
            if  self.checkDescription(des):
                token = str(self.line_token.text())
                tipus = str(self.combo_type.currentIndex())        
                if not self.db.updateSettingsMota(self.identi,des,token,tipus):
                    QtGui.QMessageBox.warning(None,"Error","No s'han pogut actualitzar els camps") 
                else:
                    self.update.emit()
            else:
                QtGui.QMessageBox.warning(None,"Error",u"La descripció ja existeix") 
        else:
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades")  
        self.db.close()
        
    #Constructor de la classe
    #@param: identi: id de la taula motes de la base de dades 
    #Inicialitzar GUI i les seves funcions                      
    def __init__(self, identi):        
        QtGui.QDialog.__init__(self)
        self.identi=identi
        self.setupUI()
        self.db=Database()
        if self.db.connect():
            (des,token,tipus) =self.db.getSettingsMota(self.identi)
            self.desAnt=des
            self.line_des.setText(des)
            self.line_token.setText(token)
            self.combo_type.setCurrentIndex(tipus)
        else:
            QtGui.QMessageBox.warning(None,"Error","No es pot connectar amb la base de dades") 
        self.db.close()
       
        self.connect(self.pushButton_Back, QtCore.SIGNAL('clicked()'), self.back)
        self.connect(self.pushButton_Save, QtCore.SIGNAL('clicked()'), self.save)
        self.connect(self.pushButton_Edit_des, QtCore.SIGNAL('clicked()'), self.editDes)
        self.connect(self.pushButton_Edit_token, QtCore.SIGNAL('clicked()'), self.editToken)
        
    #Inicialització de la GUI
    def setupUI(self):        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.verticalLayout = QtGui.QVBoxLayout(self)
        
        self.fontText = QtGui.QFont()
        self.fontText.setPointSize(14)

        iconEdit = QtGui.QIcon()
        iconEdit.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        label_des= QtGui.QLabel(u"Descripció:", self)
        label_des.setFont(self.fontText)
        
        self.line_des = QtGui.QLineEdit(self)
        self.line_des.setFont(self.fontText)
        self.line_des.setFixedWidth(300)
        
        self.pushButton_Edit_des = QtGui.QPushButton(self)         
        self.pushButton_Edit_des.setIcon(iconEdit)
        self.pushButton_Edit_des.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_Edit_des.setFixedSize(QtCore.QSize(30, 30))
        
        self.horizontalLayout_2 = QtGui.QHBoxLayout() 
        self.horizontalLayout_2.addWidget(self.line_des)
        self.horizontalLayout_2.addWidget(self.pushButton_Edit_des)
                
        label_token= QtGui.QLabel("Thing_Token:", self)
        label_token.setFont(self.fontText)
        
        self.line_token = QtGui.QLineEdit(self)
        self.line_token.setFont(self.fontText)
        self.line_token.setFixedWidth(300)
        
        self.pushButton_Edit_token = QtGui.QPushButton(self)         
        self.pushButton_Edit_token.setIcon(iconEdit)
        self.pushButton_Edit_token.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_Edit_token.setFixedSize(QtCore.QSize(30, 30))
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout() 
        self.horizontalLayout_3.addWidget(self.line_token)
        self.horizontalLayout_3.addWidget(self.pushButton_Edit_token)
        
        label_type= QtGui.QLabel("Tipus de mota:", self)
        label_type.setFont(self.fontText)
        
        self.combo_type = QtGui.QComboBox(self)
        self.combo_type.setFont(self.fontText)
        self.combo_type.addItem(self.listTipusMota[0])
        self.combo_type.addItem(self.listTipusMota[1])
        self.combo_type.setFixedWidth(300)
        
        self.pushButton_Back = QtGui.QPushButton(self) 
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/back.jpeg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Back.setIcon(iconBack)
        self.pushButton_Back.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Back.setFixedSize(QtCore.QSize(70, 70)) 
         
        self.pushButton_Save = QtGui.QPushButton(self) 
        iconSave = QtGui.QIcon()
        iconSave.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Save.setIcon(iconSave)
        self.pushButton_Save.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_Save.setFixedSize(QtCore.QSize(70, 70))
 
        self.horizontalLayout = QtGui.QHBoxLayout() 
        self.horizontalLayout.addWidget(self.pushButton_Back)        
        self.horizontalLayout.addWidget(self.pushButton_Save) 
     
        self.verticalLayout.addWidget(label_des)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setAlignment(self.horizontalLayout_2, QtCore.Qt.AlignLeft)  
        self.verticalLayout.addWidget(label_token)
        self.verticalLayout.addLayout(self.horizontalLayout_3)  
        self.verticalLayout.setAlignment(self.horizontalLayout_3, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(label_type)
        self.verticalLayout.addWidget(self.combo_type)         
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.verticalLayout.setAlignment(self.horizontalLayout, QtCore.Qt.AlignLeft)
        
    