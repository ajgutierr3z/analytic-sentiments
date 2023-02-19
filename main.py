import tweepy
import csv
import re
from textblob import TextBlob
from geopy.geocoders import Nominatim


def create_conect_twt(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> tweepy:
    """
    Create conecction with twitter
    :param consumer_key: key for consumer consults
    :param consumer_secret: key secret for consumer
    :param access_token: key for access
    :param access_token_secret: key secrets for access
    :return: tweepy.API(auth)
    """
    # Autentica a través de OAuth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Crea una instancia de la API de Tweepy
    return tweepy.API(auth)


def geolacalizacion_nombre(location: str) -> str:
    """
    Create string for location with latitude, longitude and count of km
    :param location: Location at calculate latitude and longitude
    :return: geolocator
    """
    # Crear el objeto geolocator
    geolocator = Nominatim(user_agent="Consult_data_research")

    # Obtener las coordenadas de la ciudad de México
    location = geolocator.geocode(location)

    # Crear una cadena con el formato necesario para la API de Twitter
    geocode_str = f"{location.latitude}, {location.longitude}, 1000km"
    return geocode_str


def create_analytic_csv(name_file: str, name_user: str, date: str, location: str, limit_twt: int,
                        search_words: list, api: tweepy):
    """
    Create analytic of sentiment and result generated one csv with date of publication,
    text of tweet, user, and sentiments
    :param name_file: name of csv to create
    :param name_user: name of timeline to extrac of tweet
    :param date: date start to create to the extract
    :param location: location for create la extract
    :param limit_twt: limte of twt to consult
    :param search_words: list of keyword to search in one timeline
    :param api: conecction with twitter
    """
    geocode = geolacalizacion_nombre(location)

    # Abre un archivo CSV para escribir los resultados
    name_csv = name_file+'.csv'
    with open(name_csv, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha', 'Tweet', 'Usuario', 'Sentimiento'])
        #print(geocode)
        # Recorre la timeline del usuario y escribe los tweets en el CSV
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=name_user, tweet_mode='extended',
                                   since_id=date, geocode=geocode).items(limit_twt):
            print(geocode)
            tweet_text = tweet.full_text
            if any(word in tweet.full_text for word in search_words):
                cleaned_text = re.sub(r'http\S+', '', tweet_text)
                cleaned_text = re.sub(r'RT.*', '', cleaned_text)
                cleaned_text = cleaned_text.strip()
                sentiment = TextBlob(cleaned_text).sentiment.polarity
                if sentiment > 0:
                    sentiment_label = 'Positivo'
                elif sentiment < 0:
                    sentiment_label = 'Negativo'
                else:
                    sentiment_label = 'Neutro'
                writer.writerow([tweet.created_at, cleaned_text, tweet.user.screen_name, sentiment_label])


if __name__ == '__main__':
    # Nombre de usuario del usuario a analizar
    user_name = 'elonmusk'
    # fechas a buscar
    date_since = "2000-01-01"
    # Palabras clave a buscar
    keywords = ['COVID-19', 'pandemia']
    #volumen de twets
    max_twets = 100
    #localidad a buscar en unradio de 1000km
    locations = 'Texas'
    #npmbre dle csv
    file = 'tweets'
    # Define las llaves y tokens de autenticación, sustituya las equis ('x') por sus llaves de conexión a la api
    consumer_key = 'xxxxxxxxxxxxxxxxx'
    consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    conect_twt = create_conect_twt(consumer_key, consumer_secret, access_token, access_token_secret)
    create_analytic_csv(file, user_name, date_since, locations, max_twets, keywords, conect_twt)