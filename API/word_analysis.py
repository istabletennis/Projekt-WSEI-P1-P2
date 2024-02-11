from songs_utility import prepare_song_lyrics
from textblob import TextBlob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import statistics
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def get_words_count_from_list_of_songs(list_of_songs: list[dict]) -> dict:
    """
    :param list_of_songs: list of song objects got from database
    :return: sorted dict of word occurrences
    """
    word_count = {}
    unwanted_tags = ["IN", "DT", "RP", "POS", "VBP", "RB", "VBZ", "TO", "PRP", "MD", "CC", "WRB", "WP", "PRP$", "UH"]
    for song in list_of_songs:
        blob = TextBlob(prepare_song_lyrics(song['lyrics']))
        for tagged_word in blob.tags:
            word, tag = tagged_word
            word = word.lower()
            if tag in unwanted_tags:
                continue
            else:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

    word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: -item[1])}
    return word_count


def get_noun_phrase_count_from_list_of_songs(list_of_songs: list[dict]) -> dict:
    """
    :param list_of_songs: list of song objects got from database
    :return: sorted dict of noun phrase occurrences
    This method gets all noun phrases from song, removes duplicates and puts them to noun_phrase_count dict
    """
    noun_phrase_count = {}
    for song in list_of_songs:
        blob = TextBlob(prepare_song_lyrics(song['lyrics']))
        for noun_phrase in list(set(blob.noun_phrases)):
            noun_phrase = noun_phrase.lower()
            if noun_phrase not in noun_phrase_count:
                noun_phrase_count[noun_phrase] = 1
            else:
                noun_phrase_count[noun_phrase] += 1

    noun_phrase_count = {k: v for k, v in sorted(noun_phrase_count.items(), key=lambda item: -item[1])}
    return noun_phrase_count


def get_average_sentiment_polarity_from_list_of_songs(list_of_songs: list[dict]) -> float:
    """
    :param list_of_songs: list of song objects got from database
    :return: list of polarities
    This method gets sentiment polarity for each song in provided list
    """
    polarity_list = [TextBlob(prepare_song_lyrics(song['lyrics'])).sentiment.polarity for song in list_of_songs]
    return statistics.mean(polarity_list)


def get_average_sentiment_subjectivity_from_list_of_songs(list_of_songs: list[dict]) -> float:
    """
    :param list_of_songs: list of song objects got from database
    :return: list of subjectivities
    This method gets sentiment objectivity for each song in provided list
    """
    subjectivity_list = [TextBlob(prepare_song_lyrics(song['lyrics'])).sentiment.subjectivity for song in list_of_songs]
    return statistics.mean(subjectivity_list)


def get_all_words_count_average_from_list_of_songs(list_of_songs: list[dict]) -> int:
    return int(statistics.mean([len(TextBlob(prepare_song_lyrics(song['lyrics'])).words) for song in list_of_songs]))


def create_bar_chart_out_of_count_object(title: str, y_axis_value: str, word_count: dict, chart_range: int, output_file: str):
    words = list(word_count.keys())[:chart_range]
    quantities = list(word_count.values())[:chart_range]
    plt.figure(figsize=(10, 6))
    plt.barh(words, quantities, color='grey')
    plt.xlabel('Quantity')
    plt.ylabel(y_axis_value)
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_file)

