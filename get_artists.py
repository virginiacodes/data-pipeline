import requests
import pandas as pd
import os
import json
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from cherrypicker import CherryPicker
from dotenv import load_dotenv

load_dotenv()


AUTH_URL = 'https://accounts.spotify.com/api/token'
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'


def get_tracks():
    '''Retrieve data from API (Track and artist name)
       Return dataframe
    '''
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get("SPOTIPY_CLIENT_ID"),
        'client_secret': os.environ.get("SPOTIPY_CLIENT_SECRET")
    })

    # Convert the response to JSON
    auth_response_data = auth_response.json()
    # Credentials and permissions to access the API data
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # List of Spotify playlists ID (found at the end of URL)
    playlist_id = ['37i9dQZF1DWVRSukIED0e9', 
                   '1ge2g9hnspd2kHj2swfzLf', 
                   '5GhQiRkGuqzpWZSE7OU4Se',
                   '56r5qRUv3jSxADdmBkhcz7',
                   '1HXkVtgsiWJIZ4frLZV4hx']
    
    # Variable used on line 61 to create new 'Year' column 
    current_year = 2019
    # Empty dataframe, will be used on line 66  
    main_df = pd.DataFrame()

    for id in playlist_id:

        # Retrieve tracks data from API
        r = requests.get(BASE_URL + 'playlists/' + id + '/tracks', 
                        headers=headers,                  
                        params={'fields': 'items(track(name, artists(name)))', 'limit': 100})
        # Convert to JSON
        d = r.json()
     
        # Flatten nested dictionary using CherryPicker library
        picker = CherryPicker(d)
        flat = picker['items'].flatten().get()
        df = pd.DataFrame(flat)
        
        # Add column for year in dataframe
        df['Year'] = current_year
        current_year += 1

        # Add retrieved data to dataframe
        concat_df = pd.concat([main_df, df])
        main_df = concat_df
    
    # Removing columns with null value 
    # One track had 6 artists and it created a new column for each
    # we are just keeping the main artist
    dfresult = main_df.dropna(axis=1)

    return dfresult
        

if __name__ == "__main__":
    get_tracks()
