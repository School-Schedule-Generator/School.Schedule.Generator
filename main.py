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

# read data


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

    subject_per_class_df = {}
    for class_id in classes_id:
        subject_per_class_df[class_id] = subjects_df.loc[subjects_df['class_ID'] == class_id]

    subject_per_class = split_subject_per_class(subjects_df, subject_per_class_df)


    if not conditions.valid:
        return -1

    school_schedule = Schedule()

    for class_id in classes_id:

        new_class_schedule = school_schedule.create_class_schedule(days)
        for subject in subject_per_class[class_id]:
            for i in range(subject.subject_count_in_week):
                day = random.choice(days)
                while len(new_class_schedule[day]) >= conditions.general['max_lessons_per_day']:
                    day = random.choice(days)

                subject.lesson_hours_id = len(new_class_schedule[day])
                new_class_schedule[day].append(subject)

        school_schedule.add_class_schedule(new_class_schedule)

    if settings.DEBUG:
        school_schedule.print(school_schedule, classes_id, days, print_subjects=False)

generate_schedule(
    data = loadData(),
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    conditions_file_path = './conditions.txt'
)
