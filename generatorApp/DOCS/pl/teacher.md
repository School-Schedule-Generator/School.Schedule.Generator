# teacher.py

Ten plik zawiera klasę Teacher

---

## Teacher
* ### Parametry:
    * name: imię nauczyciela
    * surname: nazwisko nauczyciela
    * possible_subjects: lista przedmiotów, które nauczyciel może nauczać
    * start_hour_index: id godziny, decyduje o rozpoczęciu lekcji przez nauczyciela (może zaczynać później)
    * end_hour_index: id godziny, decyduje o zakończeniu lekcji przez nauczyciela (może kończyć wcześniej)

## create_teachers
  * ***Parametry***:
      * teachers_df: dataframe wszystkich nauczycieli

  * Użycie:
  : zamienia dane z pandas df na instancje klasy  

  * Zwraca:
  : słownik zawierający każdego nauczyciela, klucz - teacher_id
