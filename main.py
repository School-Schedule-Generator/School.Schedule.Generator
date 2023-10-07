import pandas as pd
import random

# read data from exel files
classes_df = pd.read_excel('./data/testData/SSG_CLASSES.xlsx')
classrooms_df = pd.read_excel('./data/testData/SSG_CLASSROOMS.xlsx')
lesson_hours_df = pd.read_excel('./data/testData/SSG_LESSON_HOURS.xlsx')
subject_names_df = pd.read_excel('./data/testData/SSG_SUBJECT_NAMES.xlsx')
subjects_df = pd.read_excel('./data/testData/SSG_SUBJECTS.xlsx')
teachers_df = pd.read_excel('./data/testData/SSG_TEACHERS.xlsx')

tables = [classes_df, classrooms_df, lesson_hours_df, subject_names_df, subjects_df, teachers_df]

# -------------------------------------------------------------------------------------
# nauczyciele i wychowacy wybierani z inputa usera na podstawie listy z teachers_db

# przy tworzeniu klas i subjektow user będzie miał wybór dla wychowacy/nauczyciela z tylko tych którzy mają w teachers
# pozwolenie na dany przedmiot
# nauczyciel zw musi być ustawiany na takiego który jest rzeczywiście wychowawcą danej klasy
# -------------------------------------------------------------------------------------


class ScheduleConditions:
    """
    class for conditionalising a schedule
    """
    def __init__(self, *args, min_lessons_per_day=5, max_lessons_per_day=9):
        self.max_lessons_per_day = max_lessons_per_day
        self.min_lessons_per_day = min_lessons_per_day

    def format_schedule(self, schedule):
        """
        :param schedule: schedule for all school classes
        :return: returns conditionalized schedule
        """
        pass


class SchoolClass:
    """
    class from classes dataframe turned into an object
    """
    def __init__(self, class_id, grade, class_signature, supervising_teacher):
        self.class_id = class_id
        self.grade = grade
        self.class_signature = class_signature
        self.supervising_teacher = supervising_teacher


class Subject:
    """
    subject from subjects dataframe turned into an object
    """
    def __init__(self, subject_id, subject_name_id, class_id, subject_count_in_week, number_of_groups, subject_length,
                 lesson_hours_id, teacher_id, classroom_id):
        self.subject_id = subject_id
        self.subject_name_id = subject_name_id
        self.class_id = class_id
        self.subject_count_in_week = subject_count_in_week
        self.number_of_groups = number_of_groups
        self.subject_length = subject_length
        self.lesson_hours_id = lesson_hours_id
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id


def get_classes_id(df):
    """
    :param df: dataframe of classes
    :return: list of classes ids
    """
    return df['Class_ID'].to_numpy()


def create_schedule(days):
    """
    :param days: list of days that the lessons can be in
    :return: empty schedule of passed in days
    """
    new_schedule = {}
    for day in days:
        new_schedule[day] = []
    return new_schedule


def split_subject_per_class(subject_per_class_df):
    """
    :param subject_per_class_df: list of dataframes of subjects per class
    :return: returns splitet into classes lists of subjects
    """
    subject_per_class = {}
    for class_df_id in subject_per_class_df:
        class_df = subject_per_class_df[class_df_id]
        subject_per_class[class_df_id] = [Subject(
            subject_id=subjects_df.loc[i, 'subject_ID'],
            subject_name_id=subjects_df.loc[i, 'subject_name_ID'],
            class_id=subjects_df.loc[i, 'class_ID'],
            subject_count_in_week=subjects_df.loc[i, 'subject_count_in_week'],
            number_of_groups=subjects_df.loc[i, 'number_of_groups'],
            teacher_id=subjects_df.loc[i, 'teacher_ID'],
            classroom_id=subjects_df.loc[i, 'classroom_ID'],
            subject_length=subjects_df.loc[i, 'subject_length'],
            lesson_hours_id=subjects_df.loc[i, 'lesson_hours_ID']
        ) for i in range(len(class_df))]
    return subject_per_class


def get_condition_list(file_path):
    """
    :param file_path: path
    :return: list of conditions written in a file
    """
    condition_raw = open(file_path, 'r')
    lines = condition_raw.readlines()
    conditions_list = []
    for i, line in enumerate(lines):
        condition = line.strip().split(':')
        try:
            conditions_list.append({'argument': condition[0], 'value': condition[1]})
        except IndexError:
            print(f'Passed in argument at line {i} is not fully defined')
    condition_raw.close()
    return conditions_list


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

    subject_per_class = split_subject_per_class(subject_per_class_df)

    condition_list = get_condition_list('./conditions.txt')
    conditions = ScheduleConditions(condition_list)

    for class_id in classes_id:
        schedule = create_schedule(days)
        for subject in subject_per_class[class_id]:
            for i in range(subject.subject_count_in_week):
                day = random.choice(days)
                while len(schedule[day]) == conditions.max_lessons_per_day:
                    day = random.choice(days)
                subject.lesson_hours_id = len(schedule[day])
                schedule[day].append(subject)


    #sprawdzic czy jakis dzien ma mniej lekcji niz minimum
    #jesli tak to znalezc dzien z najwieksza iloscia lekcji i przeniesc jeden przedmiot do tego dnia


generate_schedule()
