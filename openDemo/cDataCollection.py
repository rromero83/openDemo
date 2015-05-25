# -*- coding: utf-8 -*-
'''
Created on May 2, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports genèrics
import time,threading

#Imports openDemo
from Database import Database
from SendDataToServer import SendDataToServer
import ObjectCoAP, Control, ConvertValue,Log

#Funció que captura les dades de cada mota realitzant peticions CoAP GET, envia les dades a l'aplicació Write.js
#i controla l'estat de la calefacció de la caldera
def collectData(db):
    global lock
    if db.connect():
        try:
            Control.getSettings (db)#Control sistema calefaccio
            records=db.select("SELECT ipv6,thingToken FROM motes where type=0 and thingToken IS NOT NULL and thingToken !=''")
            lowTemp=False#Control sistema calefaccio
            for row in records: 
                try:   
                    ipv6=str(row[0])
                    temp =ObjectCoAP.sendGET(ipv6,'temp' )                                                                        
                    if temp is not None:
                        tempValue = ConvertValue.getTemperature(temp)
                        if not lowTemp: #Control sistema calefaccio
                            lowTemp = Control.checkTemp(tempValue) #Control sistema calefaccio                               
                    hum =ObjectCoAP.sendGET(ipv6,'hum' )  
                    if hum is not None:
                        humValue=ConvertValue.getHumidity(hum)                    
                    if (tempValue or humValue) is not None:
                        send=SendDataToServer(lock,tempValue,humValue,ipv6,str(row[1]))#Emmagatzematge a thethings.iO
                        send.start()#Emmagatzematge a thethings.iO              
                except:
                    Log.writeError( "No hi ha comunicacio amb la mota "+ ipv6)
                    pass   
            Control.checkAction(lowTemp)#Control sistema calefaccio
        except:
            pass                                    
    db.close()
    
#Funció que inicialitza diversos components i crida a la funció collectData() cada minut
def start():
    global lock
    Log.init()
    ObjectCoAP.init()  
    ObjectCoAP.addResource('caddmotes')#Alta adreces IPv6       
    lock = threading.Lock()#Emmagatzematge a thethings.iO
    timeCollection=60
    db=Database()
    db.init()   
    while True:
        timeStart=time.time()                
        collectData(db)
        tempsActual= time.time()
        diff= tempsActual-timeStart
        if (diff<timeCollection):
            temps=timeCollection-(diff%60)        
            time.sleep(temps)
