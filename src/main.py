import tweepy
import os
from dotenv import load_dotenv, find_dotenv


class TwitterHandler(object):

    def __init__(self):
        load_dotenv(find_dotenv())
        self.auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
        )


def test_init():
    assert TwitterHandler().auth
