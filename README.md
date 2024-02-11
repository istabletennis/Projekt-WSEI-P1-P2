

# DOKUMENTACJA ZMIAN W PROJEKCIE

*10/01/24*\
Ze względu na istnienie gotowej API serwisu z tekstami piosenek Genius.com zdecydowałam się skorzystać z tego właśnie rozwiązania w celu zdobycia niezbędnych danych — tekstów piosenek o miłości. W tym celu napiszę skrypt łączący się z tymże API, w celu ich pobrania (jest to forma web scrappera wspomnianego w Wiki projektu - https://github.com/istabletennis/Projekt-WSEI-P1-P2/wiki/1.-Karta-Projektu). Napotkałam przy tym istotną przeszkodę, jaką jest brak możliwości wyszukiwania tekstów piosenek po tematyce, gatunku czy słowach "kluczach" w tekstach. Możliwe jest jedynie wykorzystanie nazwy artysty, roku produkcji. W związku z tym postanowiłam przejrzeć tematyczne playlisty w aplikacji streamingowej Spotify, dzięki którym odnajdę tytuły i artystów piosenek o miłości z interesujących mnie dekad - 1950s do 2020s, z różnych gatunków i podgatunków, w celu zapewnienia sobie różnorodnej puli badawczej (**playlists.txt**).
Po zidentyfikowaniu interesujących mnie playlists (jest ich 46), napiszę skrypt pobierający listę piosenek wraz z wykonawcami w formie testowej. Następnie usunę duplikaty. Plik ze skryptem dla przykładowej playlisty nazwać będzie **Spotify_Scrapper.py**.
Z tak gotową listą będę mogła przystąpić do pobierania tekstów piosenek z portalu Genius.com.


*16/01/24*\
Po napisaniu skryptu w celu ściągnięcia listy piosenek z wyselekcjonowanych playlist na Spotify konieczne jest napisanie skryptu do wyszukania tychże utworów poprzez genius API (apka portalu z tekstami piosenek). Wyszukiwać piosenek będę po ich tytule i artyście, a następnie będę sprawdzać i przypisywać indywidualne ID piosenki z portalu Genius do niej samej. W ten sposób moim kolejnym krokiem może być użycie skryptu szukającego po genius ID utworu i ściągającego jego tekst.
Skrypt można znaleźć pod nazwą **Genius_Scrapper.py**.
Teksty wszystkich piosenek zostaną zapisane w pliku JSON, a następnie załadowane do bazy danych.

*25/01/24*\
Zmiany w skrypcie **Spotify_Scrapper.py**:
* Wzbogacenie o metodę wyszukiwania najwcześniejszej daty powstania (przy eliminacji 'remastered', 'version X, 'feat', etc.); 
* Wszystkie metody zostały przekształcone w celu generowania wyniku w postaci JSON

Zmiany w skrypcie **Genius_Scrapper.py**:
* Powstała dodatkowa walidacja wyników wyszukiwania
 
Powstał plik **main.py**, który korzysta z metod zamieszczonych w obu powyższych scrapperach.

*26/01/24*\
Skrypt *main.py*: główna część skryptu została zamknięta w pętli, w której w każdej iteracji pozyskiwane są dane z kolejnych playlist, których ID zawarte są w zdefiniowanej liście. Pobierane są informacje o artyście, tytule, roku wydania (wg portalu Genius i Spotify) i tekście.

*28/01/24*\
Przeprowadzono normalizacje danych we wszystkich wygenerowanych plikach JSON. Z sukcesem zostały zupadatowane 29 plików  JSON, które następnie zostały załadowane do lokalnie hostowanej bazy danych MongoDB. Przed usunięciem duplikatów nasza baza posiada łącznie 2920 arrays (tekstów piosenek).

*01/02/24*\
Pliki JSON z danymi utworów zunifikowano w jeden plik. Przesiano wyniki w celu usunięcia duplikatów, usunięto je, a następnie załadowano ponownie do lokalnej bazy danych 2, kolekcji P2. W kolekcji znajduje się obecnie 2159 unikatowych tekstów piosenek. Poniżej prezentowane są statystyki ilości uzyskanych tekstów z uwzględnieniem dekady, w której powstały.

* 50s:1949-1960: 174
* 60s: 1959-1970: 284
* 70s: 1969-1980: 393
* 80s: 1979-1990: 342
* 90s: 1989-2000: 179
* 00s: 1999-2011: 374
* 10s: 2009-2020: 613
* 20s: 2019-2030: 261

*05/02/24*\
Stworzono szkielet testowej aplikacji we frameworku fast API. Posiada następujące funkcje: logowanie, rejestracja, wylogowywanie użytkownika, komunikacja z bazą danych (nowa kolekcja: users) oraz prototyp strony oczekiwania na zakończenie działania skryptu docelowego. Aplikacja została umieszczona w folderze **API** wraz z prowizorycznym front-endem.

*11/02/24*\
Dodałam nowy plik python **songs_utility.py**, który zawiera podstawowe metody odpowiedzialne za wysyłanie zapytań do bazy danych MongoDB (get data).
Dodałam także nowy plik **word_analysis.py**, który stanowi kolekcje metod odpowiedzialnych za analizę tekstów piosenek (bibliotek: textblob). Przeprowadzona została analiza pod kątem ilości słów, ich częstotliwości występowania (z wyłączeniem słów niewnoszących nic do analizy, np. przyimków) oraz analiza sentymentu tekstu. W pliku znajduje się metoda służąca do stworzenia wykresu słupkowego na podstawie danych — tekstów piosenek. 
Zadanie wykonywane w tle w pliku **main.py** (folder API) został zamieniony na zadanie, które wykonuje następujące czynności:
* pobranie piosenek z żądanego okresu
* obliczenie ich ilości
* obliczenie ilości słów w piosenkach z żądanego okresu
* określenie sentymentu
* stworzenie odpowiednich pól analizy, w tym wykresu\
Przerobione zostały formularze HTML by wyświetlać zawartości w bardziej przystępny sposób.
Dodano plik **requirements.txt**.
Tym sposobem aplikacja została oddana do użytku i oceny. Spełnia ona wymagania określone w początkowej fazie tworzenia projektu (patrz: WIKI).
