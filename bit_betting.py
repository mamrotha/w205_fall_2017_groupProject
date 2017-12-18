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
columns = ['hour','price','sent_avg, ']
sql = "SELECT created_at_hr, price_usd, avg(sentiment) as avg_sent \
FROM bitcoin_hr_adjust, tweet_sentiment \
WHERE created_at_hr = update_hour \
GROUP BY created_at_hr, price_usd \
ORDER BY created_at_hr ASC;"
cur.execute(sql)
df = pd.DataFrame(cur.fetchall())
df.columns = columns

#