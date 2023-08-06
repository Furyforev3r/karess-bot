import os
import time
from dotenv import load_dotenv, find_dotenv
from lyricsgenius import Genius
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

start_time = time.time()

load_dotenv(find_dotenv())
client_id = os.environ.get("client_id_spotify")
client_secret = os.environ.get("client_secret_spotify")
redirect_uri = "https://github.com/furyforev3r"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri
))


def get_playlist_tracks(user_id: str, playlist_id: str):
    playlist_items = sp.user_playlist_tracks(user_id, playlist_id, fields='items,uri,name,id,total', market='fr')['items']
    results = []

    for item in playlist_items:
        track = item['track']
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name']
        }

        results.append(track_info)

    return results


def main():
    genius = Genius(os.environ.get("CLIENT_ACCESS_TOKEN"))
    genius.verbose = False
    genius.remove_section_headers = True
    genius.skip_non_songs = False
    genius.excluded_terms = ["(Remix)", "(Live)"]

    user_id = os.environ.get("user_id")
    playlist_id = os.environ.get("playlist_id")

    if not all((client_id, client_secret, user_id, playlist_id)):
        print("Please set all required environment variables.")
        return

    tracks = get_playlist_tracks(user_id, playlist_id)
    lyrics = []

    for track in tracks:
        try:
            song = genius.search_song(track['name'], track['artist'])
            song_lyrics = song.lyrics
            final_lyrics = song_lyrics.replace('Embed', '').split("\n")
            song_dict = {'track': track, 'lyrics': final_lyrics}
            lyrics.append(song_dict)

        except Exception as e:
            print(f"An error occurred: {e}")

    lyics_dumps = json.dumps(lyrics, indent=4)

    with open('lyrics.py', 'w', encoding="utf-8") as f:
        f.write(f"lyrics = {lyics_dumps}")

    print(lyics_dumps)

    print("\n\n--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
