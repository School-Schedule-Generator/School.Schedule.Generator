from loadData import *
from scheduleConditions import *
from subject import *
from schoolClass import *
from common import *
import pandas as pd
import random

# TODO-LIST:
# -------------------------------------------------------------------------------------
# nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

# przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
# pozwolenie na dany przedmiot
# nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy

# sprawdzic czy jakis dzien ma mniej lekcji niz minimum
# jesli tak to znalezc dzien z najwieksza iloscia lekcji i przeniesc jeden przedmiot do tego dnia
# -------------------------------------------------------------------------------------

# read data
[lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df] = loadData()


def generate_schedule():
    """
    :return: generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    """
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    classes_id = get_classes_id(classes_df)

    subject_per_class_df = {}
    for class_id in classes_id:
        subject_per_class_df[class_id] = subjects_df.loc[subjects_df['class_ID'] == class_id]

    subject_per_class = split_subject_per_class(subjects_df, subject_per_class_df)

    conditions = ScheduleConditions('./conditions.txt')
    if not conditions.valid:
        return -1

    school_schedule = []

    for class_id in classes_id:
        schedule = create_schedule(days)
        for subject in subject_per_class[class_id]:
            for i in range(subject.subject_count_in_week):
                day = random.choice(days)
                while len(schedule[day]) >= conditions.general['max_lessons_per_day']:
                    day = random.choice(days)

                subject.lesson_hours_id = len(schedule[day])
                schedule[day].append(subject)

        school_schedule.append(schedule)

    if True: #settings.DEBUG
        print_school_schedule(school_schedule, classes_id, days, print_subjects=True)

generate_schedule()
