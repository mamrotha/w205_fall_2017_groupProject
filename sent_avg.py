#Imports
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

#Start connection, analyzer, and engine
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
engine = create_engine('postgresql+psycopg2://postgres:foobar@localhost:5432/crypto')