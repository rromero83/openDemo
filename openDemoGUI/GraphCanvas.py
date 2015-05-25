# -*- encoding: utf-8 -*-
'''
Created on May 7, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''

#Import genèric
import numpy as np

#Imports maplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Classe per generar gràfic
class GraphCanvas(FigureCanvas):
    #Variable global
    data_labels=['00:00','06:00','12:00','18:00','24:00']
    
    #Constructor de la classe
    def __init__(self, width = 5, height = 4, dpi = 80):
        #Crear una figura
        self.figure = Figure(figsize=(width, height), dpi=dpi, facecolor = '#D4D0C8')
        
        #Afegir la figura en el Canvas
        FigureCanvas.__init__(self, self.figure)
              
        
        #Crear un eix
        self.ax1 = self.figure.add_subplot(111)
        self.ax1.hold(False)
       
    #Funció que representa els valors de temperatura
    #@param: xdata: llista amb el valor dels temps en què s'ha emmagatzemat cada valor de temperatura
    #@param: data: valors de temperatura
    def plotFigureTemperature(self,xdata, data):   
        try: 
            self.ax1.plot(xdata,data, 'r-')
            self.ax1.set_ylim([0,50])
            self.ax1.set_ylabel(u'Temperatura (°C)',color='r')  
        except:
            pass       
            
    #Funció que representa els valors d'humitat
    #@param: xdata: llista amb el valor dels temps en què s'ha emmagatzemat cada valor d'humitat 
    #@param: data: valors d'humitat, isTemp: booleà per indicar que es vol mostrar la temperatura  
    def plotFigureHumidity(self,xdata,data, isTemp):
        try: 
            if isTemp:
                self.ax2=self.ax1.twinx()
                self.ax2.plot(xdata,data, 'b-')
                self.ax2.set_ylim([0,100])
                self.ax2.set_ylabel(u'Humitat relativa (%)',color='b')
            else:
                self.ax1.plot(xdata,data, 'b-')
                self.ax1.set_ylim([0,100])
                self.ax1.set_ylabel(u'Humitat relativa (%)',color='b')
        except:
            pass  
        
        
    #Funció que afegeix el títol i dibuixa el gràfic  
    #@param:isTemp: booleà per indicar que es vol mostrar la temperatura
    #@param:isHum: booleà per indicar que es vol mostrar l'humitat
    def setTitle(self,isTemp,isHum):            
        text=''
        isBoth=False
        if isTemp and isHum:
            text= u'Històric de temperatura i humitat'  
            isBoth=True          
        elif isTemp and not isHum:
            text= u'Històric de temperatura'            
        else:
            text= u'Històric d\'humitat relativa'                          
        self.ax1.set_title(text)
        pos = np.arange(0,1441,360)
        self.ax1.set_xticks(pos)
        if isBoth:
            try:
                self.ax2.set_xticks(pos)
            except:
                pass
        self.ax1.set_xticklabels(self.data_labels)
        self.ax1.grid(which="both")
        self.draw()
           
            
        