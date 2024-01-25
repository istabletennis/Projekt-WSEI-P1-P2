import requests
from bs4 import BeautifulSoup as bs


def get_first_match_id(genius_token, search_phrase):
    headers = {
        'Authorization': f'Bearer {genius_token}',
    }
    params = {
        'q': search_phrase,
    }
    url = 'https://api.genius.com/search'
    response = requests.get(url, headers=headers, params=params)
    try:
        if response.json()['response']['hits'][0]['result']['primary_artist']['name'].lower() in search_phrase.lower():
            result = response.json()['response']['hits'][0]['result']['api_path'].split('/')[2]
            return result
        else:
            return None
            print(f"No lyrics found for {search_phrase}")
    except:
        print(f"Could not find any match for {search_phrase}")
        return None


def get_song_info(genius_token, song_id):
    headers = {
        'Authorization': f'Bearer {genius_token}',
    }
    url = 'https://api.genius.com/songs/' + song_id
    response = requests.get(url, headers=headers)
    return response


def get_song_lyrics_url(song_info):
    try:
        return song_info.json()['response']['song']['url']
    except:
        print(f"No song lyrics for song {song_info.json()['response']['song']['title']}")
        return None


def get_song_release_date(song_info):
    try:
        return song_info.json()['response']['song']['release_date']
    except:
        return None


def get_song_lyrics(song_lyrics_url):
    if song_lyrics_url is None:
        return None
    else:
        raw_text = requests.get(song_lyrics_url).text
        soup = bs(raw_text.replace('<br/>', '\n'), "html.parser")
        container = soup.find_all('div', class_=lambda c: c and c.startswith('Lyrics__Container'))
        text = "\n".join([x.get_text() for x in container])
        return text





