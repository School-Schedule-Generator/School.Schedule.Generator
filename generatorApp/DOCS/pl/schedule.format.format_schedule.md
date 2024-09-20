# schedule/format/format_schedule.py

Ten plik zawiera funkcję format_schedule

---

## format_schedule
  * ***Parametry***:
      * conditions: obiekt warunków
      * teachers: lista wszystkich nauczycieli w harmonogramie
      * classrooms: lista wszystkich sal lekcyjnych w harmonogramie
      * classes_id: lista wszystkich identyfikatorów klas
      * days_ordered: kolejność dni, w których dodawane są lekcje
      * days: lista dni
      * log_file_name
    
  * Użycie:
  : łączy każdą *ekspansję* 
  (funkcję operującą na już wygenerowanym harmonogramie)
    
  * Zwraca:
  : self
