# -*- encoding: utf-8 -*-
'''
Created on Apr 14, 2015

UOC Treball Final de Màster

@author:  Roberto Romero
'''

#Funció que calcula el valor real de la temperatura
#@param: value: valor de temperatura proporcionat per les motes
def getTemperature(value):
    temp = (value[0] << 8)+value[1]
    temperatura =-46.86+175.72*temp/ 65536
    return round(temperatura,2)

#Funció que calcula el valor real de l'humitat
#@param: value: valor d'humitat proporcionat per les motes
def getHumidity(value):
    hum = (value[0] << 8)+value[1]
    humidity = -6.0+125.0 * hum / 65536
    return round(humidity,2)