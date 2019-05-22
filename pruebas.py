import os
import time
import pymongo
import ast
import json
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = cliente["prueba"]
coleccion = mydb["logs2"]

f = open('doc.log','r') #Carga del archivo

def follow(f): #Funcion que lee el ultimo renglon del archivo, si detecta cambios espera 0.3 segundos para volver a correr
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.3)
            continue
        yield line

loglines = follow(f)
for data in loglines:
    data = data.replace(" ",",",4)
    data = data.replace('"','')
    data = data.split(",")
    full_data = []
    diccionario = {}

    x = []
    for e in data:
        full_data.append(e.split("="))

    for e in range (4,len(full_data)):
        valor = "{'"+full_data[e][0]+"':'"+full_data[e][1]+"'}"
        valor = valor.replace('\n','')
        vcast = ast.literal_eval(valor)
        diccionario.update(vcast)
    insercion = coleccion.insert_one(diccionario)