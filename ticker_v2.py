import requests
import pandas as pd
import numpy as np
import datetime as dt
import psycopg2

#Connect to the database and create cursor
conn = psycopg2.connect(database="crypto", user="postgres",           host="localhost", port="5432")
cur = conn.cursor()

#Grab data from coindesk API and create pandas df
r = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
ticker = pd.DataFrame(r.json())
ticker['last_updated'] = pd.to_datetime(ticker['last_updated'],unit='s')
ticker['date'] = [d.date() for d in ticker["last_updated"]]
ticker['time'] = [d.time() for d in ticker["last_updated"]]
ticker = ticker[["date", "time", "id", "symbol", "price_usd", "available_supply", "total_supply"]]

#Insert data into appropriate table
cur.execute("INSERT INTO ticker (date, time, id, symbol, price_usd, 	available_supply, total_supply) VALUES (%s,%s,%s,%s,%s,%s,%s,)", 		(date, time, id, symbol, price_usd, available_supply, 	total_supply,))

conn.commit()
conn.close()