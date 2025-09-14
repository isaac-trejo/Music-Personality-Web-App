import os
from flask import Flask, session, redirect, url_for, request, render_template

from clients.genius_api import get_lyrics, chunk_lyrics
from clients.hf_api import lyric_emotion_info
from clients.spotify_api import cache_handler, sp, sp_oauth
from services.emotion_logic import normalize_emotions_percent


# Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    session.clear()
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    return redirect(url_for('get_tracks'))

@app.route('/callback')
def callback():
    if request.args.get('code'):
        token_info = sp_oauth.get_access_token(request.args['code'])
        if token_info:
            session['token_info'] = token_info
            return redirect(url_for('get_tracks'))

    return redirect(url_for('index'))


@app.route('/get_tracks')
def get_tracks():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        session.pop('token_info', None)
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    try:
        tracks = sp.current_user_top_tracks(limit=5)
        track_info = [(track['name'], track['artists'][0]['name']) for track in tracks['items']]
        session['track_info'] = track_info
        return render_template('index.html', track_info=track_info)
    except Exception as e:
        print(f"Error fetching tracks: {str(e)}")
        session.clear()
        return redirect(url_for('index'))


@app.route('/emotion_info')
def emotion_info():
    if 'track_info' not in session:
        return redirect(url_for('get_tracks'))

    track_info = session['track_info']

    return "Emotion info page"


if __name__ == '__main__':
    app.run(debug=True)