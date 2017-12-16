#Imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

#Connect to database and start analyzer
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
analyser = SentimentIntensityAnalyzer()

#Get appropriate twitter data
sql = "SELECT tweet, created_at \
       FROM tweets \
       WHERE lang = 'en';"
cur.execute(sql)

#Create dataframe of twitter data
data = cur.fetchall()
df = pd.DataFrame()
tweets = []
times = []
for i in range(len(data)): tweets.append(data[i][0])
df['tweet'] = np.asarray(tweets)
for i in range(len(data)): times.append(data[i][1])
df['created_at'] = np.asarray(times)

#Adjust for date and times
df['created_at'] =  pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')
df['date'] = [d.date() for d in df["created_at"]]
df['time'] = [d.time() for d in df["created_at"]]
df = df[["date", "time", "tweet"]]

#Create array of sentiment values and add to dataframe
sentiments = []
for tweet in df['tweet']:
    sent = analyser.polarity_scores(tweet).get('compound')
    sentiments.append(sent)
df['sentiment'] = np.asarray(sentiments)

#Send dataframe to new table
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')
df.to_sql("twitter_sentiment", engine, if_exists="append")