import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from copy import copy
from pymongo import MongoClient


load_dotenv(find_dotenv())


class TwitterService(object):

    def __init__(self):
        self.auth = self.create_auth()

    @property
    def db(self):
        return DatabaseSevice()

    def create_auth(self):
        return tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
            os.environ.get('CALLBACK_URL', 'http://localhost:5000/callback'),
        )

    def get_admin(self):
        auth = self.create_auth()
        auth.set_access_token(
            os.environ['ACCESS_TOKEN'],
            os.environ['ACCESS_TOKEN_SECRET'],
        )
        return UserService(auth)

    def create_user(self, oauth_token, oauth_verifier):
        auth = self.create_auth()
        auth.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_verifier,
        }
        auth.get_access_token(oauth_verifier)
        self.db.create_user(
            oauth_token=oauth_token,
            access_token=auth.access_token,
            access_token_secret=auth.access_token_secret,
        )

    def get_user(self, oauth_token):
        try:
            user_data = self.db.get_user(
                oauth_token=oauth_token,
            )
            auth = self.create_auth()
            auth.set_access_token(
                user_data['access_token'],
                user_data['access_token_secret'],
            )
            return UserService(auth)
        except TypeError:
            return None


class DatabaseSevice(object):

    def __init__(self):
        client = MongoClient(os.environ['MONGODB_URI'])
        self.user_collection = client.get_default_database()['users']

    def create_user(self, **kwargs):
        return self.user_collection.insert_one(kwargs)

    def get_user(self, **kwargs):
        return self.user_collection.find_one(kwargs)


class UserService(object):

    def __init__(self, auth):
        self.api = tweepy.API(auth)

    def me(self):
        return self.api.me()
