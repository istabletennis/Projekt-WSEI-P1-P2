def get_songs_from_release_range(db, collection_name, lower_range: int, upper_range: int) -> list[dict]:
    result = []
    for song in db[collection_name].find(
            ({"$and": [{"spotify_release": {"$gt": lower_range}}, {"spotify_release": {"$lt": upper_range}}]})):
        result.append(song)
    return result


def get_first_song_with_title(db, collection_name, song_title) -> list[dict]:
    return db[collection_name].find_one({"name": song_title})


def prepare_song_lyrics(lyrics) -> dict:
    return lyrics.replace(r"\u2018", "'").replace(r"\u2019", "'")