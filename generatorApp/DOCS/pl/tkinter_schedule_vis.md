# school_class.py

Ten plik zawiera funkcję do wizualizacji harmonogramu podczas jego tworzenia

> [!UWAGA]  
> Najlepiej używać jej tylko w trybie DEBUG.

---

### tkinter_schedule_vis
  * ***Parametry***:
      * schedule: instancja harmonogramu
      * days: lista dni
      * capture: bool, decyduje, czy funkcja ma zrobić zrzut ekranu wygenerowanego harmonogramu
      * capture_name: nazwa zrzutu ekranu
      * dir_name: lokalizacja zapisu zrzutu ekranu 

  * Użycie:
  : generuje wizualizację harmonogramu

  * Zwraca:
  : True, jeśli proces zakończył się poprawnie, w przeciwnym razie False
