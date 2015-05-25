# -*- coding: utf-8 -*-
'''
Created on Apr 14, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports openDemo
import ObjectCoAP,Log

#Variables globals    
global database, tempSet

#Funció per obtenir el valor de temperatura de la base de dades
#@param: db: objecte Database
def getSettings (db):
    global tempSet,database
    database = db
    tempSet=db.getTemperaturaConsigna()
               
#Funció que verifica si s'ha d'enviar ordre de control a la mota que controla la caldera
#@param: lowTemp: booleà que indica si cap valor de temperatura està per sota del valor de consigna
def checkAction(lowTemp):    
    ipActuator = getIPActuator () 
    if ipActuator is not None:
        state=getState(ipActuator)  
        if state is not None:
            if (lowTemp and state == '0'):  
                sendOrder(ipActuator,'1')                               
            elif (lowTemp == False and state=='1'): 
                sendOrder(ipActuator,'0')                               
    
#Funció que retorna un booleà per indicar si la temperatura capturada està per sota de la de consigna 
#@param: temp: valor real de la temperatura capturat    
def checkTemp(temp):
    global tempSet
    lTemp=False
    if temp < tempSet:
        lTemp=True
    return lTemp

#Funció per obtenir IPv6 de la mota que actua sobre la caldera
def getIPActuator ():
    global database
    ip = None
    rec=database.select("SELECT ipv6 FROM motes where type=1")
    for row in rec:
        ip = row[0]
    return ip

#Funció per obtenir l'estat actual de l'actuador fent un CoAP GET al recurs 'cactuator'
#@param: ipActuator: string amb l'adreça IPv6 de la mota actuador
def getState(ipActuator):
    state=None
    try:
        if ipActuator is not None:
            p = ObjectCoAP.sendGET(ipActuator,'cactuator')
            state = chr(p[0])
    except:
        Log.writeError("No es pot obtenir l'estat")
        pass
    return state

#Funció que envia ordre a l'actuador a través CoAP PUT en el recurs 'cactuator'
#@param: ipActuator: string amb l'adreça IPv6 de la mota actuador
#@param: order: string amb l'ordre a realitzar per la mota
def sendOrder(ipActuator,order):
    try:
        ObjectCoAP.sendPUT(ipActuator,'cactuator',order)      
    except:
        Log.writeError( "No s'ha pogut enviar l'ordre")
        pass