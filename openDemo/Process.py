# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports genèrics
import thread,socket
#Imports openDemo
import Log
from Database import Database


#Funció que envia per CoAP una comanda PUT perquè la mota deixi d'enviar paquets
#@param: c: objecte coap
#@param: ipv6: string amb l'adreça IPv6 de la mota 
def sendStopAddMote(c,ipv6):   
    try: 
        
        c.PUT('coap://[{0}]/caddmotes'.format(ipv6),payload = [ord('1')],)
    except:
        Log.writeError("No s'ha pogut enviar ordre stopAddMotes")
        pass

#Funció que verifica el format IPv6
#@param: ipv6: string amb l'adreça IPv6 de la mota 
def checkIPv6Format(ipv6):
    formatOK=True    
    try:
        socket.inet_pton(socket.AF_INET6, ipv6)
    except:
        Log.writeError( "format IPv6: "+ipv6)
        formatOK=False
        pass
    return formatOK

#Funció que verifica que IPv6 comenci per bbbb::
#@param: ipv6: string amb l'adreça IPv6 de la mota 
def checkIPOpenWSN(ipv6):
    return ipv6.startswith('bbbb::')

#Funció que processa el paquet rebut, si IPv6 no esta en el sistema s'afegeix
#Si s'afegeix o ja esta en el sistema s'envia ordre a la mota perque deixi d'enviar
#@param: c: objecte coap
#@param: ipv6: string amb l'adreça IPv6 de la mota 
def process(c,ipv6):     
    if ipv6 is not None:
        isOk=False        
        db=Database()
        if db.connect():
            records=db.select("SELECT ipv6 FROM motes where ipv6='%s'" % ipv6)
            if records is not None:
                if not records:
                    if checkIPv6Format(ipv6) and checkIPOpenWSN(ipv6):  
                        if db.insert("INSERT INTO motes (ipv6) VALUES ('"+ipv6+"')"):
                            isOk=True
                else:
                    isOk=True
        db.close()
        if isOk:  
            thread.start_new_thread( sendStopAddMote,(c,ipv6,)) 
           