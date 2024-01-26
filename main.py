import Genius_Scrapper as genius
from Spotify import *
from dotenv import load_dotenv
import os
import json

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_API_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")
spotify_playlist_id = "3JLryF82HynTqqOnpEKtUx"
spotify_playlist_name = "50sLoveSongs"

playlist_ids = [
    # "6gfg0SNQ0ebRID2r0Tf19o", done
    # "37i9dQZF1EIe9kRMasbUWQ", timeout
    # "37i9dQZF1DWYUCqLrWKr4p", done
    # "7wpHFMfczO4QMY19sQ19jw", done
    # "6cr7pq4MWgM3F3TCssX6bL", done
    # "6PV6JdJQxLY8PX6RKCtdSe", timeout
    # "37i9dQZF1DWY373eEGlSj4", done
    # "7IgUBxZamXXF44C5Bq0WQN", timeout
    # "2rKCt2r9K2oktq7bGrawcQ", done
    # "4wVun2fjaTGP6X7h0FAGmI", done
    # "1ez8DRkt6zSv7VbsydUTgF", done
    # "37i9dQZF1DXc3KygMa1OE7", done
    # "4NPYnFL3EQcHPB82Qbv5A5", done
    # "2FCW1UTJOUIP3qMLiSIaog", done
    # "5hi1dLxyaOgxNbS9xvRSPu", done
    # "2hGBRYAON8N8e9sHQrGpwi", done
    # "5T85yZiWjhmOj2QmyzT8Qy", timeout
    "37i9dQZF1DWXqpDKK4ed9O",
    "5Kar9ubIBpXecVyV9kEz1d",
    "16PHbxRcSspmRSlYIgArdR",
    "37fSBUXHEieXa1KU2NmVuf",
    "37i9dQZF1DXd0DyosUBZQ7",
    "37i9dQZF1DXd0DyosUBZQ7",
    "55526srud2X6DyvnELI1g0",
    "2YnpVaTqjNk0qxzEPu36W0",
    "0VaitZrpLDbFuaMqURX6hG",
    "2tRXrKvNkV5t9wdZqoOgCW",
    "37i9dQZF1DWVTfbQdQ8l7H",
    "37i9dQZF1EIdsS2tNc85Lj",
    "6BlEK8z04aI8aZnpIpqMhG",
    "37i9dQZF1EIdsS2tNc85Lj",
    "1zTuR5uEZ8MG3LX74IZPOD",
    "6oNsYDhN95gkENsdFcAwTh",
    "4qfKXdLwk7ruT8uM6sdVXq",
    "37i9dQZF1DX7Z7kYpKKGTc",
    "37i9dQZF1DX50QitC6Oqtn",
    "4HN214laokstO6XtPSSUhc",
    "27Vexc5zoyUbu0JXmJqoZb",
    "2dIxoKGXCZK0VSKrdpmGEL",
    "4EWeAEldtmPTzCZ3aVfHlm",
    "4UBSNKDnfsc4hkbsGwZg13",
    "37i9dQZF1EIf5L4STgdymG",
    "37i9dQZF1DX7rOY2tZUw1k"
]

for id in playlist_ids:
    SPOTIFY_TOKEN = spotify_get_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    playlist = spotify_get_playlist(SPOTIFY_TOKEN, id)

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

    with open(f"playlists/{id}.json", 'w') as json_file:
        json.dump(playlist, json_file, indent=4)
