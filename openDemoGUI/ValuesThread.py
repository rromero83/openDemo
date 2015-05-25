# -*- encoding: utf-8 -*-
'''
Created on May 8, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore
#Import openDemo
import ObjectCoAP

#Classe QThread per obtenir els valors de temperatura i humitat d'una mota
class ValuesThread(QtCore.QThread): 
    
    #Variable golbal
    getValues = QtCore.pyqtSignal(int,list)
    
    #Constructor de la classe 
    #@param: ipv6: adreça IPv6 de la mota
    def __init__(self,ipv6):        
        QtCore.QThread.__init__(self) 
        self.ipv6=ipv6
     
    #Funció per obtenir els valors de temperatura i humitat a través de la llibreria CoAP OpenWSN 
    #retorna els valors utilitzant "SIGNALS" enviats a la Finestra Valors   
    def getData(self):
        try:            
            temp =ObjectCoAP.sendGET(self.ipv6,'temp') 
            self.getValues.emit(0,temp)
            hum =ObjectCoAP.sendGET(self.ipv6,'hum' ) 
            self.getValues.emit(1,hum)            
        except:
            self.getValues.emit(2,[0])
            pass
    #Funció que es crida en realitzar el start() de la classe ValuesThread  
    def run(self): 
        self.getData()
        