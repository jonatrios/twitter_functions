# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 11:41:13 2021

@author: Jonathan
"""
from twitter_keys import  api_key, api_secret_key, access_token, access_token_secret
import tweepy
import json
from datetime import datetime
from dateutil import tz



auth = tweepy.OAuthHandler(api_key, api_secret_key)

auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)




def user_timeline(username,n):
    twet_list = []
    for t in tweepy.Cursor(api.user_timeline, screen_name=username,
                           tweet_mode='extended').items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        twet_list.append(json.loads(t_json,object_hook=date_hook)) #
    return twet_list

def tweet_seacrh(keyword,n):
    search_list = []
    for t in tweepy.Cursor(api.search, q=keyword,lang='es',
                           tweet_mode='extended').items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        search_list.append(json.loads(t_json,object_hook=date_hook)) #
    return search_list

def historical_search(keyword,from_date,n):
    from_date = datetime.strptime(from_date,'%d/%m/%Y %H:%M')
    from_date = datetime.strftime(from_date,'%Y%m%d%H%M')
    h_list = []
    for t in tweepy.Cursor(api.search_full_archive,environment_name='learning', query=keyword,fromDate=from_date).items(n): #numero de tweets a traer
        t_json = json.dumps(t._json)
        h_list.append(json.loads(t_json,object_hook=date_hook)) #
    return h_list


#helper functions
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


def str_to_datestr(string):
    str_format_date = '%a %b %d %H:%M:%S +0000 %Y'
    try:
        d = datetime.strptime(string,str_format_date)
        d = datetime.strftime(d,'%d/%m/%Y %H:%M:%S')
        return d
    except ValueError:
        return string
    



