import os
import time
import pymongo

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = cliente["prueba"]
coleccion = mydb["logs"]

f = open('/var/log/remote/FG/192.168.60.36.log','r') #Carga del archivo

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
    x = []
    for e in data:
        full_data.append(e.split("="))

    for e in range (4,len(full_data)):
        x.append((' "{}":"{}" ').format(full_data[e][0],full_data[e][1]))

    dataInsert = "{ "
    for e in range(len(x)-1):
        dataInsert = dataInsert + str(x[e]) + ","
    dataInsert = dataInsert + str(x[len(x)-1]) + " }"
    dataInsert = dataInsert.replace("\n","")
    dataInsert = json.dumps(dataInsert)
    x = coleccion.insert(dataInsert).inserted_id
    print(x)