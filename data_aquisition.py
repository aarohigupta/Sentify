# given a list of spotify playlist ids, this script will get 
# the features (from spotify's api) for 400 songs from the playlists
# and save them to a csv file 
from pandas import DataFrame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np


def getData(playlists: list) -> DataFrame:
    # create empty dataframe to store data
    data = DataFrame(columns=['id', 'name', 'artist', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'])
    # get the data from spotify's api
    song_number = 0
    # if there are more than 400 songs in the playlists, only get 400
    for playlist in playlists:
        # get the tracks from the playlist
        tracks = sp.playlist_tracks(playlist)
        # get the features for each track
        for track in tracks['items']:
            # get the features for the track
            features = sp.audio_features(track['track']['id'])[0]
            # add the features to the dataframe
            data = data.append({'id': track['track']['id'], 'name': track['track']['name'], 'artist': track['track']['artists'][0]['name'], 'danceability': features['danceability'], 'energy': features['energy'], 'key': features['key'], 'loudness': features['loudness'], 'mode': features['mode'], 'speechiness': features['speechiness'], 'acousticness': features['acousticness'], 'instrumentalness': features['instrumentalness'], 'liveness': features['liveness'], 'valence': features['valence'], 'tempo': features['tempo'], 'duration_ms': features['duration_ms'], 'time_signature': features['time_signature']}, ignore_index=True)
            # increment the song number
            song_number += 1
            # if there are more than 400 songs, stop
            if song_number >= 400:
                break
    # return a dataframe of the data
    return data


credentials = json.load(open('authorization.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# trial run to see if function works
playlists = ["2WhRgVayJAZRqlKq12UOn4"]
getData(playlists).to_csv('trial.csv', index=False)
