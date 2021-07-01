# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 19:18:24 2021

@author: Lucia Zabaleta
"""
from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import numpy as np
from tweets_profile import tweet_seacrh
import re
import string

pos = twitter_samples.strings('positive_tweets.json')

neg = twitter_samples.strings('negative_tweets.json')
    

def tweet_cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet).strip() #Remove user
    tweet = re.sub(r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*|\/+", "", tweet) #Remove links
    tweet = re.sub(r"(\w)\1+", r"\1\1",tweet) #Normalize words that has repeated letters
    tweet = re.sub(r"\d+:\d+\s?","",tweet) #Remove hours
    tweet = tweet.replace('\n', ' ').replace('#','').replace('_','') #Remove hashtag but keep the text and remove newlines
    tweet = " ".join(tweet.split())
    return tweet

# Tokenize to 
def tweet_tokenizer(clean_tweet,lang='english'):
    ttk = TweetTokenizer()
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticones
        u"\U0001F300-\U0001F5FF"  # simbolos
        u"\U0001F680-\U0001F6FF"  # transporte & simbolos de mapas
        u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
        u"\U0001F1F2-\U0001F1F4"  # bandera de Macau
        u"\U0001F1E6-\U0001F1FF"  # banderas
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    clean_tweet = emoji_pattern.sub(r'', clean_tweet)
    clean_tweet = re.sub("[¿¡.-]+", "", clean_tweet)
    sw = stopwords.words(lang)
    r = ttk.tokenize(clean_tweet)
    a = [w.lower() for w in r if w not in string.punctuation]
    b = [x for x in a if x not in sw and x.isalpha() == True and len(x) >= 2]
    return b
 
    
pos_clean = list(map(tweet_cleaner,pos))

neg_clean = list(map(tweet_cleaner,neg))

pos_label = list(map(lambda x : [x, 'pos'],pos_clean))
neg_label = list(map(lambda x : [x, 'neg'],neg_clean)) 

full_data = np.array(pos_label + neg_label)
   
np.random.shuffle(full_data)

vectorizer = CountVectorizer(analyzer=tweet_tokenizer)

all_features = vectorizer.fit(full_data[:,0])

features_t = all_features.transform(full_data[:,0])

tfidf_features = TfidfTransformer().fit(features_t)

tfidf_t = tfidf_features.transform(features_t)

X_train, X_test, y_train, y_test = train_test_split(tfidf_t, full_data[:,1],test_size=0.3,random_state=42)

# First Model
cl = MultinomialNB()

cl.fit(X_train,y_train)

cl.score(X_test, y_test)

# Second Model
svm_cl = SVC(kernel='linear',probability=True)

svm_cl.fit(X_train,y_train)

svm_cl.score(X_test, y_test)


# Prediction test for new  non seen elements
text_list = np.array(['this product is really very good!',
             'i dont like it at all :(',
             'You are so nice :)', 
             'La verdad me parece bien que se haga justicia',
             'Ese queso es horrible',
             'Love youuuuu!!!'])


text_matrix = vectorizer.transform(text_list)

cl.predict(text_matrix)


# gr = list(map(lambda x : tweet_tokenizer(x,lang='english'),gt))
# gr = list(map(lambda x : [x, 'pos'],gr))
# full = np.array(gr)
# spanish_text = [tweet_cleaner(elem['retweeted_status']['full_text'])  if elem['full_text'].startswith('RT') else tweet_cleaner(elem['full_text']) for elem in spanish_list]
# pos_tokenize = list(map(lambda x : tweet_tokenizer(x,lang='english'),pos_clean))
# neg_tokenize = list(map(lambda x : tweet_tokenizer(x,lang='english'),neg_clean))

