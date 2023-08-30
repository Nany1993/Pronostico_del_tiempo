
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI

def send_twilio_message(message_body, to):
    from twilio.rest import Client

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_=PHONE_NUMBER,
        to=to
    )

    return message.sid

def get_forecast(response,i): #respuesta e iterador
    
    Fecha = response['forecast']['forecastday'][0]["hour"][i]['time'].split()[0]
    Hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    Condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    Temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    Lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    Probabilidad_Lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    
    return Fecha, Hora, Condicion, Temperatura, Lluvia, Probabilidad_Lluvia
