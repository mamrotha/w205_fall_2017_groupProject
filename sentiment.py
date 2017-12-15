from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import psycopg2

#Connect to postgres database and start analyzer
conn = psycopg2.connect(database="crypto", user="postgres", password="pass", host="localhost", port="5432")
cur = conn.cursor()
analyser = SentimentIntensityAnalyzer()

#Alter table and add sentiment values as column
cur.execute("ALTER TABLE tweets ADD COLUMN IF NOT EXISTS sentiment                   decimal")
conn.commit()

#Get data from postgres
cur.execute("""SELECT tweet FROM tweets""")
feed = cur.fetchall()

#Create array of sentiment values
sentiments = []
for tweet in feed:
    sent = analyser.polarity_scores(tweet[0]).get('compound')
    sentiments.append(sent)

#Insert the sentiments to new column and commit
for sent in sentiments:
    cur.execute("INSERT INTO tweets(sentiment) VALUES (%s)", (sent,))
conn.commit()

#Close connection
conn.close()