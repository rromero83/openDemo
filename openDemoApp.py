# -*- encoding: utf-8 -*-
'''
Created on May 9, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''

#Imports genèrics
import sys,threading,time

#Imports PyQT 
from PyQt4 import QtGui

#Imports openDemo
from openDemo import cDataCollection
from openDemoGUI import MainWindow 


#Classe multifil Application
class Application(threading.Thread):
    #Constructor
    def __init__(self):
        threading.Thread.__init__(self)  
    #Funció que realitza l'execució    
    def run (self):
        cDataCollection.start()

#Classe GUI
class ApplicationGUI():
    #Constructor
    def __init__(self):
        # Crear aplicació Qt
        self.app = QtGui.QApplication(sys.argv)

        # Omplir aplicació Qt
        self.gui = MainWindow.MainWindow()
        
    #Funció que realitza l'execució
    def start(self):       
        #Mostrar aplicació Qt
        self.gui.show()
        
        # Executar aplicació Qt
        self.app.exec_()

#Funció principal
def main():
    #openDemo Application   
    application =Application()    
    application.start()
    
    #Esperar per inicialitzar objectes
    time.sleep(5)
    
    #GUI Application
    applicationGUI = ApplicationGUI()
    applicationGUI.start()
        
if __name__ == "__main__":
    main()
