# -*- encoding: utf-8 -*-
'''
Created on May 7, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports PyQT 
from PyQt4 import QtCore

#Classe QThread per obtenir l'històric de valors de la plataforma thethings.iO i representar-los gràficament
class PlotThread(QtCore.QThread): 
    #Variables globals
    retries=2   
    notifyProgress = QtCore.pyqtSignal()
    errorMessage = QtCore.pyqtSignal(str)
    
    #Constructor de la classe     
    #@param: thethingsio: objecte Configthethingsio
    #@param: isTemp: booleà per indicar que es vol mostrar la temperatura
    #@params: isHum: booleà per indicar que es vol mostrar l'humitat, startDate: string amb la data inicial
    #@params: endDate: string amb la data final, hourUtcOffset: integer amb el òfset horari respecte UTC 
    #@param: canvas: objecte GraphCanvas
    def __init__(self, thethingsio,isTemp, isHum,startDate,endDate,hourUtcOffset, canvas):        
        QtCore.QThread.__init__(self) 
        self.thethingsio=thethingsio  
        self.isTemp=isTemp
        self.isHum=isHum
        self.startDate =startDate
        self.endDate=endDate
        self.hourUtcOffset=hourUtcOffset
        self.canvas =canvas
        
    #Funció per obtenir l'històric de valors de la plataforma thethings.iO i representar-los gràficament
    def plotFigures(self):  
        dataTemp=''
        dataHum=''                               
        if self.isTemp:
            dataTemp= self.getData("temperature") 
            self.notifyProgress.emit()                        
            if dataTemp !="":                
                dataTemp=dataTemp.split(",")
                dataTemp.reverse()
                xdataTemp=list()
                for item in dataTemp[:]:
                    if 'Z' in item:
                        xdataTemp.append(self.getTemps(item))
                        dataTemp.remove(item)                                                                          
                self.canvas.plotFigureTemperature(xdataTemp,dataTemp)                                                                                                                                                                    
            else:
                self.errorMessage.emit(u"No es pot mostrar el gràfic de temperatura")    
            self.notifyProgress.emit()                         
        if self.isHum: 
            dataHum =  self.getData("humidity") 
            self.notifyProgress.emit()                        
            if dataHum !="":
                dataHum=dataHum.split(",")
                dataHum.reverse()   
                xdataHum=list()
                for item in dataHum[:]:
                    if 'Z' in item:
                        xdataHum.append(self.getTemps(item))
                        dataHum.remove(item)                            
                self.canvas.plotFigureHumidity(xdataHum,dataHum,self.isTemp)                                                                                                                 
            else:
                self.errorMessage.emit(u"No es pot mostrar el gràfic d'humitat") 
            self.notifyProgress.emit()     
        if dataTemp!='' or dataHum!='':                                        
            self.canvas.setTitle(self.isTemp,self.isHum)                                                 
             
    #Funció qie obté els valors de la plataforma thethigns.iO
    #@para: key: "temperature" o "homidity"        
    def getData(self,key):
        i=0            
        while(i<self.retries):
            data=self.thethingsio.getToTheThingsio(key,self.startDate,self.endDate)
            if data !="": 
                break
            i=i+1
        return data    
    
    #Funció que calcula el nombre de minuts d'una hora del dia
    #@param: value: hora del dia
    def getTemps(self,value):
        arrayValue=value.split(':')   
        temps=int(arrayValue[0])*60+int(arrayValue[1])+60*self.hourUtcOffset  
        if temps>=1440:
            temps=temps-1440  
        return temps      
                 
    #Funció que es crida en realitzar el start() de la classe PlotThread                       
    def run(self):        
        self.plotFigures()