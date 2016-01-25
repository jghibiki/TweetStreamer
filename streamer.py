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

conn = psycopg2.connect("dbname=tweet_stream user=jghibiki password=123abc")
cur = conn.cursor()


class StreamListener(tweepy.StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, _data):
        data = json.loads(_data)
        if ("delete" not in data and
                "retweeted_status" not in data and
                ( data["user"]["id_str"] == trump_id or
                  data["user"]["id_str"] == hilary_id)):
            print(data["text"])
            cur.execute("INSERT INTO tweets (created_date, tweet) VALUES(%s, %s);",
                (datetime.datetime.utcnow(), data["text"]))

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
    stream.filter(follow=[trump_id, hilary_id], async=False)
    #    except Exception:
    #        print(e)
