# subject.py

Ten plik zawiera klasę Subject

---

## Subject
* ### Parametry:
    * subject_id
    * subject_name_id: id nazwy
    * class_id: id klasy
    * number_of_groups: liczba grup, na które klasa jest podzielona dla tego przedmiotu
    * lesson_hour_id: id godziny lekcyjnej
    * teachers_id: id nauczyciela, jeśli None, domyślnie [-1]
    * classroom_id: id sali lekcyjnej
    * is_empty: jeśli True, ta instancja jest pustym przedmiotem 
      (używane do zrobienia miejsca przed lekcjami na początek zajęć)
    * max_stack: liczba określająca, ile przedmiotów tego typu może być kolejno
    * movable: decyduje, czy ten przedmiot można przesuwać
    * group: grupa, dla której jest ten przedmiot, gdy klasa jest podzielona na grupy
    * classroom_types: typ sali lekcyjnej

* ### Funkcje
  * ### split_subjects
      * ***Parametry***:
          * subjects_df: dataframe wszystkich przedmiotów
          * teachers: lista klas szkolnych
          * classes_id: lista id klas

      * Użycie:
      : zamienia dane z pandas df na instancje klasy  

      * Zwraca:
      : podzielone według nauczycieli i klas ([teacher_id][class_id]) listy przedmiotów
