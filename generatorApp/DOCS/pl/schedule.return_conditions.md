# schedule/return_conditions.py

Ten plik zawiera funkcje klasy Harmonogram do sprawdzania, czy warunki są spełnione

---

## Funkcje
  * ### are_teachers_taken
    * ***Parametry***:
        * teachers_id: identyfikatory nauczycieli
        * day: dzień nowej pozycji przedmiotu
        * lesson_index: indeks nowej pozycji przedmiotu

    * Użycie:
    : sprawdza, czy nauczyciele na nowej pozycji mają już lekcje.
    Ta funkcja służy do sprawdzania, czy możliwa jest zmiana pozycji przedmiotu

    * Zwraca:
    : True/False w zależności od tego, czy nauczyciele mają już lekcje na podanej pozycji

  * ### check_teacher_conditions
    * ***Parametry***:
        * teachers_id: identyfikatory nauczycieli
        * day: dzień nowej pozycji przedmiotu nauczyciela
        * days: lista dni
        * lesson_index: indeks nowej pozycji przedmiotu
        * teachers: lista wszystkich nauczycieli

    * Użycie:
    : jeśli nauczyciel miał przedmiot na podanej pozycji, czy byłby konflikt z jego warunkami pracy

    * Zwraca:
    : True, jeśli warunki są spełnione; w przeciwnym razie False
