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
    # try to create new schedule when there is no possible one with current setup
    # checking conditions passed in by user (ilosc godzin lekcyjnych nauczyciela w planie z iloscia leckji mozliwych wedlug conditions)
# ***********

# GROUPING:
# ***********
    # make grouping suitable for teachers conditions (check for day that the teacher can have lessons in)
# ***********

# CREATE
# ***********
    # generacja na podstawie teachers
        # dodać do tabeli teachers kolumny start lesson, end lesson, dni (w których dniach nauczyciel może mieć lekcje)
# ***********

# WEB
# ***********
    # nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

    # przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
    # pozwolenie na dany przedmiot
    # nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy

    # sprawdzanie czy user wpisał poprawne dane (np w ograniczaniu dni nauczycieli)
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

    # splitting data to separate dataframes
    [lesson_hours_df, subject_names_df, subjects_df, teachers_df, classes_df, classrooms_df] = data

    # gathering basic information from dataframes
    classes_id = SchoolClass.get_classes_id(classes_df)
    school_classes = SchoolClass.get_school_classes(classes_df, classes_id)
    subject_per_class = split_subject_per_class(subjects_df, school_classes)
    teachers = create_teachers(teachers_df)

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
    if not tkinter_schedule_vis.tkinter_schedule_vis(
        schedule_obj=new_school_schedule_object,
        days=days,
        dir_name=f'{log_file_name}',
        capture_name='FinalCapture'
    ):
        debug_log(log_file_name, 'DEBUG: no tkinter generated')

    return new_school_schedule_object


now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
ss = generate_schedule(
    data=load_data(),
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    conditions_file_path='./conditions.txt',
    log_file_name=time_str
)
