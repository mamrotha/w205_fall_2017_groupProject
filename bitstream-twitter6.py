#This code is for Python 2.7

import tweepy
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

consumer_key = 'IIW6zftvU8twvbJtudDWNGkCT'
consumer_secret = '9dwLpN4VgqiN8Wtc9Wg69MpRxPqo4yUV9b2yjosp9vpHC4qDjg'
access_token = '316687582-rhg8Ip0frp5LxjxNhqMRqckUxiuajNEJ9FrhXuj4'
access_token_secret = 'aJcqeEEisURA0tlhfBBDm5itHYKh0QCLoaNwIGBU5o2wY'

class MyStreamListener(tweepy.StreamListener):
    
    def __init__(self, max_responses):
        self.max_responses = max_responses
        self.num_responses = 0
        
    def on_data(self, data):
        if self.num_responses == self.max_responses:
            return False
        self.num_responses += 1
        
        json_data = json.loads(data)
        
#        print("\n\n")
#        print("================================================")
#        print("            ",self.num_responses)
#        print("================================================")
        #print(json.dumps(json_data, sort_keys= True, indent=4))
        
        if 'text' in json_data:
            #print("\nTweet:",json_data['text'])
            #print("\nCreated_at:",json_data['created_at'])
            #print("\nTimestamp_ms:",json_data['timestamp_ms'])
            #print("\nCoordinates:",json_data['coordinates'])
            #print("\nRetweet_count:",json_data['retweet_count'])
            #print("\nLang:",json_data['lang'])
            #print("\nUser_TimeZone:",json_data['user']['time_zone'])
            dataJson =json.loads(data[:-1])
            #print (dataJson)
            tweet = dataJson['text'].encode('utf8')
            created_at =dataJson['created_at']
            lang = dataJson['lang']
            coordinates =dataJson['coordinates']
            user_time_zone = dataJson['user']['time_zone']
            user_name = dataJson['user']['name'].encode('utf8')
            user_id = dataJson['user']['id']
            #print "Json",text,user_time_zone
            print "Json",tweet,created_at,lang,coordinates,user_time_zone
            conn = psycopg2.connect(database="crypto", user="postgres", password="crypto", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute("INSERT INTO tweets (tweet,created_at,lang,coordinates,user_time_zone,user_id,user_name) VALUES (%s,%s,%s,%s,%s,%s,%s)",(tweet, created_at,lang,coordinates,user_time_zone,user_id,user_name));
         
            conn.commit()
            conn.close()
      
    def on_error(self, status_code):
        print 'Error:', str(status_code)
        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print time.strftime("%Y%m%d_%H%M%S")
            print "A reconnection attempt will occur in " + \
            str(sleepy/60) + " minutes."
            print '''
            *******************************************************************
            From Twitter Streaming API Documentation
            420: Rate Limited
            The client has connected too frequently. For example, an 
            endpoint returns this status if:
            - A client makes too many login attempts in a short period 
              of time.
            - Too many copies of an application attempt to authenticate 
              with the same credentials.
            *******************************************************************
            '''
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print time.strftime("%Y%m%d_%H%M%S")
            print "A reconnection attempt will occur in " + \
            str(sleepy) + " seconds."
            time.sleep(sleepy)
            self.nightnight += 1
        return True        
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

my_stream_listener = MyStreamListener(2000)

my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listener, timeout=60, wait_on_rate_limit=True)
my_stream.filter(track=["bitcoin","btc"], async=True)
