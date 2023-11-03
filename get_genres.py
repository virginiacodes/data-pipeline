import requests
import pandas as pd
import os
import json
import time
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from cherrypicker import CherryPicker
from dotenv import load_dotenv

load_dotenv()


def get_genre():
    '''Retrieve artists Spotify IDs and save into a list
       Use list in for loop to retrieve artists data
       Return dataframe with artists name, genres and number of followers'''

    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get("SPOTIPY_CLIENT_ID"),
        'client_secret': os.environ.get("SPOTIPY_CLIENT_SECRET")
    })

    # convert the response to JSON
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
    
    # Empty dataframe, will be used on line 82
    main_df = pd.DataFrame()

    for id in playlist_id:

        # Retrieve artists ID from API
        r = requests.get(BASE_URL + 'playlists/' + id + '/tracks', 
                        headers=headers,                  
                        params={'fields': 'items(track(name, artists(id)))', 'limit': 100})
        # Convert result to JSON
        d = r.json()
     
        # Flatten nested dictionary using CherryPicker library
        picker = CherryPicker(d)
        flat = picker['items'].flatten().get()
        df = pd.DataFrame(flat)

        # Removing columns with null value
        dfresult = df.dropna(axis=1)

        # Turn artist id column into a list to use in for loop iteration
        artists_id_list = dfresult['track_artists_0_id'].to_list()

        for id in artists_id_list:   

            # Retrieve artists data from API
            r2 = requests.get(BASE_URL + 'artists/' + id, 
                        headers=headers,                  
                        params={'fields': 'items(genres, name)', 'limit': 100})
            # Convert result to JSON
            data_genres = r2.json()
    
            df_genres = pd.json_normalize(data_genres)
            # Delete columns that are not needed
            df_genres_edited = df_genres.drop(['href', 'id', 'images', 'popularity', 'type', 'uri', 
                     'external_urls.spotify', 'followers.href'], axis=1)
    
            # Add retrieved data to dataframe
            concat_df = pd.concat([main_df, df_genres_edited])
            main_df = concat_df
            # Pause for 1 second to avoid reaching API rate limit
            time.sleep(1)
    
    return main_df


if __name__ == "__main__":
    get_genre()
