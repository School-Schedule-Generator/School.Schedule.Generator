from datetime import datetime
from loadData import *
from scheduleConditions import *
from schoolClass import *
from schedule import *
from tkinter_schedule_vis import *

import tkinter_schedule_vis

# TODO-LIST:
# ---------------------------------------------------------------------------------------------------------------------

# GENERAL:
# ***********
    # fix schedule text logging
# ***********

# CREATE
# ***********
    # implementacja subject_length -> lekcja ma się powtarzać tyle razy ile podane
# ***********

# WEB
# ***********
    # nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

    # przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
    # pozwolenie na dany przedmiot
    # nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy
# ***********

# GUPOWANIE
# ***********
    # Zmiana w dodawaniu(append) lekcji w fukcji create:
    # zamiast schedule.append(subject) dodawac liste schedule.append([subject])

    # zmienic zmienna z teacher_id na teachers_id jako liste nauczycieli
    # w trakcie sprawdzania nauczycieli sprawdzic wszystkich nauczycieli z listy

    # Grupowanie lekcji:
        # po initowaniu planu lekcji trzeba podzielić przedmiot(subject) na odpowiednią ilość grup
        # żeby podzielić grupy trzeba wiedzieć ilu nauczycieli obsuługuje dany przedmiot
        # jeśli liczba nauczycieli (ln) == ilość grup (ig) dublujemy lekcje w tym samym miejscu
            # [subject_id1_gr1, subject_id1_gr2, ...]
            # jeśli nauczyciel wywołuje konflikt wymieniamy lekcje danej grupy w tym miejscu na inną zgrupowaną lekcje odpowiednią dla tej grupy
            # jeśli i to nie jest możliwe stawiamy przedmiot dla danej grupy w innym miejscu traktując go jako osobny niezgrupowany przedmiot
        # jeśli ln == 1 przechodzimy odrazu do traktowania każdej lekcji jako osobny niezgrupowany obiekt pozostawiając tylko 1 grupe na orginalnej pozycji
# ***********

# ---------------------------------------------------------------------------------------------------------------------


def generate_schedule(data, days, conditions_file_path, log_file_name):
    """
    :param data: list of data in strict order of: [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df]
    :param days: list of days that the lessons can occur
    :param conditions_file_path: path to file with list of conditions to satisfy with the schedule
    :param log_file_name: current time for logging
    :return: generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    """

    # Creating directory and log files
    if not os.path.exists(f'logs/{log_file_name}'):
        os.makedirs(f'logs/{log_file_name}')
    with open(f'logs/{log_file_name}/{log_file_name}.txt', 'w') as f:
        pass
    with open(f'logs/{log_file_name}/{log_file_name}_schedule.txt', 'w') as f:
        pass

    # Creating global schedule conditions
    conditions = ScheduleConditions(file_path=conditions_file_path, log_file_name=log_file_name)
    if not conditions.valid:
        debug_log(log_file_name, 'Error: Passed in conditions had syntax error')
        return -1

    # splitting data to separate dataframes
    [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df] = data

    # gathering basic information from dataframes
    classes_id = SchoolClass.get_classes_id(classes_df)
    school_classes = SchoolClass.get_school_classes(classes_df, classes_id)
    subject_per_class = split_subject_per_class(subjects_df, school_classes)

    new_school_schedule_object = Schedule().create(
        classes_id=classes_id,
        conditions=conditions,
        days=days,
        subject_per_class=subject_per_class,
        log_file_name=log_file_name
    )

    new_school_schedule_object.split_to_groups(
        days,
        conditions,
        log_file_name
    )

    # applay complex conditions to schedule
    new_school_schedule_object.format_schedule(
        conditions,
        schedule=new_school_schedule_object,
        days=days,
        log_file_name=log_file_name
    )

    # schedule visualisation using tkinter
    tkinter_schedule_vis.tkinter_schedule_vis(
        schedule_obj=new_school_schedule_object,
        days=days,
        dir_name=f'{log_file_name}',
        capture_name='FinalCapture'
    )

    # new_school_schedule_object.log_schedule(days, log_file_name+'_schedule')

    return new_school_schedule_object


now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
ss = generate_schedule(
    data=load_data(),
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    conditions_file_path='./conditions.txt',
    log_file_name=time_str
)
