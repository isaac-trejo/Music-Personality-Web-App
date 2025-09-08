from flask import session
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from spotipy import Spotify

from config import SP_CLIENT_ID, SP_CLIENT_SECRET, SP_REDIRECT_URI

# Spotify variables 
sp_client_id = SP_CLIENT_ID
sp_client_secret = SP_CLIENT_SECRET
sp_redirect_uri = SP_REDIRECT_URI  # Handles refresh token
cache_handler = FlaskSessionCacheHandler(session)
scope = 'user-top-read'     # Allowed information from user

# Spotify Authorization Manager
sp_oauth = SpotifyOAuth(
    client_id=sp_client_id,
    client_secret=sp_client_secret,
    redirect_uri=sp_redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True    # Shows Spotify login request screen
    )

# Spotify API Client
sp = Spotify(auth_manager=sp_oauth)