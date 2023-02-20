import tweepy
import pandas as pd
from textblob import TextBlob
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def connect_to_twitter_api(api_key: str, api_secret_key: str, access_token: str, access_token_secret: str):
    """
    Función que realiza la conexión a la API de Twitter.

    Args:
    api_key (str): clave de API de Twitter.
    api_secret_key (str): clave secreta de API de Twitter.
    access_token (str): token de acceso de Twitter.
    access_token_secret (str): token de acceso secreto de Twitter.

    Returns:
    Objeto tweepy.API: objeto API de Twitter autenticado.
    """
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    logging.info('Conexión a la API de Twitter establecida')
    return api


def extract_timeline(api: tweepy.API, screen_name: str, since_date: str, until_date: str, location: str, keyword: str):
    """
    Función que extrae el timeline de un usuario de Twitter, filtrado por fechas, ubicación y palabras clave.

    Args:
    api (tweepy.API): objeto API de Twitter autenticado.
    screen_name (str): nombre de usuario de Twitter del que se quiere extraer el timeline.
    since_date (str): fecha de inicio del rango de fechas en formato YYYY-MM-DD.
    until_date (str): fecha de fin del rango de fechas en formato YYYY-MM-DD.
    location (str): ubicación de los tweets que se quieren extraer.
    keyword (str): palabra clave a buscar en los tweets.

    Returns:
    lista de objetos Status: lista de tweets filtrados.
    """
    tweets = []
    logging.info("Preparando extracción de tweets")
    for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items():
        if (status.created_at.date() >= pd.to_datetime(since_date).date() and
            status.created_at.date() <= pd.to_datetime(until_date).date() or
            location.lower() in status.user.location.lower() and
            keyword.lower() in status.full_text.lower()):
            tweets.append(status)
    logging.info(f'Se han extraído {len(tweets)} tweets')
    return tweets


def analyze_sentiment(text: str):
    """
    Función que analiza el sentimiento de un texto usando TextBlob.

    Args:
    text (str): texto a analizar.

    Returns:
    float: polaridad del sentimiento del texto en el rango [-1, 1].
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity


def export_to_csv(tweets: list, output_file: str):
    """
    Función que exporta los tweets a un archivo CSV con las cabezeras correspondientes.

    Args:
    tweets (list): lista de tweets a exportar.
    output_file (str): ruta del archivo de salida.
    """
    data = [[tweet.created_at, tweet.user.screen_name, tweet.full_text, analyze_sentiment(tweet.full_text)] for tweet in tweets]
    df = pd.DataFrame(data, columns=['Fecha de publicación', 'Usuario', 'Texto', 'Sentimiento'])
    df.to_csv(output_file, index=False)
    logging.info(f'Los tweets se han exportado a {output_file}')


def main(api_key, api_secret_key, access_token, access_token_secret, screen_name, since_date, until_date, location, keyword, output_file):
    """
    Función principal que ejecuta el script completo.

    Args:
    api_key (str): clave de API de Twitter.
    api_secret_key (str): clave secreta de API de Twitter.
    access_token (str): token de acceso de Twitter.
    access_token_secret (str): token de acceso secreto de Twitter.
    screen_name (str): nombre de usuario de Twitter del que se quiere extraer el timeline.
    since_date (str): fecha de inicio del rango de fechas en formato YYYY-MM-DD.
    until_date (str): fecha de fin del rango de fechas en formato YYYY-MM-DD.
    location (str): ubicación de los tweets que se quieren extraer.
    keyword (str): palabra clave a buscar en los tweets.
    output_file (str): ruta del archivo de salida.
    """
    api = connect_to_twitter_api(api_key, api_secret_key, access_token, access_token_secret)
    tweets = extract_timeline(api, screen_name, since_date, until_date, location, keyword)
    export_to_csv(tweets, output_file)


if __name__ == '__main__':
    api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    api_secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    screen_name = 'elonmusk'
    since_date = '2000-01-01'
    until_date = '2023-03-30'
    location = 'California'
    keyword = 'space'
    output_file = 'tweets.csv'
    main(api_key, api_secret_key, access_token, access_token_secret, screen_name, since_date, until_date, location, keyword, output_file)
