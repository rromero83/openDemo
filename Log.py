# -*- encoding: utf-8 -*-
'''
Created on May 10, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports genèrics
import logging,os
#Variable global
global logger

#Funció per inicialitzar el log
def init():
    global logger
    logger = logging.getLogger('openDemo')
    logger.setLevel(logging.ERROR)
    path='/opt/openDemo/log/'
    if not os.path.exists(path):
        os.makedirs(path)
    handler = logging.FileHandler(path+'openDemo.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

#Funció per escriure en el log
def writeError(strError):
    global logger
    logger.error(strError)