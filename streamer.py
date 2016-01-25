from __future__ import unicode_literals
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy, datetime, signal, sys, json, psycopg2

# Variables that contains the user credentials to access Twitter API
access_token = "4010739394-F156dCIH53L1pfstMxF7PlqkmfDJEZJScb0qGAv"
access_token_secret = "7ZynMAw4hsnmyFfifGl9z8omFKqBRDbCcbhO1rgiqQW51"
consumer_key = "NhwzdxzKaBRemgIpnnuZFmyNd"
consumer_secret = "EB6OJaK5IGbfXPjMKsk1nRY9GxdgHuEsGZDAKVh0VJubp9iSFO"

trump_id = '25073877'
hilary_id = '1339835893'
sanders_id = '216776631'
bush_id = '113047940'
cruz_id = '23022687'
carson_id = '1180379185'
christie_id = '1347285918'
rubio_id = '15745368'

conn = psycopg2.connect("dbname=tweet_stream user=jghibiki password=123abc")
cur = conn.cursor()

# Abbeviations
# CT: candidate thought
# OT: original thought (post by non candidate)
# RT: retweet

class StreamListener(tweepy.StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, _data):
        data = json.loads(_data)
        if "delete" not in data:
            if ( "retweeted_status" not in data and
                  ( data["user"]["id_str"] == trump_id or
                    data["user"]["id_str"] == hilary_id or
                    data["user"]["id_str"] == sanders_id or
                    data["user"]["id_str"] == bush_id or
                    data["user"]["id_str"] == cruz_id or
                    data["user"]["id_str"] == carson_id or
                    data["user"]["id_str"] == christie_id or
                    data["user"]["id_str"] == rubio_id)):

                print("CT: %s" % data["text"])

                query = """INSERT INTO candidate_tweets (
                        user_name,
                        user_id,
                        created_date,
                        tweet
                    ) VALUES(%s, %s, %s, %s);"""

                query_data = (
                    data["user"]["name"],
                    data["user"]["id_str"],
                    datetime.datetime.utcnow(),
                    data["text"]
                )

                cur.execute(query, query_data)
            elif "retweeted_status" not in data:
                print("OT: %s" % data["text"])

                query = """INSERT INTO tweets (
                        user_name,
                        user_id,
                        created_date,
                        tweet
                    ) VALUES(%s, %s, %s, %s);"""

                query_data = (
                    data["user"]["name"],
                    data["user"]["id_str"],
                    datetime.datetime.utcnow(),
                    data["text"]
                )

            elif "retweeted_status" in data:

                print("RT: %s" % data["text"])

                query = """INSERT INTO retweets (
                        user_name,
                        user_id,
                        created_date,
                        tweet,
                        original_tweet,
                        original_user_name,
                        original_user_id
                    ) VALUES(%s, %s, %s, %s, %s, %s, %s);"""

                query_data = (
                    data["user"]["name"],
                    data["user"]["id_str"],
                    datetime.datetime.utcnow(),
                    data["text"],
                    data["retweeted_status"]["text"],
                    data["retweeted_status"]["user"]["name"],
                    data["retweeted_status"]["user"]["id_str"]
                )


        return True

    def on_error(self, status):
        print(status)


def GracefulExit(_signal, frame):
    if _signal is signal.SIGINT:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == '__main__':
    # set up exit handler
    signal.signal(signal.SIGINT, GracefulExit)

    # This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    print("Starting Stream...")
    #while(True):
    #    try:
    stream.filter(follow=[trump_id, hilary_id, sanders_id, bush_id, cruz_id, carson_id, christie_id, rubio_id], async=False)
    #    except Exception:
    #        print(e)
