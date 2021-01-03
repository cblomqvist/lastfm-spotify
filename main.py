from lastfm_spotify import LastFmSpotify
from pprint import pprint

# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if __name__ == '__main__':
    d = LastFmSpotify()
    track_uris = []

    print(f"Getting top {d.playlist_length} songs from LastFM (excluding Last Christmas from result)")
    songs = d.fetch_songs_from_lastfm()
    # print(f"Songs from LastFM: {songs}")

    print(f"Getting URIs for {songs.__len__()} songs from Spotify")
    for song in songs:
        track_uri = d.get_uri_from_spotify(song['song'], song['artist'])
        track_uris.append(track_uri)
        # print(track_uri)

    print("Creating a Spotify Playlist")
    playlist_id = d.create_spotify_playlist()

    print(f"Adding songs to playlist {playlist_id}")
    d.add_songs_to_playlist(playlist_id, track_uris)

    print("Added these songs to the playlist")
    songlist = d.list_songs_in_playlist(playlist_id)
    for item in songlist['items']:
        song = item['track']['name']
        artist = item['track']['artists'][0]['name']
        print(f" - '{song}', by {artist}")
