from datetime import datetime, timedelta
import numpy as np
import time
from threading import Thread
from fastapi import FastAPI

#Pasos para ejecutar
#Instalar librerias
#Ejecutar programa
#Ejecutar en terminal "uvicorn main:app --reload"
#Abrir "/docs" para mejor visualizacion

lista_ph = []
lista_humedad = []
lista_temperatura = []

def sensor_temperatura():
    while True:
        hora_actual = datetime.now().hour + datetime.now().minute / 60
        valor = round(20 + 5 * np.sin(2 * np.pi * hora_actual / 24 )* np.random.randint(0,100)/100, 2)
        lista_temperatura.append({"timestamp": datetime.now(), "valor": valor})

        lista_temperatura[:] = [d for d in lista_temperatura if d["timestamp"] > datetime.now() - timedelta(hours=24)]
        time.sleep(5)

def sensor_humedad():
    while True:
        valor = round(np.random.uniform(60, 90), 2)
        lista_humedad.append({"timestamp": datetime.now(), "valor": valor})

        lista_humedad[:] = [d for d in lista_humedad if d["timestamp"] > datetime.now() - timedelta(hours=24)]
        time.sleep(5)

def sensor_ph():
    while True:
        valor = round(np.random.uniform(5.5, 7.5), 2)
        lista_ph.append({"timestamp": datetime.now(), "valor": valor})

        lista_ph[:] = [d for d in lista_ph if d["timestamp"] > datetime.now() - timedelta(days=3)]
        time.sleep(5)

def iniciar_sensores():
    Thread(target=sensor_temperatura, daemon=True).start()
    Thread(target=sensor_humedad, daemon=True).start()
    Thread(target=sensor_ph, daemon=True).start()

#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

app = FastAPI()
iniciar_sensores()

@app.get("/temperatura")
def get_temperatura():
    return {
        "ultima_medida": lista_temperatura[-1] if lista_temperatura else None,
        "ultimas_10_medidas": lista_temperatura[-10:]
    }

@app.get("/humedad")
def get_humedad():
    return {
        "ultima_medida": lista_humedad[-1] if lista_humedad else None,
        "historial_de_humedad": lista_humedad
    }

@app.get("/ph")
def get_ph():
    return {
        "Historial_de_ph": lista_ph
    }
