#Sample code snippets for working with psycopg


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

#Create the Database

try:
    # CREATE DATABASE can't run inside a transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE crypto")
    cur.close()
    conn.close()
except:
    print "Could not create crypto"

#Connecting to tcount

conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")

#Create a Tables

#Create table for twitter data
cur = conn.cursor()
cur.execute('''CREATE TABLE tweets
       (tweet TEXT          NOT NULL,
        created_at TEXT     NOT NULL,
        lang TEXT           NOT NULL,
        coordinates TEXT,      
        user_time_zone TEXT,
        user_id TEXT,
        user_name TEXT);''')
conn.commit()

#Create table for ticker data
cur = conn.cursor()
cur.execute('''CREATE TABLE ticker
       (date DATE                NOT NULL, 
        time TIME                NOT NULL,
        id TEXT                  NOT NULL,
        symbol TEXT              NOT NULL,
        price_usd INT            NOT NULL,
        available_supply INT     NOT NULL,
        total_supply INT     NOT NULL);''')
conn.commit()

conn.close()
