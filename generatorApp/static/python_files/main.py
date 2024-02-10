from datetime import datetime
from itertools import product
from load_data import *
from schedule_conditions import *
from school_class import *
from schedule import *
from classroom import *
from subject import *
from teacher import *
from tkinter_schedule_vis import *

import tkinter_schedule_vis

# TODO-LIST:
# ---------------------------------------------------------------------------------------------------------------------

# WEB
# ***********
    # checking conditions passed in by user (ilosc godzin lekcyjnych nauczyciela w planie z iloscia leckji mozliwych wedlug conditions)

    # nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

    # przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
    # pozwolenie na dany przedmiot
    # nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy

    # zmienianie dni w których mogą być lekcje
# ***********

# ---------------------------------------------------------------------------------------------------------------------


def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)


def generate_schedule(data, days, min_lessons_per_day, max_lessons_per_day, log_file_name):
    """
    :param data: list of data in strict order of: [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df]
    :param days: list of days that the lessons can occur
    :param log_file_name: current time for logging
    :param min_lessons_per_day: minimum number of lessons per day
    :param max_lessons_per_day: maximum number of lessons per day
    :return: generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    """

    # Creating directory for log files
    if settings.SAVELOG:
        if not os.path.exists(f'logs/{log_file_name}'):
            os.makedirs(f'logs/{log_file_name}')
        with open(f'logs/{log_file_name}/{log_file_name}.txt', 'w') as f:
            pass

    # Creating global schedule conditions
    conditions = ScheduleConditions(min_lessons_per_day=min_lessons_per_day, max_lessons_per_day=max_lessons_per_day)

    schedule = False
    for i, days_order in enumerate(permutations(days, len(days))):
        version = i

        # splitting data to separate dataframes
        [
            _,
            _,
            subjects_df,
            teachers_df,
            classes_df,
            classrooms_df,
            _
        ] = copy.deepcopy(data)

        # gathering basic information from dataframes
        classes_id, classes_start_hour_index = SchoolClass.get_classes_data(classes_df)
        teachers = create_teachers(teachers_df)
        subjects = split_subjects(subjects_df, teachers, classes_id)
        classrooms = create_classrooms(classrooms_df)

        schedule = Schedule(version=version).create(
            classes_id=classes_id,
            classes_start_hour_index=classes_start_hour_index,
            conditions=conditions,
            days=days,
            days_ordered=days_order,
            subjects=subjects,
            teachers=teachers,
            log_file_name=log_file_name
        ).split_to_groups(
            days,
            conditions,
            log_file_name
        ).format_schedule(
            conditions,
            days=days,
            teachers=teachers,
            classrooms=classrooms,
            classes_id=classes_id,
            classes_start_hour_index=classes_start_hour_index,
            days_ordered=days_order,
            log_file_name=log_file_name
        )
        debug_log(log_file_name, f"Version: {version}, Valid: {schedule.valid}, Day order: {days_order}")

        if schedule.valid:
            break

    # schedule visualisation using tkinter
    if not tkinter_schedule_vis.tkinter_schedule_vis(
        schedule=schedule,
        days=days,
        dir_name=f'{log_file_name}',
        capture_name='FinalCapture',
    ):
        debug_log(log_file_name, 'DEBUG: no tkinter generated')

    return schedule.data


now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
data = load_data()

ss = generate_schedule(
    data=data,
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    min_lessons_per_day=7,
    max_lessons_per_day=10,
    log_file_name=time_str
)

file_path = f'../data/schedule_{time_str}'
info = {'Title': 'Test Schedule', 'Time': time_str, 'Path': file_path}
schedule_to_excel(schedule_to_json(ss, file_path), data, info, file_path)
