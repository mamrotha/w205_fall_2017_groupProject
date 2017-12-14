import requests
import pandas as pd
import numpy as np
import datetime as dt
import psycopg2
import warnings
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")

r = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
ticker = pd.DataFrame(r.json())
ticker['last_updated'] = pd.to_datetime(ticker['last_updated'],unit='s')
ticker['date'] = [d.date() for d in ticker["last_updated"]]
ticker['time'] = [d.time() for d in ticker["last_updated"]]
ticker = ticker[["date", "time", "id", "symbol", "price_usd", "available_supply", "total_supply"]]

engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')
ticker.to_sql("ticker", engine, if_exists="append")

print("ticker_data updated")
