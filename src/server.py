from flask import Flask, url_for, redirect, render_template, session, request
from .main import TwitterService


app = Flask(__name__)
twitter = TwitterService("/callback")


@app.route("/")
def index():
    redirect_url = twitter.auth.get_authorization_url()
    session.set('request_token', twitter.auth.request_token)
    return redirect(redirect_url)


@app.route("/callback")
def callback():
    twitter.create_user(
        verifier=request.GET.get('oauth_verifier'),
        token=session['request_token'],
    )
    return redirect(url_for('start'))


@app.route("/start")
def start():
    user = twitter.get_user(session['request_token'])
    return render_template('result.html', content=user.api.user_timeline())
