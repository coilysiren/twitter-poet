from flask import Flask, url_for, redirect, render_template, session, request
from .main import TwitterService
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/start")
def start():
    twitter = TwitterService()

    if not session.get('request_token'):
        redirect_url = twitter.auth.get_authorization_url()
        session['request_token'] = twitter.auth.request_token

    print('session ' + str(session))
    print('oauth_token ' + session['request_token']['oauth_token'])

    if twitter.get_user(session['request_token']['oauth_token']):
        return redirect(url_for('results'))
    else:
        return redirect(redirect_url)


@app.route("/callback")
def callback():
    twitter = TwitterService()
    twitter.create_user(
        oauth_token=request.args.get('oauth_token'),
        oauth_verifier=request.args.get('oauth_verifier'),
    )
    return redirect(url_for('results'))


@app.route("/results")
def results():
    twitter = TwitterService()
    if session.get('request_token'):
        user = twitter.get_user(session['request_token']['oauth_token'])
        return render_template('result.html', content=user.me())
    else:
        return redirect(url_for('start'))
