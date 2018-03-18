#Imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine
from tzlocal import get_localzone

#Start connection, analyzer, and engine
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
analyser = SentimentIntensityAnalyzer()
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')

#Get tweet dataframe
columns = ['created_at_hr','tweet']
sql = "SELECT created_at_hour, tweet \
       FROM tweets_hr_adjust \
       WHERE lang = 'en' AND \
       created_at_hour between '12/11/2017' and '12/12/2017';"
cur.execute(sql)
df = pd.DataFrame(cur.fetchall())
df.columns = columns
df['created_at_hr'] = pd.to_datetime(df['created_at_hr'], format='%Y-%m-%d %H:%M:%S+00:00')
df['created_at_hr'] = df['created_at_hr'].dt.tz_convert('UTC').dt.tz_localize(None)

#Rename columns
sentiments = []
for tweet in df['tweet']:
    sent = analyser.polarity_scores(tweet).get('compound')
    sentiments.append(sent)
df['sentiment'] = np.asarray(sentiments)

#Send dataframe to new table
df.to_sql("tweet_sentiment", engine, if_exists="append")