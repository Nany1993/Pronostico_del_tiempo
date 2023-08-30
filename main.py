# Importar módulos necesarios
import time
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
from utils import send_twilio_message, get_forecast  # Importar funciones desde utils.py

query = 'Cucuta'
api_key = API_KEY_WAPI

url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

response = requests.get(url_clima).json()

datos = []
Horas_Disponibles = len(response['forecast']['forecastday'][0]['hour'])
for i in tqdm(range(Horas_Disponibles), colour='green'):
    datos.append(get_forecast(response, i))  # Utilizar la función get_forecast desde utils.py

col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
df = pd.DataFrame(datos, columns=col)
df = df.sort_values(by='Hora', ascending=True)

df_rain = df[(df["Hora"] > 6) & (df["Hora"] < 22)]
df_rain = df_rain[["Hora", "Condicion", "Temperatura"]]
df_rain.set_index("Hora", inplace=True)

time.sleep(2)

# Crear el cuerpo del mensaje
message_body = (
    f'\nHola! \n\n\n El pronostico de lluvia hoy {df["Fecha"][0]} en {query} es :\n\n\n {str(df_rain)}'
)

# Llamar a la función para enviar el mensaje de Twilio
send_twilio_message(message_body, '+573005424395')

print('Mensaje Enviado')
