# -*- encoding: utf-8 -*-
'''
Created on Apr 14, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports CoAP OpenWSN
from coapdevelop.coap import coap,coapResource

#Variable global
global c
c= None

#Funció per inicialitzar objecte coap
def init():
    global c
    if c is None:        
        c=coap.coap() 
        
#Funció per afegir recursos en l'objecte coap
#@param: strResource: string amb el nom del recurs
def addResource(strResource):
    r=coapResource.coapResource(path = strResource)
    c.addResource(r)

#Funció per enviar peticions GET
#@param:ipv6: string amb l'adreça IPv6
#@param: resource: string amb el nom del recurs que es vol accedir
def sendGET(ipv6,resource):
    return c.GET('coap://[{0}]/{1}'.format(ipv6,resource))

#Funció per enviar peticions PUT
#@param:ipv6: string amb l'adreça IPv6
#@param: resource: string amb el nom del recurs que es vol accedir
#@param: order: string amb l'ordre a realitzar
def sendPUT(ipv6,resource, order):    
    c.PUT('coap://[{0}]/{1}'.format(ipv6,resource),payload = [ord(order)],)    
