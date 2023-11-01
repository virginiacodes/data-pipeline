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
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

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

    # Get playlist data
    playlist_id = ['37i9dQZF1DWVRSukIED0e9', 
                   '1ge2g9hnspd2kHj2swfzLf', 
                   '5GhQiRkGuqzpWZSE7OU4Se',
                   '56r5qRUv3jSxADdmBkhcz7',
                   '1HXkVtgsiWJIZ4frLZV4hx']
    
    current_year = 2019
   
    main_df = pd.DataFrame()

    for id in playlist_id:

        # pull all playlist entries
        r = requests.get(BASE_URL + 'playlists/' + id + '/tracks', 
                        headers=headers,                  
                        params={'fields': 'items(track(name, artists(name)))', 'limit': 100})
        d = r.json()
     
        # Flatten dictionary using CherryPicker library
        picker = CherryPicker(d)
        flat = picker['items'].flatten().get()
        df = pd.DataFrame(flat)
        
        # Add column for year
        df['Year'] = current_year
        current_year += 1


        concat_df = pd.concat([main_df, df])
        main_df = concat_df

     
    
    # Removing columns with null value
    dfresult = main_df.dropna(axis=1)

    return dfresult
        

if __name__ == "__main__":
    get_tracks()
