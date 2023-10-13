from loadData import *
from scheduleConditions import *
from subject import *
from schoolClass import *
from common import *
import pandas as pd
from schedule import *
import random

# TODO-LIST:
# ---------------------------------------------------------------------------------------------------------------------
# nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

# przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
# pozwolenie na dany przedmiot
# nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy

# sprawdzic czy jakis dzien ma mniej lekcji niz minimum
# jesli tak to znalezc dzien z najwieksza iloscia lekcji i przeniesc jeden przedmiot do tego dnia

# implementacja grup w głównym loopie

# zamiana używania classes_id na używanie listy klas z pełnymi informacjami
# ---------------------------------------------------------------------------------------------------------------------


def generate_schedule(data, days, conditions_file_path):
    """
    :param data: list of data in strict order of: [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df]
    :param days: list of days that the lessons can occur
    :param conditions_file_path: path to file with list of conditions to satisfy with the schedule
    :return: generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    """
    conditions = ScheduleConditions(conditions_file_path)
    [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df] = data

    classes_id = SchoolClass.get_classes_id(classes_df)
    school_classes = SchoolClass.get_school_classes(classes_df, classes_id)

    subject_per_class = split_subject_per_class(subjects_df, school_classes)

    if not conditions.valid:
        return -1

    new_school_schedule_object = Schedule().create(
        classes_id=classes_id,
        conditions=conditions,
        days=days,
        subject_per_class=subject_per_class
    )

    conditions.update_min_day_len(schedule=new_school_schedule_object, days=days)

    if settings.DEBUG:
        new_school_schedule_object.print(classes_id, days, print_subjects=False)

    return new_school_schedule_object


ss = generate_schedule(
    data=load_data(),
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    conditions_file_path='./conditions.txt'
)
