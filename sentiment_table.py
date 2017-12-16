#Imports
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#Connect to database and start analyzer
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
analyser = SentimentIntensityAnalyzer()

#Get appropriate twitter data
sql1 = "SELECT tweet, created_at FROM tweets;"
cur.execute(sql1)

#Create dataframe of twitter data
data = curs.fetchall()
colNames = data[0].keys()
df = pd.DataFrame([[row[col] for col in colNames] for row in data], columns=colNames)

#Create array of sentiment values and add to dataframe
sentiments = []
for tweet in data:
    sent = analyser.polarity_scores(tweet[0]).get('compound')
    sentiments.append(sent)

df['sentiment'] = sentiments

#Send dataframe to new table
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')
df.to_sql("twitter_sentiment", engine, if_exists="append")