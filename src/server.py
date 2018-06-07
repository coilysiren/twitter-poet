from flask import Flask, url_for, redirect, render_template, session, request
from .main import TwitterService
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['CONSUMER_KEY']
twitter = TwitterService()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/start")
def start():
    redirect_url = twitter.auth.get_authorization_url()
    session['request_token'] = twitter.auth.request_token
    return redirect(redirect_url)


@app.route("/callback")
def callback():
    twitter.create_user(
        verifier=request.args.get('oauth_verifier'),
        token=session['request_token'],
    )
    return redirect(url_for('results'))


@app.route("/results")
def results():
    user = twitter.get_user(session['request_token'])
    return render_template('result.html', content=user.api.user_timeline())
