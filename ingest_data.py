import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import csv

from cherrypicker import CherryPicker

import sqlite3 as sl
import sqlalchemy as sa
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


AUTH_URL = 'https://accounts.spotify.com/api/token'

# Function that returns artists name and track name in dictionary form
def get_tracks():

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

    # pull all playlist entries
    r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', 
                    headers=headers,                  
                    params={'fields': 'items(track(name, artists(name)))', 'limit': 100})
    d = r.json()


    picker = CherryPicker(d)
    flat = picker['items'].flatten().get()
    df = pd.DataFrame(flat)


    df = df.drop(['track_artists_1_name'], axis=1)
    df = df.drop(['track_artists_2_name'], axis=1)
    df = df.drop(['track_artists_3_name'], axis=1)
    df = df.drop(['track_artists_4_name'], axis=1)
    df = df.drop(['track_artists_5_name'], axis=1)



    print(df)


    # df = pd.DataFrame.from_dict(d, orient='columns')



     

    






if __name__ == "__main__":
    get_tracks()
