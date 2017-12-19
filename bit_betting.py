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
sql = "SELECT * FROM avg_sentiment;"
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
coin = 500.00
cash = 500.00
time = df['hour'][0]
print time,'Cash:',cash,'Bitcoin:',coin,'Total: 1000.00'

for i in range(1,52):
    p = df['price_change'][i]
    s = df['sent_change'][i]
    time = df['hour'][i]
    if s>0:
        change = cash*s
        cash = cash-change
        coin = coin+(coin*p)+change
    elif s<0:
        change = coin*s
        cash = cash-change
        coin = coin+(coin*p)+change
    tot = cash+coin
    print time,'Cash: %.2f Bitcoin: %.2f,'Total: %.2f' % (cash,coin,tot)

price_0 = float(df['price'][0])
price_f = float(df['price'][51])
tot_price_change = (price_f-price_0)/price_0
total_bitcoin = 1000.00+1000.00*tot_price_change
print 'Bitcoin benchmark:', total_bitcoin

