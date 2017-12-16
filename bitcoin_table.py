#Imports
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

#Connect to database and create engine
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')

#Create dataframe of bitcoin data
sql = "SELECT date, time, price_usd \
       FROM ticker \
       WHERE id = 'bitcoin';"
df = pd.read_sql_query(sql, engine)

#Get last hours of tweet sentiments


#Average the values and add to the df


#Send dataframe to new table
df.to_sql("bitcoin", engine, if_exists="append")