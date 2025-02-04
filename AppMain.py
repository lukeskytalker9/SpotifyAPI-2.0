from flask import Flask, request, redirect, session

from spotipy.oauth2 import SpotifyOAuth
from datetime import timedelta

from User import User


app = Flask(__name__)
app.secret_key = ''
app.permanent_session_lifetime = timedelta(days=30)

# Spotify API credentials
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""  # This should be set up in your Spotify Developer Dashboard

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read playlist-modify-public user-top-read')


class Website:

    @classmethod
    def getToken(cls):
        return session['token_info']['access_token']
    
    @classmethod
    def isTokenValid(cls):
        return



@app.route('/')
def home():
    return "Home Page"

@app.route('/dashboard')
def dashboard():
    return "Dashboard"


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info #______________________________________This max not be appropriete
    
    #This should confirm it was not just randomly called
    #Add token to session
    #Add user to database if not already there
        #Pull user data from Spotify
    #Redirect to dashboard
    
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/get_user_data')
def getUserData():

    user = User(session['token_info']) 

    return user.getUserData()   

@app.route('/update_database')
def updateDatabase():
    user = User(session['token_info'])
    user.updateData()
    return "Don!"



if __name__ == '__main__':
    app.run()