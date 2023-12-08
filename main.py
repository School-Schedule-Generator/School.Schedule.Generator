import copy
from datetime import datetime
from itertools import product
from settings import settings
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
    # create handling for no possible outcomes of current schedule
        # (esspecialy in update_min_day_len where there is infinite loop if there is no possible place to take subject from)
    # try to create new schedule when there is no possible one with current setup
    # checking conditions passed in by user (ilosc godzin lekcyjnych nauczyciela w planie z iloscia leckji mozliwych wedlug conditions)
# ***********

# WEB
# ***********
    # nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

    # przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
    # pozwolenie na dany przedmiot
    # nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy

    # sprawdzanie czy user wpisał poprawne dane (np w ograniczaniu dni nauczycieli)

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


def generate_schedule(data, days, conditions_file_path, log_file_name):
    """
    :param data: list of data in strict order of: [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df]
    :param days: list of days that the lessons can occur
    :param conditions_file_path: path to file with list of conditions to satisfy with the schedule
    :param log_file_name: current time for logging
    :return: generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    """

    # Creating directory for log files
    if not os.path.exists(f'logs/{log_file_name}'):
        os.makedirs(f'logs/{log_file_name}')
    with open(f'logs/{log_file_name}/{log_file_name}.txt', 'w') as f:
        pass

    # Creating global schedule conditions
    conditions = ScheduleConditions(file_path=conditions_file_path, log_file_name=log_file_name)
    if not conditions.valid:
        debug_log(log_file_name, 'Error: Passed in conditions had syntax error')
        return -1

    teachers_orders = [0, 1]
    if settings.RANDOM:
        teachers_orders.append(-1)

    schedule = False
    for i, days_order in enumerate(permutations(days, len(days))):
        for j, teachers_order in enumerate(teachers_orders):
            version = i*10+j

            # splitting data to separate dataframes
            [
                lesson_hours_df,
                subject_names_df,
                subjects_df,
                teachers_df,
                classes_df,
                classrooms_df
            ] = copy.deepcopy(data)

            # gathering basic information from dataframes
            classes_id = SchoolClass.get_classes_id(classes_df)
            teachers = create_teachers(teachers_df)
            subjects = split_subjects(subjects_df, teachers, classes_id)

            schedule = Schedule(version=version).create(
                classes_id=classes_id,
                conditions=conditions,
                days=days,
                days_ordered=days_order,
                subjects=subjects,
                teachers=teachers,
                teachers_order=teachers_order,
                log_file_name=log_file_name
            ).split_to_groups(
                days,
                conditions,
                log_file_name
            ).format_schedule(
                conditions,
                days=days,
                teachers=teachers,
                log_file_name=log_file_name
            )
            debug_log(log_file_name, f"Version: {version}, Valid: {schedule.valid}")
            if schedule.valid:
                break

        if schedule.valid:
            break

    # schedule visualisation using tkinter
    if not tkinter_schedule_vis.tkinter_schedule_vis(
        schedule=schedule,
        days=days,
        dir_name=f'{log_file_name}',
        capture_name='FinalCapture'
    ):
        debug_log(log_file_name, 'DEBUG: no tkinter generated')

    return schedule.data


now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
ss = generate_schedule(
    data=load_data(),
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    conditions_file_path='./conditions.txt',
    log_file_name=time_str
)
