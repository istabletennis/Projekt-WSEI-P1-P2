import Genius_Scrapper as genius
from Spotify_Scrapper import *
from dotenv import load_dotenv
import os
import json

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_API_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")
spotify_playlist_id = "3JLryF82HynTqqOnpEKtUx"
spotify_playlist_name = "50sLoveSongs"


SPOTIFY_TOKEN = spotify_get_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
playlist = spotify_get_playlist(SPOTIFY_TOKEN, spotify_playlist_id)

# playlist['tracks'] = playlist["tracks"][:5]

print('Searching for Songs release dates...')

for track in playlist["tracks"]:
    try:
        track["spotify_release"] = get_earliest_release_date_of_song(SPOTIFY_TOKEN, track)
        print(f"Found release date for song {track['name']} by {track['artist']}")
    except:
        print(f"Could not find earlier release date for song {track['name']} by {track['artist']}")
        continue

print('Searching For Lyrics...')

for track in playlist['tracks']:
    search_phrase = f"{track['name']} - {track['artist']}"
    song_id = genius.get_first_match_id(GENIUS_TOKEN, search_phrase)
    print(f"Searching for lyrics of song {search_phrase}")
    if song_id:
        song_info = genius.get_song_info(GENIUS_TOKEN, song_id)
        lyrics_url = genius.get_song_lyrics_url(song_info)
        track['genius_release'] = genius.get_song_release_date(song_info)
        if lyrics_url:
            track['lyrics'] = genius.get_song_lyrics(lyrics_url)
        else:
            track['lyrics'] = None
    else:
        track['lyrics'] = None

with open(f"{spotify_playlist_name}.json", 'w') as json_file:
    json.dump(playlist, json_file, indent=4)











