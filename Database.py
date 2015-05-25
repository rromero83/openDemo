# -*- encoding: utf-8 -*-
'''
Created on Mar 11, 2015

UOC Treball Final de Màster

@author: Roberto Romero
'''
#Imports genèrics
import sqlite3,os
#Imports openDemo
import Log

#Classe Database per accedir a la base de dades
class Database(object):

    #Constructor de la classe       
    def __init__(self):
        self.db=None
        self.db_file = '/opt/openDemo/bd/database.sqlite'
        
    #Funció que verifica si existeix la base de dades, en cas contrari la crea    
    def init(self):
        try:
            array=self.db_file.split('/')
            db_path='/'+array[1]+'/'+array[2]+'/'+array[3]+'/'
            pathexists=os.path.exists(db_path)
            if not pathexists:
                os.makedirs(db_path)            
            dbexists = os.path.exists(self.db_file)
            if not dbexists:
                    self.createTable()
        except:
            Log.writeError("No es pot inicialitzar la base de dades")

    #Funció que connecta amb la base de dades
    def connect(self):
        isConnected=True
        try:
            self.db=sqlite3.connect(self.db_file)
        except:
            isConnected=False
            Log.writeError("No s'ha pogut connectar amb la base de dades")
            pass
        finally:
            return isConnected
    
    #Funció que realitza una consulta a la base de dades i retorna el resultat
    #@param: sql: string amb la sentència de consulta SQL    
    def select(self,sql):
        records=None
        try:     
            cursor=self.db.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()            
        except:
            Log.writeError("No s'ha realitzat la consulta: "+sql)
            pass
        finally:
            return records 
        
    #Funció que realitza un "insert" a la base de dades i retorna un booleà indicant si s'ha realitzat correctament
    #@param: sql: string amb la sentència d'inserció SQL  
    def insert(self,sql):
        okInsert=True
        try:
            cursor=self.db.cursor()
            cursor.execute(sql) 
            self.db.commit()            
        except:
            self.db.rollback()
            okInsert=False
            Log.writeError("No s'ha pogut guardar el registre")
            pass
        finally:
            if cursor is not None:
                cursor.close()
            return okInsert
     
    #Funció que realitza un "update" a la base de dades i retorna un booleà indicant si s'ha realitzat correctament
    #@param: sql: string amb la sentència d'actualització SQL     
    def update(self,sql):
        okUpdate=True
        try:
            cursor=self.db.cursor()
            cursor.execute(sql) 
            self.db.commit()            
        except:
            self.db.rollback()
            okUpdate=False
            Log.writeError("No s'ha pogut actualitzar el registre")
            pass
        finally:
            if cursor is not None:
                cursor.close()
            return okUpdate
    #Funció que tanca la connexió amb la base de dades        
    def close(self):
        try:
            if self.db is not None:
                self.db.close()
        except:
            Log.writeError("No s'ha pogut tancar la connexio amb la base de dades")
            pass
        finally:
            self.db=None
    
    #Funció que crear les dues taules de la base de dades       
    def createTable(self):
        try:
            if self.connect():
                sqlt1="""CREATE TABLE "motes" ("id" INTEGER PRIMARY KEY  NOT NULL , "ipv6" VARCHAR NOT NULL , "thingToken" VARCHAR DEFAULT null, "type" INTEGER NOT NULL DEFAULT (0), "description" VARCHAR DEFAULT null)"""
                cursor = self.db.cursor() 
                cursor.execute(sqlt1)
                sqlt2="""CREATE TABLE "settings" ("id" INTEGER PRIMARY KEY  NOT NULL , "temp" INTEGER NOT NULL )"""
                cursor.execute(sqlt2)
                cursor.execute("INSERT INTO settings (temp) VALUES (19)")
                self.db.commit()
                cursor.close()            
        except:
            self.db.rollback()
            Log.writeError("No s'ha pogut crear la taula")
            pass
        finally:
            self.close()
    
    #Funció que retorna el valor de temperatura de consigna 
    def getTemperaturaConsigna(self):
        tempSet=None
        rec=self.select("SELECT temp FROM settings")
        for row in rec:
            tempSet = row[0]  
        return tempSet
    
    #Funció que retorna un booleà indicant si s'ha pogut actualitzar el valor de temperatura de consigna 
    #@param: temp: valor de consigna de temperatura a actualitzar  
    def updateTemperaturaConsigna (self,temp):
        return self.update("UPDATE settings SET temp= %s"%temp )
    
    #Funció que retorna un diccionari descripció-ipv6 per a cada mota sensor si el camp descripció no és null
    def getDiccDescriptionIpv6(self):
        dicc=dict()
        rec=self.select("SELECT description,ipv6 FROM motes WHERE type=0 and description IS NOT NULL and description !=''")
        for row in rec:
            dicc[str(row[0])]=str(row[1])
        return dicc
    
    #Funció que retorna un diccionari descripció-Thing_Token per a cada mota sensor si els camps description i thingToken no són null
    def getDiccDescriptionToken(self):
        dicc=dict()
        rec=self.select("SELECT description,thingToken FROM motes WHERE type=0 and description IS NOT NULL and thingToken IS NOT NULL and description !='' and thingToken !=''")
        for row in rec:
            dicc[str(row[0])]=str(row[1])
        return dicc   
    
    #Funció que retorna els camps  description,thingToken,type d'una mota
    #@param: id: integer amb el id de la mota en la BD 
    def getSettingsMota (self, idindex):                
        tipus=0
        rec=self.select("SELECT description,thingToken,type FROM motes WHERE id=%s"%idindex)
        for row in rec:
            des=str(row[0])
            token=str(row[1])
            tipus=int(row[2]) 
        if des is None or des=='None':
            des=""   
        if token is None or token=='None':
            token=""       
        return des,token,tipus
    
    #Funció que retorna un booleà indicant si la descripció proporcionada existeix en la base de dades
    #@param: des: string amb la descripció d'una mota
    def descripExist(self,des):
        exist=False
        rec=self.select("SELECT id FROM motes WHERE description='%s'"%des)
        if len(rec)>0:
            exist=True
        return exist
    
    #Funció que retorna un booleà indicant si s'ha pogut actualitzar els paràmetres de configuració d'una mota
    #@param: id: integer amb el id de la mota en la BD  
    #@param: des: string amb la descripció de la mota  
    #@param: token: string amb el Thing_Token de la mota   
    #@param: tipus: integer amb el tipus de mota, 0-mota sensor; 1-mota actuador
    def updateSettingsMota(self,idindex, des, token, tipus):
        return self.update("UPDATE motes SET description='%s',thingToken='%s',type=%s WHERE id=%s "%(des, token, tipus,idindex) )
        