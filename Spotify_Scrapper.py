import requests
from requests.exceptions import ConnectionError
import re


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


def _strip_title(title):
    title = title.split(' - ')[0]
    title = re.sub(r'\([^)]*\)', '', title)
    return title


def spotify_get_playlist(spotify_token, spotify_playlist_id, offset=0, limit=100):
    track_list = {'tracks': []}
    headers = {
        'Authorization': f'Bearer {spotify_token}',
    }
    url = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks?offset={offset}&limit={limit}"
    response = requests.get(url, headers=headers)
    try:
        for track in response.json()["items"]:
            track_info = {
                "name": _strip_title(track['track']['name']),
                "artist": track['track']['artists'][0]['name'],
                "spotify_release": track['track']['album']['release_date'].split('-')[0]
            }
            track_list['tracks'].append(track_info)

        if response.json()["next"]:
            offset, limit = re.search(r'offset=(\d+)&limit=(\d+)', response.json()["next"]).groups()
            track_list['tracks'] = track_list['tracks'] + spotify_get_playlist(spotify_token, spotify_playlist_id, offset=offset, limit=limit)['tracks']

        return track_list

    except Exception as e:
        print(f"Exception: {e}")
        return []


def _spotify_search(spotify_token, search_phrase, type):
    headers = {
        'Authorization': f'Bearer {spotify_token}',
    }
    params = {
        'q': search_phrase,
        'type': type
    }
    url = f"https://api.spotify.com/v1/search"
    response = requests.get(url, headers=headers, params=params)
    return response


def get_earliest_release_date_of_song(spotify_token, song_info: dict):
    search_phrase = f"{song_info['name']} - {song_info['artist']}"
    response = _spotify_search(spotify_token, search_phrase, 'track').json()
    release_years = []
    for track in response['tracks']['items']:
        result_artist = track["artists"][0]["name"]
        result_title = track["name"]
        if song_info['artist'].lower() in result_artist.lower() and song_info['name'].lower() in result_title.lower():
            release_year = track["album"]["release_date"].split('-')[0]
            release_years.append(int(release_year))
    oldest_release = min(release_years, default=float('inf'))
    return str(min(oldest_release, int(song_info['spotify_release'])))








