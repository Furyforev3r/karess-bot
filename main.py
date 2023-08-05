import tweepy
import random
from random import choice
import time
from time import sleep
from lyrics_scrapping.lyrics import songs
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = tweepy.Client(bearer_token=os.environ.get("bearer_token"),
                       consumer_key=os.environ.get("consumer_key"),
                       consumer_secret=os.environ.get("consumer_secret"),
                       access_token=os.environ.get("access_token"),
                       access_token_secret=os.environ.get("access_token_secret")
                       )


while True:
    try:
        song = choice(songs)
        Lyrics = choice(songs["lyrics"])

        if len(Lyrics) > 0:
            tweet = client.create_tweet(text=f'- "{Lyrics}"\n\n{songs['track']['name']} - {songs['track']['artist']}!')
            print(tweet)
            sleep(7200)
    except Exception as e:
        print(f"An error occurred: {e}")
