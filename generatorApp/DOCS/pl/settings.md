# settings.py

Ten plik zawiera wszystkie ważne zmienne globalne oraz domyślne nazwy

Ponieważ ustawienia są stałe, tworzona jest tylko jedna instancja
w tym samym pliku, w którym jest zdefiniowana, dlatego do importowania ustawień
należy importować tylko tę instancję obiektu, jak pokazano poniżej:  
`from settings import settings`

---
Lista ustawień:
* DEBUG
: decyduje o przebiegu pracy programu, używane podczas testowania

* TKCAPTURE 
: bool decydujący, czy chcesz generować zrzuty ekranu tkintera 
harmonogramu w procesie tworzenia harmonogramu, 
więcej informacji na ten temat w osobnym rozdziale

* SAVELOG  
: bool decydujący, czy debuglog zapisuje logi do pliku

* BASE_DATA_PATH 
: ścieżka podstawowa wszystkich danych używanych przez program

* TEST_DATA_PATH 
: ścieżka do danych używanych **tylko** do testów

* DF_NAMES 
: lista nazw wszystkich dataframe'ów

* COLUMN_NAMES 
: słownik zawierający nazwy dataframe'ów jako klucze
i odpowiadające im nazwy ich kolumn

> [!UWAGA]  
> Używaj ***COLUMN NAMES*** do ponownego zapisu nazwy zamiast wydobywania jej ze zmiennych ustawień  
> Rób to dla czytelności i spójności
