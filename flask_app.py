from flask import Flask
from funciones_app import *
from flask import request,jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import tweepy
import os

#load_dotenv()
project_folder = os.path.expanduser('~/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
app = Flask(__name__)
CORS(app)
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')

client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret,
                       wait_on_rate_limit=True)

@app.route('/clasificar', methods=['POST'])
def clasificar():
    if request.method == 'POST':
        datos=request.get_json()
        #Tweets antiguos
        tweets_antiguos= datos['tweets']
        mensajes=""
        for t in tweets_antiguos:
            mensajes = mensajes  + " " + traducir_mensaje(t['mensaje'])
        #Tweets Nuevos
        usuario=datos['usuario']
        fecha_actual=datos['fecha_actual']
        fecha_pasada=datos['fecha_pasada']
        tweets=[]
        try:
            tweets=tweets_usuario(client,usuario,fecha_actual,fecha_pasada)
        except:
            print('Error')
        #Agregar Tweets Nuevos
        for t in tweets:
            mensajes = mensajes  + " " + traducir_mensaje(t['texto'])
        print(mensajes)
        estado={}
        estado['resultado'] = -1
        #Pickle
        vec=obtener('vectorizer')
        red=obtener('red')
        if(mensajes!="" and len(tweets)>0):
            data=procesar_data(vec,[mensajes])
            resul=red.predict(data).tolist()
            for est in resul:
                estado['resultado'] = est
            texto_traducido=traducir(tweets)
            data=procesar_data(vec,texto_traducido)
            resul=red.predict(data).tolist()
            for indice in range(len(tweets)):
                tweets[indice]['estado']= resul[indice]
        return jsonify({'tweets':tweets,'estado': estado['resultado']})



@app.route('/tweets', methods=['POST'])
def obtenerTweets():
    if request.method == 'POST':
        datos=request.get_json()
        usuario=datos['usuario']
        fecha_actual=datos['fecha_actual']
        fecha_pasada=datos['fecha_pasada']
        tweets=tweets_usuario(client,usuario,fecha_actual,fecha_pasada)
        print(tweets)
        #Agregar Tweets Nuevos
        estado={}
        mensajes=""
        for t in tweets:
            mensajes = mensajes  + " " + traducir_mensaje(t['texto'])
        print(mensajes)
        estado['resultado'] = -1
        vec=obtener('vectorizer')
        red=obtener('red')
        if(mensajes!="" and len(tweets)>0):
            #Analizar Estado
            data=procesar_data(vec,[mensajes])
            resul=red.predict(data).tolist()
            for est in resul:
                estado['resultado'] = est
            #Analizar Tweets
            texto_traducido=traducir(tweets)
            data=procesar_data(vec,texto_traducido)
            resul=red.predict(data).tolist()
            for indice in range(len(tweets)):
                tweets[indice]['estado']= resul[indice]
        return jsonify({'tweets':tweets,'estado': estado['resultado']})


if __name__=="__main__":
    app.run()
