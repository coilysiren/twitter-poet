import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from copy import copy
from pymongo import MongoClient


load_dotenv(find_dotenv())


class TwitterService(object):

    def __init__(self):
        self.auth = self._create_auth()

    @property
    def db(self):
        return DatabaseSevice()

    @property
    def redirect_and_token(self):
        redirect = self.auth.get_authorization_url(signin_with_twitter=True)
        token = self.auth.request_token
        return redirect, token

    def _create_auth(self):
        return tweepy.OAuthHandler(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET'],
            os.environ.get('CALLBACK_URL', 'http://localhost:5000/callback'),
        )

    def get_admin(self):
        self.auth.set_access_token(
            os.environ['ACCESS_TOKEN'],
            os.environ['ACCESS_TOKEN_SECRET'],
        )
        return UserService(self.auth)

    def create_user(self, oauth_token, oauth_verifier):
        self.auth.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_verifier,
        }
        self.auth.get_access_token(oauth_verifier)
        self.db.create_user(
            oauth_token=oauth_token,
            access_token=self.auth.access_token,
            access_token_secret=self.auth.access_token_secret,
        )

    def get_user(self, oauth_token):
        try:
            user_data = self.db.get_user(
                oauth_token=oauth_token,
            )
            self.auth.set_access_token(
                user_data['access_token'],
                user_data['access_token_secret'],
            )
            return UserService(self.auth)
        except OutdatedCrendentialsException:
            self.db.delete_user(
                oauth_token=oauth_token,
            )
            return None
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

    def delete_user(self, **kwargs):
        return self.user_collection.remove(kwargs)


class OutdatedCrendentialsException(BaseException):
    pass


class UserService(object):

    def __init__(self, auth):
        self.api = tweepy.API(auth)
        try:
            self.api.verify_credentials()
        except tweepy.error.TweepError:
            raise OutdatedCrendentialsException

    def me(self):
        return self.api.me()


def test_placeholder():
    assert True
