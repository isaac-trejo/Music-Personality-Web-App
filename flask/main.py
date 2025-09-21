import os
from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS

from clients.genius_api import get_lyrics, chunk_lyrics
from clients.hf_api import lyric_emotion_info
from clients.spotify_api import cache_handler, sp, sp_oauth
from services.emotion_logic import normalize_emotions_percent


# Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

# Enable CORS for React frontend
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"], supports_credentials=True)


@app.route('/api/logout')
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

@app.route('/api/auth/login')
def login():
    """Initiate Spotify OAuth flow"""
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({"auth_url": auth_url})

@app.route('/api/auth/status')
def auth_status():
    """Check if user is authenticated"""
    token_valid = sp_oauth.validate_token(cache_handler.get_cached_token())
    return jsonify({"authenticated": token_valid})

@app.route('/callback')
def callback():
    if request.args.get('code'):
        token_info = sp_oauth.get_access_token(request.args['code'])
        if token_info:
            session['token_info'] = token_info
            # Redirect to React frontend after successful auth
            return redirect('http://localhost:5173/?auth=success')

    return redirect('http://localhost:5173/?auth=error')

@app.route('/api/get_tracks')
def get_tracks():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        return jsonify({"error": "Not authenticated", "authenticated": False}), 401
    
    try:
        tracks = sp.current_user_top_tracks(limit=5)
        track_info = [(track['name'], track['artists'][0]['name']) for track in tracks['items']]
        session['track_info'] = track_info
        return jsonify({"tracks": track_info, "authenticated": True})
    except Exception as e:
        print(f"Error fetching tracks: {str(e)}")
        session.clear()
        return jsonify({"error": str(e), "authenticated": False}), 500

@app.route('/api/user/profile')
def get_user_profile():
    """Get current user's Spotify profile"""
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        user = sp.current_user()
        profile_data = {
            "display_name": user.get('display_name', 'User'),
            "id": user.get('id'),
            "images": user.get('images', [])
        }
        return jsonify(profile_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/emotion_info')
def analyze_song_emotion():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        return jsonify({"error": "Not authenticated"}), 401
    
    if 'track_info' not in session:
        return jsonify({"error": "No track info available"}), 400

    track_info = session['track_info']
    
    try:
        # Process all songs at once
        emotion_results = []
        
        for track_name, artist_name in track_info:
            # Get lyrics for each song
            lyrics = get_lyrics(artist_name, track_name)
            if lyrics:
                # Chunk and analyze lyrics
                chunks = chunk_lyrics(lyrics)
                emotion_data = lyric_emotion_info(chunks)
                normalized_emotions = normalize_emotions_percent(emotion_data)
                
                emotion_results.append({
                    "track": track_name,
                    "artist": artist_name,
                    "emotions": normalized_emotions
                })
        
        return jsonify({
            "success": True,
            "emotion_analysis": emotion_results,
            "total_songs": len(emotion_results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)