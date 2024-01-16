from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup as bs

load_dotenv()
genius_token = os.getenv("GENIUS_API_TOKEN")


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
        result = response.json()['response']['hits'][0]['result']['api_path'].split('/')[2]
    except:
        result = 'none'
    return result


def get_song_lyrics_url(genius_token, song_id):
    headers = {
        'Authorization': f'Bearer {genius_token}',
    }

    url = 'https://api.genius.com/songs/' + song_id
    response = requests.get(url, headers=headers)
    try:
        result = response.json()['response']['song']['url']
    except:
        result = 'none'
    return result


def get_song_lyrics(song_lyrics_url):
    raw_text = requests.get(song_lyrics_url).text
    soup = bs(raw_text.replace('<br/>', '\n'), "html.parser")
    container = soup.find_all('div', class_=lambda c: c and c.startswith('Lyrics__Container'))
    text = "\n".join([x.get_text() for x in container])
    return text


if __name__ == "__main__":
    song_id = get_first_match_id(genius_token, "Caroline Polachek - Sunset")
    song_lyrics_url = get_song_lyrics_url(genius_token=genius_token, song_id=song_id)
    lyrics = get_song_lyrics(song_lyrics_url)
    print(lyrics)


