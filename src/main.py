import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from copy import copy


class TwitterService(object):

    def __init__(self):
        load_dotenv(find_dotenv())
        self.auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
            os.environ.get('CALLBACK_URL', 'http://localhost:5000/callback'),
        )
        self.users = {}  # TODO: mongodb

    def create_user(self, verifier, token):
        print(token)
        user_twitter_auth = copy(self.auth)
        self.auth.set_access_token = (
            token['oauth_token'],
            token['oauth_token_secret'],
        )
        user_twitter_auth.get_access_token(verifier)
        self.users[token['oauth_token']] = UserService(user_twitter_auth)

    def get_user(self, token):
        return self.users[token['oauth_token']]


class UserService(object):

    def __init__(self, user_twitter_auth):
        self.api = tweepy.API(user_twitter_auth)


def test_init():
    assert TwitterService().auth
