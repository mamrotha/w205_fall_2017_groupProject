#Imports
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

#Start connection, analyzer, and engine
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')

#Get price and average sentiment dataframe
columns = ['hour','price','sent_avg']
sql = "SELECT created_at_hr, price_usd, avg(sentiment) as avg_sent \
FROM bitcoin_hr_adjust, tweet_sentiment \
WHERE created_at_hr = update_hour \
GROUP BY created_at_hr, price_usd \
ORDER BY created_at_hr ASC;"
cur.execute(sql)
df = pd.DataFrame(cur.fetchall())
df.columns = columns

#Created percent change columns
price_delta = [0.0]
for p in range(1,52):
    x_0 = float(df['price'][p-1])
    x_1 = float(df['price'][p])
    delta = (x_1-x_0)/x_0
    price_delta.append(delta)
df['price_change'] = price_delta

sent_delta = [0.0]
for p in range(1,52):
    x_0 = float(df['sent_avg'][p-1])
    x_1 = float(df['sent_avg'][p])
    delta = (x_1-x_0)/x_0
    sent_delta.append(delta)
df['sent_change'] = sent_delta

#Create betting strategy
coin = 500
cash = 500
for i in range(1,52):
    p = df['price_change'][i]
    s = df['sent_change'][i]
    coin = coin+coin*p
    cash_change = cash*s
    cash = cash+cash_change
    coin = coin+cash_change
