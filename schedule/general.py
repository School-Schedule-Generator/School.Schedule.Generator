from subject import Subject
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


def log_schedule(self, days, log_file_name):
    schedule_by_hour_id = {}
    lesson_hours = set()
    for class_id in self.school_schedule:
        class_schedule = self.school_schedule[class_id]
        for day in days:
            class_schedule_at_day = class_schedule[day]
            for subjects in class_schedule_at_day:
                try:
                    schedule_by_hour_id[subjects[0].lesson_hours_id].append(subjects)
                except KeyError:
                    schedule_by_hour_id[subjects[0].lesson_hours_id] = [subjects]
                lesson_hours.add(subjects[0].lesson_hours_id)

    for lesson_hour in sorted(list(lesson_hours)):
        debug_log(log_file_name, '{0:>7}'.format(f'|{lesson_hour}. |'), end='')
        for subjects in schedule_by_hour_id[lesson_hour]:
            debug_log(log_file_name, ':', end='')
            for subject in subjects:
                debug_log(log_file_name, '{0:>10}'.format(f'{subject.teachers_id}, '))
            else:
                debug_log(log_file_name, '{0:>10}'.format(''))
            debug_log(log_file_name, ':', end='')
        debug_log(log_file_name, '|\n')


def move_subject_to_day(self, class_id, day_to, day_from, subject_position, log_file_name):
    old = self.school_schedule[class_id][day_from][subject_position]
    if old[0].is_empty:
        debug_log(log_file_name, "ERROR: can't move empty space")
        return False

    first_lesson = find_first_lesson(self.school_schedule[class_id][day_from], log_file_name=log_file_name)

    if subject_position == first_lesson:
        self.school_schedule[class_id][day_from][first_lesson] = [Subject(is_empty=True, lesson_hours_id=first_lesson)]
    elif subject_position == -1:
        self.school_schedule[class_id][day_from].pop()
    else:
        debug_log(log_file_name, "ERROR: you can only move 1st and last lesson")
        return False

    self.school_schedule[class_id][day_to].append(old)
    if len(self.school_schedule[class_id][day_to]) > 1:
        if subject_position == first_lesson:
            for subject in self.school_schedule[class_id][day_to][-1]:
                subject.lesson_hours_id = (len(self.school_schedule[class_id][day_to])-1)

        else:
            for subject in self.school_schedule[class_id][day_to][-1]:
                subject.lesson_hours_id = \
                    self.school_schedule[class_id][day_to][subject_position - 1][0].lesson_hours_id + 1

    elif len(self.school_schedule[class_id][day_to]) == 1:
        for subject in self.school_schedule[class_id][day_to][-1]:
            subject.lesson_hours_id = 1

    else:
        for subject in self.school_schedule[class_id][day_to][-1]:
            subject.lesson_hours_id = 0

    return True


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


def get_same_time_teacher(self, day, lesson_index, class_id):
    same_time_teachers = []
    for class_schedule_id in self.school_schedule:
        if class_id == class_schedule_id:
            continue
        class_schedule_day = self.school_schedule[class_schedule_id][day]
        try:
            class_subjects = class_schedule_day[lesson_index]
            for class_subject in class_subjects:
                for teacher_id in class_subject.teachers_id:
                    same_time_teachers.append(teacher_id)
        except IndexError:
            pass
    return same_time_teachers


def find_first_lesson(schedule_at_day, log_file_name):
    for i, subjects in enumerate(schedule_at_day):
        for subject in subjects:
            if subject.is_empty:
                debug_log(log_file_name, 'DEBUG: empty cell')
            else:
                return i
    return None


def get_num_of_lessons(schedule_at_day, log_file_name):
    first_lesson_index = find_first_lesson(schedule_at_day, log_file_name)
    return len(schedule_at_day[first_lesson_index:])
