# schedule/general.py

Ten plik zawiera ogólne funkcje klasy Harmonogram

---

## Funkcje
  * ### create_class_schedule
    * ***Parametry***:
        * days: lista dni, w których mogą odbywać się lekcje

    * Zwraca:
    : pusty harmonogram dla podanych dni
  
  * ### move_subject_to_day
    * ***Parametry***:
        * class_id: id aktualnej klasy
        * day_to: dzień, na który przesunięto przedmiot
        * day_from: aktualna pozycja przedmiotu
        * subject_position: pozycja przedmiotu w dniu
        * subject_to_position: może być -1 lub indeksem pierwszej lekcji; 
      decyduje, gdzie przesunięto przedmiot

    * Użycie:
    : self.data[class_id] = class_schedule

    * Zwraca:
    : True, jeśli przesunięcie było udane, w przeciwnym razie False
  
  * ### swap_subject_in_groups
    * ***Parametry***:
        * group: id grupy (nie indeks)
        * subjects_list_x, subjects_list_y: przedmioty do zamiany miejscami

    * Użycie:
    : zamienia pozycje przedmiotów

    * Zwraca:
    : None
  
  * ### safe_move
    * ***Parametry***:
        * teachers_id: identyfikatory nauczycieli do sprawdzenia
        * day_from: dzień, z którego pobieramy przedmiot
        * day_to: dzień, do którego dodajemy przedmiot
        * subject_position: stara pozycja przedmiotu
        * subject_new_position: nowa pozycja, do której dodajemy przedmiot
        * class_id: klasa, do której przesunięto przedmiot
        * days: lista dni
        * teachers: lista wszystkich nauczycieli
        * group: grupa klasy do przemieszczenia
        * log_file_name: nazwa pliku dla informacji o działaniu

    * Użycie:
    : przed próbą przesunięcia za pomocą move_subject_to_day(), funkcja sprawdza, czy operacja jest możliwa
    i powiadamia program

    * Zwraca:
    : bool; czy operacja powiodła się

  * ### get_same_time_teacher
    * ***Parametry***:
        * day: dzień przedmiotu
        * lesson_index: indeks przedmiotu

    * Zwraca:
    : lista nauczycieli, którzy prowadzą lekcję w danym dniu o danym indeksie lekcji
  
  * ### get_same_time_classrooms
    * ***Parametry***:
        * day: dzień przedmiotu
        * lesson_index: indeks przedmiotu

    * Zwraca:
    : lista sal lekcyjnych, w których odbywa się lekcja w danym dniu o danym indeksie lekcji

  * ### get_stacked_lessons
    * ***Parametry***:
        * class_id: id klasy
        * day: dzień przedmiotu
        * group: grupa przedmiotu
        * lesson_index: indeks przedmiotu; jeśli == 0, to domyślnie przyjmuje pierwszy indeks lekcji
        * log_file_name: nazwa pliku dla informacji o działaniu

    * Użycie:
    : sprawdza, czy przedmiot osiągnął limit max_stack

    * Zwraca:
    : lista tego samego typu przedmiotów kolejno, ostatnie indeksy godzin lekcyjnych w stosie

  * ### find_another_grouped_lessons
    * ***Parametry***:
        * class_id: id klasy
        * lesson_day: dzień przedmiotu
        * number_of_groups: liczba grup tego przedmiotu
        * lesson_index: indeks przedmiotu
        * days: lista dni

    * Użycie:
    : sprawdza, czy któraś lekcja jest podzielona na grupy, 
    jest to dla zamiany grupowanej lekcji, aby nauczyciel nie miał 2 lekcji równocześnie

    * Zwraca:
    : lista lekcji grupowanych, które można zamienić z inną lekcją grupowaną

  * ### find_first_lesson_index
    * ***Parametry***:
        * schedule_at_day: schedule[klasa_id][dzień]
        * log_file_name
    
    * Użycie:
    : znajduje pierwszy indeks lekcji, jeśli jest pusty przedmiot, indeks nie będzie równy 0
    
    * Zwraca:
    : indeks lub None, jeśli dzień jest pusty

  * ### get_num_of_lessons
    * ***Parametry***:
        * schedule_at_day: schedule[klasa_id][dzień]
        * log_file_name
    
    * Zwraca:
    : liczba niepustych lekcji w danym dniu
