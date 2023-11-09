from subject import Subject
from settings import settings
from debug_log import *

def create_class_schedule(days):
    """
    :param days: list of days that the lessons can be in
    :return: empty schedule of passed in days
    """
    new_class_schedule = {}
    for day in days:
        new_class_schedule[day] = []
    return new_class_schedule


def print_debug(log_file_name, self, classes_id, days, print_subjects=False):
    for i, class_schedule in enumerate(self.school_schedule):
        debug_log(log_file_name, f'class {classes_id[i]}')
        for j in range(len(class_schedule)):
            debug_log(log_file_name, f'\t{days[j]}\n\t\tlen={len(class_schedule[days[j]])}')
            if print_subjects:
                for subject in class_schedule[days[j]]:
                    debug_log(log_file_name, f'\t\t{subject.subject_name_id} teacher:{subject.teacher_id}')
            debug_log(log_file_name, '\n')
        debug_log(log_file_name, '-' * 10)


def move_subject_to_day(self, class_id, day_to, day_from, subject_position, log_file_name):
    old = self.school_schedule[class_id][day_from][subject_position]
    if old.is_empty:
        debug_log(log_file_name, "ERROR: can't move empty space")
        return False

    first_lesson = find_first_lesson(self.school_schedule[class_id][day_from], log_file_name=log_file_name)

    if subject_position == first_lesson:
        self.school_schedule[class_id][day_from][first_lesson] = Subject(is_empty=True, lesson_hours_id=first_lesson)
    elif subject_position == -1:
        self.school_schedule[class_id][day_from].pop()
    else:
        debug_log(log_file_name, "ERROR: you can only move 1st and last lesson")
        return False

    self.school_schedule[class_id][day_to].append(old)
    if len(self.school_schedule[class_id][day_to]) > 1:
        if subject_position == first_lesson:
            self.school_schedule[class_id][day_to][-1].lesson_hours_id = len(self.school_schedule[class_id][day_to])-1
        else:
            self.school_schedule[class_id][day_to][-1].lesson_hours_id = \
                self.school_schedule[class_id][day_to][subject_position-1].lesson_hours_id + 1
    elif len(self.school_schedule[class_id][day_to]) == 1:
        self.school_schedule[class_id][day_to][subject_position].lesson_hours_id = 1
    else:
        self.school_schedule[class_id][day_to][subject_position].lesson_hours_id = 0
    return True


def get_same_time_teacher(self, day, lesson_index):
    temp = []
    for other_class_schedule_id in self.school_schedule:
        other_class_schedule_day = self.school_schedule[other_class_schedule_id][day]
        try:
            other_class_subject = other_class_schedule_day[lesson_index]
            temp.append(other_class_subject.teacher_id)
        except IndexError:
            pass
    return temp


def swap(self, class_id, day_x, subject_x_position, day_y, subject_y_position):
    (
        self.school_schedule[class_id][day_x][subject_x_position].lesson_hours_id,
        self.school_schedule[class_id][day_y][subject_y_position].lesson_hours_id
    ) = (
        self.school_schedule[class_id][day_y][subject_y_position].lesson_hours_id,
        self.school_schedule[class_id][day_x][subject_x_position].lesson_hours_id
    )

    (
        self.school_schedule[class_id][day_x][subject_x_position],
        self.school_schedule[class_id][day_y][subject_y_position]
    ) = (
        self.school_schedule[class_id][day_y][subject_y_position],
        self.school_schedule[class_id][day_x][subject_x_position]
    )

def find_first_lesson(schedule_at_day, log_file_name):
    for i, subject in enumerate(schedule_at_day):
        if subject.is_empty:
            debug_log(log_file_name, 'DEBUG: empty cell')
        else:
            return i
    return None

def get_num_of_lessons(schedule_at_day, log_file_name):
    first_lesson_index = find_first_lesson(schedule_at_day, log_file_name)
    return len(schedule_at_day[first_lesson_index:])