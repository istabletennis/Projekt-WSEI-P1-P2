
# DOKUMENTACJA ZMIAN W PROJEKCIE

*10/01/24*\
Ze względu na istnienie gotowej API serwisu z tekstami piosenek Genius.com zdecydowałam się skorzystać z tego właśnie rozwiązania w celu zdobycia niezbędnych danych - tekstów piosenek o miłości. W tym celu napiszę skrypt łączący się z tymże API, w celu ich pobrania (jest to forma web scrappera wspomnianego w Wiki projektu - https://github.com/istabletennis/Projekt-WSEI-P1-P2/wiki/1.-Karta-Projektu). Napotkałam przy tym istotną przeszkodę, jaką jest brak możliwości wyszukiwania tekstów piosenek po tematyce, gatunku czy słowach "kluczach" w tekstach. Możliwe jest jedynie wykorzystanie nazwy artysty, roku produkcji. W związku z tym postanowiłam przejrzeć tematyczne playlisty w aplikacji streamingowej Spotify, dzięki którym odnajdę tytuły i artystów piosenek o miłości z interesujących mnie dekad - 1950s do 2020s, z różnych gatunków i podgatunków, w celu zapewnienia sobie różnorodnej puli badawczej (**playlists.txt**).
Po zidentyfikowaniu interesujących mnie playlists (jest ich 46), napiszę skrypt pobierający listę piosenek wraz z wykonawcami w formie testowej. Następnie usunę duplikaty. Plik ze skryptem dla przykładowej playlisty nazwać będzie **Spotify_Scrapper.py**.
Z tak gotową listą będę mogła przystąpić do pobierania tekstów piosenek z portalu Genius.com.


*16/01/24*\
Po napisaniu skryptu w celu ściągnięcia listy piosenek z wyselekcjonowanych playlist na Spotify, konieczne jest napisanie skryptu do wyszukania tychże utworów poprzez genius API (apka portalu z tekstami piosenek). Wyszukiwać piosenek będę po ich tytule i artyście, a następnie będę sprawdzać i przypisywać indywidualne ID piosenki z portalu Genius do niej samej. W ten sposób moim kolejnym krokiem może być użycie skryptu szukającego po genius ID utworu i ściągającego jego tekst.
Skrypt można znaleźć pod nazwą **Genius_Scrapper.py**.
Teksty wszystkich piosenek zostaną zapisane w pliku JSON, a następnie załadowane do bazy danych.
