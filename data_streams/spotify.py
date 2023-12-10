from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import webbrowser
from data_streams.api_keys import spotify_client_id, spotify_client_secret


# Spotify API credentials
client_id = spotify_client_id
client_secret = spotify_client_secret
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-read-recently-played'

# Flask app setup
app = Flask(__name__)

# Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope)

# Global variable to store songs
songs_list = None

# Route to handle OAuth redirect and get access token
@app.route('/callback')
def callback():
    global songs_list
    auth_code = request.args.get('code')
    token_info = sp_oauth.get_access_token(auth_code)
    songs_list = get_recently_played(token_info['access_token'])
    return "Received songs list, you can close this window."

# Function to retrieve Spotify listening history
def get_recently_played(access_token):
    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_recently_played(limit=20)
    songs = ""
    for idx, item in enumerate(results['items']):
        track = item['track']
        songs += f"{idx}: {track['artists'][0]['name']} – {track['name']}\n"
    return songs

# Function to run the Flask app
def run_app():
    app.run(port=8888)

# Function to start the Spotify server and handle authentication
def run_spotify_server():
    global songs_list
    # Run Flask app in a separate thread
    threading.Thread(target=run_app, daemon=True).start()

    # Open the browser for user authentication
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    webbrowser.open(auth_url)

    # Wait for the songs list to be populated
    while songs_list is None:
        pass

    return songs_list

def get_spotify_data():
    output = "These are songs from my Spotify I have played recently. You can perhaps talk about the type of music I have been listening to as one of the diary entries.\n\n"
    songs = run_spotify_server()
    print(songs)
    output+=songs
    return songs

