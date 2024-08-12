from flask import redirect, request, session, jsonify, render_template
from datetime import datetime
import spotify
import requests
import urllib.parse


def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')  

    @app.route('/login')
    def login():
        scope = 'user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private'
        params = {
            'client_id': app.config['CLIENT_ID'],
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': app.config['REDIRECT_URI'],
            'show_dialog': True
        }
        auth_url = f"{spotify.AUTH_URL}?{urllib.parse.urlencode(params)}"
        return redirect(auth_url)

    @app.route('/redirect')
    def callback():
        if 'error' in request.args:
            return jsonify({"error": request.args['error']})
        
        code = request.args.get('code')
        if code:
            token_info = spotify.get_token(app.config['CLIENT_ID'], app.config['CLIENT_SECRET'], code, app.config['REDIRECT_URI'])
            session['access_token'] = token_info['access_token']
            session['refresh_token'] = token_info['refresh_token']
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
            return redirect('/main')
        return 'Error: Authorization failed.'

    @app.route('/main')
    def main():
        return render_template('main.html')  

    @app.route('/top')
    def get_top():
        access_token = session.get('access_token')
        if not access_token:
            return redirect('/login')
        
        top_tracks = spotify.get_top_tracks(access_token)
        top_artists = spotify.get_top_artists(access_token)
        
        session['top_artists'] = top_artists
        
        return render_template('top_tracks_and_artists.html', tracks=top_tracks, artists=top_artists)

    @app.route('/recommended')
    def get_recommended():
        access_token = session.get('access_token')
        if not access_token:
            return redirect('/login')
        
        top_artists = session['top_artists']
        seed_artists = [artist['id'] for artist in top_artists[:5]]
        recommendations = spotify.get_recommendations(access_token, seed_artists)
        
        session['recommendations'] = [track['uri'] for track in recommendations]
        
        
        return render_template('recommendations.html', recommendations=recommendations)

    @app.route('/create-playlist')
    def create_playlist():
        access_token = session.get('access_token')
        if not access_token:
            return redirect('/login')
        
        user_profile = spotify.get_user_profile(access_token)
        playlist = spotify.create_playlist(access_token, user_profile['id'], 'My Recommendations Playlist')
        if 'id' in playlist:
            playlist_id = playlist['id']
            track_uris = session['recommendations']
            success = spotify.add_tracks_to_playlist(access_token, playlist_id, track_uris)
            
            if success:
                return render_template('playlist_created.html', playlist_link = playlist['external_urls']['spotify'])
            else:
                return "There was an error "
        return "Failed to create playlist."

    @app.route('/refresh-token')
    def refresh_token():
        refresh_token = session.get('refresh_token')
        if not refresh_token:
            return redirect('/login')

        token_info = spotify.refresh_token(app.config['CLIENT_ID'], app.config['CLIENT_SECRET'], refresh_token)
        session['access_token'] = token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/main')

    # Additional routes like '/refresh-token' can be added similarly
