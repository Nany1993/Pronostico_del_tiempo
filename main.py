# Importar módulos necesarios
from fastapi import FastAPI
app = FastAPI()

import time
import requests
import pandas as pd
from datetime import datetime
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
from utils import send_twilio_message, get_forecast  # Importar funciones desde utils.py


@app.get("/")
def index():
    return {"mensaje" : "Bienvenidos al Prónostico del tiempo"}

@app.get("/clima/{ciudad}/{hora}")
def clima_ciudad_hora(ciudad: str, hora: int):
    api_key = API_KEY_WAPI
    url_clima = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={ciudad}&days=1&aqi=no&alerts=no'
    response = requests.get(url_clima).json()

    # Filtrar los datos correspondientes a la hora ingresada
    datos = [get_forecast(response, hora)]

    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
    df = pd.DataFrame(datos, columns=col)

    # Convertir el DataFrame a formato JSON
    result = df.to_dict(orient="records")
    
    # Modificar los valores de lluvia para que sean más descriptivos
    result[0]['Lluvia'] = "Sí lloverá" if result[0]['Lluvia'] == 1 else "No lloverá"

    # Modificar los valores de probabilidad de lluvia
    result[0]['prob_lluvia'] = f"{result[0]['prob_lluvia']}% de probabilidad de que llueva"

    return result




"""@app.get("/Ciudad/{ciudad}")
def pronostico(ciudad):
    api_key = API_KEY_WAPI
    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+ciudad+'&days=1&aqi=no&alerts=no'
    response = requests.get(url_clima).json()
    datos = []
    Horas_Disponibles = len(response['forecast']['forecastday'][0]['hour'])
    for i in range(Horas_Disponibles):
        datos.append(get_forecast(response, i)) 

    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
    df = pd.DataFrame(datos, columns=col)
    df = df.sort_values(by='Hora', ascending=True)
    df_rain = df[(df["Hora"] > 6) & (df["Hora"] < 22)]
    df_rain = df_rain[["Hora", "Condicion", "Temperatura"]]
    df_rain.set_index("Hora", inplace=True)
    
    return df_rain"""
    
    