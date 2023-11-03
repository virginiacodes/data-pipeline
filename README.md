# Spotify Data Pipeline

A data pipeline that can be used to retrieve information about songs and artists on Spotify.
The current code is using 5 playlists containing the top 100 artists in the charts from 2019 to 2023.
You can easily change the playlists IDs to retrieve information about any playlists on Spotify.

## Spotify API

Start by creating an account here: [Spotify for Developers](https://developer.spotify.com/)
Go to your Dashboard and create a 'New app'.
In your new app, go to 'Settings' and you will find your client ID and client Secret needed to connect to the API.

## Clone this repository and add a .env file

This is where you will save your client ID and client Secret from your Spotify app. In this format:

SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret

## __main__.py

Run this file to start the data processing. Make sure to add your own directory path on line 19 and 20 to create your csv files.

## get_artists.py

The function in this file currently retrieve the name of the track and artist in 5 top 100 charts playlist from 2019 to 2023.
If you want to change which playlist to retrieve data from, here is what to do:

1. Go to Spotify and find a playlist you like.
2. Copy the playlist ID which are a bunch of numbers that can be found at the end of its URL like in this example:
   
   https://open.spotify.com/playlist/**37i9dQZF1DWVCKO3xAlT1Q**
   That's the Eurovision 2023 winners playlist (best playlist of the year in my opinion) :tada:

3. Go to line 38 of this file and replace the playlist IDs in the list with your own.

If you want to change what data to retrieve from that playlist, go to this [Documentation page](https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks) 
It shows a list of attributes you can retrieve from a playlist. To edit this file, go to line 54 and change the values in brackets.
   
If the tracks in your playlists are not all from the same year, make sure to delete lines 44 and 45, and lines 63 to 65.

## get_genres.py

The function in this file currently retrieve the name of the artist, its genre and the number of followers they have in 5 top 100 charts playlist from 2019 to 2023.

If you replaced the playlist IDs with your own in the previous file, make sure to do the same in this one on line 39.

On line 79, we deleted data not needed for this particular project. If you want to retrieve all data, just delete this line or remove the column you want to keep from the drop method.


