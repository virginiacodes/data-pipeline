import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': os.environ.get("SPOTIPY_CLIENT_ID"),
    'client_secret': os.environ.get("SPOTIPY_CLIENT_SECRET")
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Get playlist data
playlist_id = '1HXkVtgsiWJIZ4frLZV4hx'

# pull all artists albums
r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', 
                headers=headers,                  
                params={'fields': 'items(track(name, artists(name, genres)))', 'limit': 100})
d = r.json()

print(d)

# name, artist[name], release_date

