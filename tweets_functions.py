# -*- coding: utf-8 -*-

from twitter_keys import  api_key, api_secret_key, access_token, access_token_secret,env_name
import tweepy
import json
from datetime import datetime
from dateutil import tz


# Establecer la conexion con Twitter mediante tweepy
auth = tweepy.OAuthHandler(api_key, api_secret_key)

auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)



# Trae tweets desde el time-line del usuario a traves del screen_name indicado
def user_timeline(username,n):
    twet_list = []
    for t in tweepy.Cursor(api.user_timeline, screen_name=username, count=100,
                           tweet_mode='extended').items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        twet_list.append(json.loads(t_json,object_hook=date_hook))
    return twet_list


# Busca por palabra clave segun lenguaje indicado
def tweet_seacrh(keyword,n,lan='en'):
    search_list = []
    for t in tweepy.Cursor(api.search, q=keyword,lang=lan,
                           tweet_mode='extended').items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        search_list.append(json.loads(t_json,object_hook=date_hook))
    return search_list

# Trae tweets desde una fecha mendionada segun palabra clave
def historical_search(keyword,from_date,n):
    from_date = datetime.strptime(from_date,'%d/%m/%Y %H:%M')
    from_date = datetime.strftime(from_date,'%Y%m%d%H%M')
    h_list = []
    for t in tweepy.Cursor(api.search_full_archive,environment_name=env_name, query=keyword,fromDate=from_date).items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        h_list.append(json.loads(t_json,object_hook=date_hook))
    return h_list


#helper function para manejar las fechas, castea a uso horario Argentina
def date_hook(json_dict):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Buenos_Aires')
    str_format_date = '%a %b %d %H:%M:%S +0000 %Y'
    for (key, value) in json_dict.items():
        try:
            d = datetime.strptime(value, str_format_date)
            d = d.replace(tzinfo=from_zone)
            d = d.astimezone(to_zone)
            json_dict[key] = datetime.strftime(d,'%d/%m/%Y %H:%M:%S')
        except:
            pass
    return json_dict




