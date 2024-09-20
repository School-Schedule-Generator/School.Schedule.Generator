# load_data.py

Ten plik zawiera funkcje do ładowania i operowania na danych

---

* ### Funkcje
  * ### load_data
      * ***Parametry***:
          * log_file_name: Plik, gdzie zapisane są dane dziennika
          * path: ścieżka do folderu z tabelami typu CSV lub Excel
          * tables: lista plików/tabel
          * dtype: typ danych do odczytu, może być .xlsx/.ods (plik Excel), .csv (wartości oddzielone przecinkiem), domyślnie xlsx

      * Zwraca:
      : lista ramek danych pandas lub False, jeśli pliki nie pasują do danych harmonogramu
  
  * ### class_to_dict
      * ***Parametry***:
          * obj: obiekt
      
      * Użycie
      : zamienia obiekt na słownik pythona

      * Zwraca:
      : obiekt w formacie słownika pythona
  
  * ### schedule_to_json
     * ***Parametry*** 
        * schedule: instancja Harmonogramu
        * file_path: ścieżka pliku do zapisania JSON
     
     * Użycie
     : zapisuje harmonogram do pliku   
  
  * ### schedule_to_excel
      * ***Parametry***:
          * schedule_dict: instancja harmonogramu w formacie słownika
          * data: lista surowych ramek danych pandas (ta sama kolejność jak w generatorze)
          * info: Argumenty (w formie słownika) do zapisania na stronie tytułowej arkusza harmonogramu,
            ustaw klucz 'Tytuł' dla dużego tytułu; domyślnie "Harmonogram szkoły"
          * file_path: ścieżka, gdzie ma zostać zapisany plik Excel
      
      * Użycie
      : tworzy plik Excela zawierający harmonogram podzielony na klasy

      * Zwraca:
      : None
