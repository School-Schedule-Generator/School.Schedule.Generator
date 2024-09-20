### Utwórz rozszerzenia

Aby napisać rozszerzenia, najpierw zapoznaj się z projektem, czytając dokumentację plików, a następnie postępuj zgodnie z tym samouczkiem.

Najpierw pobierz gałąź projektu z GitHub jako zip lub sklonuj ją za pomocą tego polecenia:
`git clone -b generator git@github.com:School-Schedule-Generator/School.Schedule.Generator.git`  

Następnie, używając pip (lub innego instalatora pakietów), pobierz wymagania z pliku requirements.txt
`pip install -r requirements.txt`  

#### Jesteśmy gotowi do działania!

Twoje rozszerzenie będzie umieszczone w katalogu schedule/format/

Najpierw otwórz szablon (template.py); oto kod wewnątrz niego:
```python
def <FUNCTION NAME>(self, <PARAMETERS>, log_file_name):
	
    # don't delete
    if self.valid is False:
        return self

    # YOUR LOGIC HERE

    return self # don't delete
```

Ustaw nazwę funkcji, a następnie skopiuj szablon do tego katalogu i zmień jego nazwę na taką samą jak nazwa funkcji.  
Jako parametry ustaw wszystkie dataframes i obiekty dostarczone przez funkcję format_schedule (w schedule/format/format_schedule.py).  
np.:
```python
def update_min_day_len(self, conditions, days, teachers, log_file_name):
```

Przejdź do pliku schedule/__init__.py i zaimportuj swoją funkcję do klasy w ten sposób:  
```python
class Schedule:
    (...)
    from .format.update_min_day_len import update_min_day_len
    
    from .format.<FUNCTION NAME> import <FUNCTION NAME>
```

Następnie przejdź do pliku schedule/format/format_schedule.py i dodaj implementację swojej funkcji (ze wszystkimi parametrami) do instrukcji return po innych funkcjach format oddzielonych 
"." w ten sposób:  
```python
return self.update_min_day_len(
        conditions,
        days,
        teachers,
        log_file_name
    ).add_classrooms(
        classrooms,
        teachers,
        days
    ).<FUNCTION NAME>(
        <PARAMETERS>, 
        log_file_name
    )
```

#### I to w zasadzie wszystko
Jeśli masz jakiekolwiek problemy, pamiętaj, że możesz użyć każdej funkcji dostarczonej przez nas w schedule.  
np.:
```python
    self.get_num_of_lessons(schedule_at_day, log_file_name)
```

Dziękujemy za wybór naszego programu :)  
Jeśli stworzysz jakieś fajne rozszerzenie, skontaktuj się z nami, to dodamy je do programu.
