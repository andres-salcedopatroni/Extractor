from deep_translator import GoogleTranslator
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import pickle
import tweepy

#Traducir texto
def traducir(texto):
    traducidos=[]
    for text in texto:
        traducidos.append(GoogleTranslator(source='auto', target='russian').translate(text['texto']))
    return traducidos

def traducir_mensaje(texto):
    return GoogleTranslator(source='auto', target='russian').translate(texto)

#Transformar la data para la red neuronal
def procesar_data(vectorizer,data):
    lista=vectorizer.transform(data)
    lista=lista.toarray()
    return lista

#Obtener una estructura
def obtener(nombre):
    with open('/home/andressalcedo2023/mysite/'+nombre+'.pkl', 'rb') as file:
    #with open(nombre+'.pkl', 'rb') as file:
        return pickle.load(file)

#Fecha de recuperacion
def fecha_recuperacion(meses):
    hoy = date.today()
    hoy = hoy - relativedelta(months=meses)
    fecha = hoy.strftime('%Y-%m-%dT00:00:00Z')
    return fecha

#Obtener tweets de usuario
def tweets_usuario(client,usuario,fecha_actual,fecha_pasada):
    twitterid = client.get_user(username=usuario)
    lista=[]
    try:
        for tweet in tweepy.Paginator(client.get_users_tweets,twitterid.data.id,start_time=fecha_pasada,end_time=fecha_actual,tweet_fields=['created_at','text'],exclude='retweets',max_results=100).flatten():
            lista.append({'texto':tweet.text,'fecha':tweet.created_at})
        return lista
    except NameError:
        return NameError,400