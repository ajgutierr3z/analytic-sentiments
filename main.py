import tweepy
import pandas as pd
from textblob import TextBlob
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(
    stream=sys.stdout,
    datefmt='%Y-%m-%d %H:%M',
    format='%(asctime)s | %(levelname)s | %(message)s'
)


def connect_to_twitter_api(api_key: str, api_secret_key: str, access_token: str, access_token_secret: str,
                           logger: logging.Logger):
    """
    Función que realiza la conexión a la API de Twitter.
    :param api_key: clave de API de Twitter.
    :param api_secret_key: clave secreta de API de Twitter.
    :param access_token: token de acceso de Twitter.
    :param access_token_secret: token de acceso secreto de Twitter.
    :param logger: mensajes de estado
    :API
    """
    logger.info("Creando conexión")
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    logger.info('Conexión a la API de Twitter establecida')
    return api


def extract_timeline(api: tweepy.API, screen_name: str, since_date: str, until_date: str, location: str,
                     keyword: str, logger: logging.Logger):
    """
    Función que extrae el timeline de un usuario de Twitter, filtrado por fechas, ubicación y palabras clave.
    :param api (tweepy.API): objeto API de Twitter autenticado.
    :param screen_name (str): nombre de usuario de Twitter del que se quiere extraer el timeline.
    :param since_date (str): fecha de inicio del rango de fechas en formato YYYY-MM-DD.
    :param until_date (str): fecha de fin del rango de fechas en formato YYYY-MM-DD.
    :param location (str): ubicación de los tweets que se quieren extraer.
    :para keyword (str): palabra clave a buscar en los tweets.
    :param logger: mensaje de estado
    :tweets
    """
    tweets = []
    logger.info("Preparando extracción de tweets")
    for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items():
        if (status.created_at.date() >= pd.to_datetime(since_date).date() and
            status.created_at.date() <= pd.to_datetime(until_date).date() or
            location.lower() in status.user.location.lower() and
            keyword.lower() in status.full_text.lower()):
            tweets.append(status)
    logger.info(f'Se han extraído {len(tweets)} tweets')
    return tweets


def analyze_sentiment(text: str):
    """
    Función que analiza el sentimiento de un texto usando TextBlob.
    :param text : texto a analizar.
    :blob.sentiment.popolarity
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity


def export_to_csv(tweets: list, output_file: str, logger: logging.Logger):
    """
    Función que exporta los tweets a un archivo CSV con las cabezeras correspondientes.
    :param tweets: lista de tweets a exportar.
    :param logger: mensaje de estado
    """
    logger.info('Preparnado creación de fichero csv')
    data = [[tweet.created_at, tweet.user.screen_name, tweet.full_text, analyze_sentiment(tweet.full_text),
             f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'] for tweet in tweets]
    df = pd.DataFrame(data, columns=['Fecha de publicación', 'Usuario', 'Texto', 'Sentimiento', 'URL'])
    df.to_csv(output_file, index=False)
    logging.info(f'Los tweets se han exportado a {output_file}')


def main(api_key, api_secret_key, access_token, access_token_secret, screen_name, since_date, until_date, location,
         keyword, output_file, logger):
    """
    Función principal que ejecuta el script completo.
    :param api_key: clave de API de Twitter.
    :param api_secret_key: clave secreta de API de Twitter.
    :param access_token: token de acceso de Twitter.
    :parma access_token_secret: token de acceso secreto de Twitter.
    :param screen_name: nombre de usuario de Twitter del que se quiere extraer el timeline.
    :param since_date: fecha de inicio del rango de fechas en formato YYYY-MM-DD.
    :param until_date: fecha de fin del rango de fechas en formato YYYY-MM-DD.
    :param location: ubicación de los tweets que se quieren extraer.
    :param keyword: palabra clave a buscar en los tweets.
    """
    logger.info('Iniciando tarea')
    api = connect_to_twitter_api(api_key, api_secret_key, access_token, access_token_secret, logger)
    tweets = extract_timeline(api, screen_name, since_date, until_date, location, keyword, logger)
    export_to_csv(tweets, output_file, logger)
    logger.info('finalizado tarea')


if __name__ == '__main__':
    api_key = 'TU_API_KEY_CODIGO'
    api_secret_key = 'TU_CODIGO_SECRETO'
    access_token = 'ACCESS_TOKEN'
    access_token_secret = 'SECRET_ACCESS_TOKEN'
    screen_name = '@user'
    since_date = 'aaaa-mm-dd'
    until_date = 'aaaa-mm-dd'
    location = 'Lugar'
    keyword = 'palabraClave',
    output_file = 'tweets.csv'
    main(api_key, api_secret_key, access_token, access_token_secret, screen_name, since_date, until_date,
         location, keyword, output_file, logger)
