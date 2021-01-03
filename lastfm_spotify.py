import json
import requests
from pprint import pprint

import secrets


class LastFmSpotify:

    def __init__(self):
        self.playlist_length = 10
        self.playlist_name = f'LastFM Top {self.playlist_length} Playlist'
        self.token = secrets.spotify_token()
        self.api_key = secrets.last_fm_api_key()
        self.user_id = secrets.spotify_user_id()
        self.spotify_headers = {"Contents-type": "application/json",
                        "Authorization": f"Bearer {self.token}"}
        self.playlists_uri = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'

    def fetch_songs_from_lastfm(self):
        params = {'limit': self.playlist_length, 'api_key': self.api_key}
        url = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json'
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("ERROR")
            pprint(response)
        res = response.json()

        lastfm_songs = []
        for item in res['tracks']['track']:
            song = item['name'].title()
            artist = item['artist']['name'].title()
            lastfm_song = {'song': song, 'artist': artist}
            print(f"LastFM : {lastfm_song}")
            if lastfm_song['song'] != 'Last Christmas':
                lastfm_songs.append(lastfm_song)
        return lastfm_songs

    def get_uri_from_spotify(self, song, artist):
        params = {
            'type': 'track',
            'q': f'{artist, song}',
            'limit': 10,
            'offset': 0
        }
        url = f"https://api.spotify.com/v1/search"
        response = requests.get(url, params=params, headers=self.spotify_headers)
        if response.status_code != 200:
            print("ERROR")
            pprint(response)

        res = response.json()
        # Popularity ranges from 0-100, where 100 is the most popular
        popularity = 0
        song_uri = ''
        song_name = ''
        artist_name = ''
        output_uri = (res['tracks']['items'])
        for item in output_uri:
            # print (f"{item['id']}, popularity: {item['popularity']}")
            if item['popularity'] > popularity:
                popularity = item['popularity']
                song_uri = item['uri']
                song_name = item['name']
                artist_name = item['artists'][0]['name']
        print(f'Spotify: {song_name}, {artist_name}: {song_uri}\n')
        return song_uri

    def create_spotify_playlist(self):
        data = {
          "name": f"{self.playlist_name}",
          "description": "Top 20 tracks from LastFM",
          "public": 'true'
        }
        data = json.dumps(data)
        url = self.playlists_uri
        response = requests.post(url, headers=self.spotify_headers, data=data)
        if 200 <= response.status_code < 300:
            print("Successfully created Spotify playlist")
        else:
            print("ERROR creating playlist!")
            pprint(response)

        res = response.json()
        return res['id']

    def add_songs_to_playlist(self, playlist_id, tracks):
        url = f"{self.playlists_uri}/{playlist_id}/tracks"
        data = {
          "uris": tracks
        }
        data = json.dumps(data)
        # pprint(data)
        response = requests.post(url, headers=self.spotify_headers, data=data)
        if 200 <= response.status_code < 300:
            print("Successfully added tracks to Spotify playlist")
        else:
            print("ERROR updating playlist!")
            pprint(response)

    def list_songs_in_playlist(self, playlist_id):
        url = f"{self.playlists_uri}/{playlist_id}/tracks"
        response = requests.get(url, headers=self.spotify_headers)
        if 200 != response.status_code:
            print(f"ERROR! Could not list songs in playlist {playlist_id}")

        res = response.json()
        return res

