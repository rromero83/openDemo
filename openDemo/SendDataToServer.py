# -*- coding: utf-8 -*-
'''
Created on Apr 16, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Import genèric
import threading
#Imports openDemo
import Log
from Configthethingsio import Configthethingsio

#Definició de la classe Thread SendDataToServer
class SendDataToServer(threading.Thread):
    #Variable global
    retries=2
    
    #Constructor de la classe
    #@param: lock: objecte Lock per sincronitzar fils
    #@param: tempValue: string amb el valor de temperatura
    #@param: hum: string amb el valor d'humitat    
    #@param: ipv6: string amb l'adreça IPv6 de la mota
    #@param: thingtoken: string amb el Thong_Token associat a la mota
    def __init__(self, lock,tempValue,hum,ipv6,thingtoken):
        threading.Thread.__init__(self)
        self.lock = lock
        self.tempValue=tempValue
        self.hum=hum
        self.ipv6 = ipv6
        self.thingtoken=thingtoken
        
    #Funció que es crida en realitzar start() a l'objecte SendDataToServer 
    #Connecta amb l'aplicació Write que inclou la llibreria de thethings.iO per enviar les dades a la plataforma thethings.iO      
    def run (self):
        self.lock.acquire()
        thethingsio=Configthethingsio(8000)
        if thethingsio.connectLibraryTheThingsio():
            if thethingsio.modify("write",self.thingtoken):
                if self.tempValue is not None:
                    i=0
                    isSaved=False
                    while(i<self.retries):
                        if thethingsio.sendToTheThingsio('{"key":"temperature","value":"'+str(self.tempValue)+'","units":"Temperature"}'):
                            isSaved=True
                            break
                        i=i+1
                    if not isSaved:
                        Log.writeError( "No s'ha pogut emmagatzemar la temperatura de la mota: "+self.ipv6)
                if self.hum is not None:  
                    i=0
                    isSaved=False
                    while(i<self.retries):                     
                        if  thethingsio.sendToTheThingsio('{"key":"humidity","value":"'+str(self.hum)+'","units":"Humidity"}'):
                            isSaved=True
                            break                        
                        i=i+1
                    if not isSaved:
                        Log.writeError( " no s'ha pogut emmagatzemar l'humitat de la mota: "+self.ipv6)
        thethingsio.closeConnectionLibraryTheThingsio()       
        self.lock.release()