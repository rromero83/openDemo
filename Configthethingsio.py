# -*- encoding: utf-8 -*-
'''
Created on Mar 11, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''

#Imports genèrics
import json, socket
#Import openDemo
import Log

#Definicio de la classe que gestiona les accions amb thethings.iO
class Configthethingsio:
    #Variables globals
    localhost='127.0.0.1'
    BUFSIZ=1024
    #Constructor de la classe
    def __init__(self,port):
        self.port = port
        self.s = None
        
    #Funció per connectar amb l'aplicació de la llibreria thethings.io a traves de socket, timeout=5 segons
    def connectLibraryTheThingsio(self):        
        isConnected=True
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(5)
            self.s.connect((self.localhost, self.port))
        except:
            Log.writeError("No s'ha pogut connectar amb thethings.iO")
            isConnected=False
            pass
        finally:
            return isConnected
        
    #Funció per enviar dades a la llibreria thethings.iO i verifica que no hi ha error
    #@param: data: dades a enviar a la plataforma thethings.iO en format JSON
    def sendToTheThingsio(self,data): 
        isSent=True      
        try:
            if self.s is not None:
                self.s.send(data)
                data=self.s.recv(self.BUFSIZ)                
                if (data=='error'):
                    isSent=False
        except:
            isSent=False
            Log.writeError( "En la comunicacio amb thethings.iO")
            pass
        finally:
            return isSent
     
    #Funció per llegir dades de la plataforma thethings.iO
    #@param: key: "temperature" o "humidity"
    #@param: startDate: data inicial
    #@param: endDate: data final 
    def getToTheThingsio(self, key,startDate,endDate):
        dataReceived="" 
        try:
            if self.s is not None:
                self.s.send('{"key":"'+key+'", "startDate":"'+startDate+'", "endDate":"'+endDate+'"}')
                while True:
                    data=self.s.recv(self.BUFSIZ)                                    
                    if data == '</FINAL>':                        
                        break;
                    else:
                        dataReceived= dataReceived+data
                dataReceived=dataReceived[:-1]                                                            
        except:            
            Log.writeError("En la comunicacio amb thethings.iO")
            pass
        finally:
            return dataReceived
    
    #Funció per tancar socket amb amb l'aplicació de la llibreria thethings.io
    def closeConnectionLibraryTheThingsio(self):        
        try:
            if self.s is not None:
                self.s.close()
        except:
            Log.writeError( "No s'ha pogut tancar la comunicacio amb thethings.iO")
            pass
        
    #Funció per modificar el valor del Thing_Token en el fitxer config.json  
    #@param: path: "write" o "read"
    #@param:  thingToken: string amb el Thing_Token
    def modify(self,path,thingToken): 
        isModify=True
        try:                           
            with open("/usr/local/thethingsio-coap-openDemo/openDemo/"+path+"/config.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                data["thingToken"]=thingToken
                jsonFile.seek(0)
                jsonFile.write(json.dumps(data))
                jsonFile.truncate()        
                jsonFile.close()
        except:
            isModify=False
            Log.writeError("En modificar el fitxer config.json")
            pass
        finally:
            return isModify


