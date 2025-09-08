import os
from spotipy import Spotify
from flask import Flask, session, redirect, url_for, request, render_template
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from huggingface_hub import InferenceClient
from lyricsgenius import Genius

from clients.genius_api import get_lyrics, chunk_lyrics
from clients.hf_api import get_emotion_info
from clients.spotify_api import cache_handler, sp, sp_oauth
import config



# Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

# Spotify variables 
# sp_client_id = config.SP_CLIENT_ID
# sp_client_secret = config.SP_CLIENT_SECRET
# sp_redirect_uri = config.SP_REDIRECT_URI  # Handles refresh token
# cache_handler = FlaskSessionCacheHandler(session)
# scope = 'user-top-read'

# # Spotify Authorization Manager
# sp_oauth = SpotifyOAuth(
#     client_id=sp_client_id,
#     client_secret=sp_client_secret,
#     redirect_uri=sp_redirect_uri,
#     scope=scope,
#     cache_handler=cache_handler,
#     show_dialog=True    # Shows Spotify login request screen
#     )

# # Spotify API Client
# sp = Spotify(auth_manager=sp_oauth)


@app.route('/')
def index():
    session.clear()
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    return redirect(url_for('get_tracks'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_tracks'))


@app.route('/get_tracks')
def get_tracks():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    tracks = sp.current_user_top_tracks(limit=5)

    # Create dict of songs and artists using list comprehension
    track_info = {track['name']: track['artists'][0]['name'] for track in tracks['items']}
    # lyrics = get_lyrics(track_info[0][0], track_info[0][1])

    for song, artist in track_info.items():
        print(f'{song}: {artist}')
        lyrics = get_lyrics(song, artist)
        limited_lyrics = lyrics[:20]
        print(limited_lyrics)

    return render_template('index.html', track_info=track_info)


@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)