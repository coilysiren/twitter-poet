import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from copy import copy


class TwitterService(object):

    def __init__(self, oauth_callback_path):
        load_dotenv(find_dotenv())
        self.auth = tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
            oauth_callback_path
        )
        self.users = {}  # TODO: mongodb

    def create_user(self, verifier, token):
        user_twitter_auth = copy(self.auth)
        user_twitter_auth.set_request_token(token[0], token[1])
        user_twitter_auth.get_access_token(verifier)
        self.users[token] = UserService(user_twitter_auth)

    def get_user(self, token):
        return self.users[token]


class UserService(object):

    def __init__(self, user_twitter_auth):
        self.api = tweepy.API(user_twitter_auth)


def test_init():
    assert TwitterService('').auth
