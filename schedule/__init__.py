import random
from tkinter_schedule_vis import tkinter_schedule_vis
import datetime
from settings import settings


class Schedule:
    def __init__(self):
        self.school_schedule = {}

    from .general import (create_class_schedule, print_debug, move_subject_to_day, swap, get_same_time_teacher,
                          find_first_lesson, get_num_of_lessons)
    from .returncondition import are_teachers_taken
    from .formatschedule import format_schedule

    create_class_schedule = staticmethod(create_class_schedule)
    format_schedule = staticmethod(format_schedule)
    find_first_lesson = staticmethod(find_first_lesson)
    get_num_of_lessons = staticmethod(get_num_of_lessons)

    def add_class_schedule(self, class_id, class_schedule):
        self.school_schedule[class_id] = class_schedule

    def create(self, classes_id, conditions, days, subject_per_class, log_file_name):
        for class_id_index, class_id in enumerate(classes_id):
            new_class_schedule = self.create_class_schedule(days)
            self.add_class_schedule(class_id, new_class_schedule)
            for subject_num, subject in enumerate(subject_per_class[class_id]):

                days_with_teacher_conflict = set()
                while True:
                    if days_with_teacher_conflict == set(days):
                        return self.create(classes_id, conditions, days, subject_per_class, log_file_name)

                    day = random.choice(days)
                    next_lesson_index = len(new_class_schedule[day])

                    if self.are_teachers_taken(subject.teachers_id, day, next_lesson_index, class_id):
                        days_with_teacher_conflict.add(day)
                        continue

                    if len(new_class_schedule[day]) >= conditions.general['max_lessons_per_day']:
                        days_with_teacher_conflict.add(day)
                    else:
                        subject.lesson_hours_id = next_lesson_index
                        new_class_schedule[day].append([subject])

                        if subject_num == len(subject_per_class[class_id]) - 1 and \
                                class_id_index == len(classes_id) - 1:
                            tkinter_schedule_vis(
                                self,
                                days,
                                capture_name=f'LastInitCapture',
                                dir_name=log_file_name,
                            )
                        break
        return self
