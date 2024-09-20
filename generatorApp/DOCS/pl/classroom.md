# classroom.py

Ten plik zawiera klasę Classroom oraz funkcję do zamiany danych z pandas DataFrame na instancje klasy  

---

## Classroom
* ### Parametry:
    * classroom_name: nazwa sali lekcyjnej, nie używane w kodzie
    * type_id: id typu sali lekcyjnej, 
  typ jest używany do podziału sal lekcyjnych na różne typy laboratoriów

## create_classrooms
* ***Parametry***:
    * classroom_df: surowe dane sal lekcyjnych (pandas DataFrame)

* Użycie:
: zamienia dane z pandas DataFrame na instancje klasy  

* Zwraca:
: słownik sal lekcyjnych, klucz - classroom_id
