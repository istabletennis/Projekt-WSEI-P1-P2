from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_SECRET")
spotify_playlist_id= "37i9dQZF1DWUGhrXBsyMVJ"


def spotify_get_token(client_id, client_secret):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def spotify_get_playlist_tracks(spotify_token, spotify_playlist_id, offset=0, limit=100):
    track_list = []
    headers = {
        'Authorization': f'Bearer {spotify_token}',
    }
    url = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks?offset={offset}&limit={limit}"
    response = requests.get(url, headers=headers)
    x = response.json()
    try:
        for track in response.json()["items"]:
            track_name = track['track']['name']
            artists = ', '.join([x['name'] for x in track['track']['artists']])
            track_list.append(f'{track_name} - {artists}')

        if response.json()["next"]:
            match = re.search(r'offset=(\d+)&limit=(\d+)', response.json()["next"])
            offset = match.group(1)
            limit = match.group(2)
            track_list = track_list + spotify_get_playlist_tracks(spotify_token, spotify_playlist_id, offset=offset, limit=limit)

        return track_list

    except Exception as e:
        print(f"Exception: {e}")
        return []


if __name__ == "__main__":
    spotify_token = spotify_get_token(spotify_client_id, spotify_client_secret)
    for song in spotify_get_playlist_tracks(spotify_token, spotify_playlist_id):
        print(song)
