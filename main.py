import requests
import urllib.parse
import os


from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, redirect, request, jsonify, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = 'http://localhost:5000/redirect'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
LOGIN_REDIRECT = '/login'

TOP_TRACK_LIST = []
TOP_ARTIST_LIST = []

REC_TRACK_LIST = []

@app.route('/')
def index():
    return f"Welcome to the App <a href={LOGIN_REDIRECT}>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True #remove later
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    
    return redirect(auth_url)

@app.route('/redirect')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/main')
    
@app.route('/main')
def main():
    return "<a href='/top'>Top Tracks and Artists</a>"

@app.route('/top')
def get_top():
    if 'access_token' not in session:
        return redirect(LOGIN_REDIRECT)
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/top/tracks?offset=0&limit=10&time_range=long_term', headers=headers)
    tracks = response.json()['items']
    
    TOP_TRACK_LIST.clear()
    result = ""
    for i, song in enumerate(tracks):
        result = result + f"{i+1}. {song['name']}<br>"
        TOP_TRACK_LIST.append(song['id'])
        
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/top/artists?offset=0&limit=10&time_range=long_term', headers=headers)
    artists = response.json()['items']
    
    TOP_ARTIST_LIST.clear()
    result += "<br><br><br>"

    for i, artist in enumerate(artists):
        result = result + f"{i+1}. {artist['name']}<br>"
        TOP_ARTIST_LIST.append(artist['id'])
    
    result += "<br><br>"
    result += "<a href='/recommended'>Get Recommendations</a>"
    
    return result

@app.route('/recommended')
def get_recommended():
    if 'access_token' not in session:
        return redirect(LOGIN_REDIRECT)
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + f"recommendations?limit=50&seed_artists={TOP_ARTIST_LIST[0]},{TOP_ARTIST_LIST[1]},{TOP_ARTIST_LIST[2]},{TOP_ARTIST_LIST[3]},{TOP_ARTIST_LIST[4]},", headers=headers)
    recs = response.json()['tracks']
    
    result = ""
    for i, track in enumerate(recs):
        result = result + f"{i+1}. {track['name']}<br>"
        REC_TRACK_LIST.append(track['uri'])
    
    result += "<br><br>"
    result += "<a href='/create-playlist'>Create a Playlist of These Songs!</a>"
    
    return result

@app.route('/create-playlist')
def create_playlist():
    if 'access_token' not in session:
        return redirect(LOGIN_REDIRECT)
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    user_info = requests.get(API_BASE_URL + 'me', headers=headers)
    userID = user_info.json()['id']
    
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}", 
        'Content-Type': 'application/json'
    }
    
    data = {'name': 'new-playlist', 'public': True}
    
    response = requests.post(API_BASE_URL + f"users/{userID}/playlists", headers=headers, json=data)
    
    if response.status_code != 201:
        return "Failed to create playlist"
    
    playlist_id = response.json()['id']
    
    data = {
        'uris': REC_TRACK_LIST
    }
    response = requests.post(API_BASE_URL + f"playlists/{playlist_id}/tracks", headers=headers, json=data)
    if response.status_code == 200:
        return "Playlist successfully created! Enjoy! :)"
    else:
        return "Playlist was not created. <a href='/login'>Click Here to Retry</a>"

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect({LOGIN_REDIRECT})
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token', 
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        
        session['refresh_token'] = new_token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
    return redirect('/main')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
