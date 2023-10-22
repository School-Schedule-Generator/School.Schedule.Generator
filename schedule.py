import random
from tkinter_schedule_vis import tkinter_schedule_vis
import datetime
import settings

class Schedule:
    def __init__(self):
        self.school_schedule = {}

    def add_class_schedule(self, class_id, class_schedule):
        self.school_schedule[class_id] = class_schedule

    def create(self, classes_id, conditions, days, subject_per_class):
        now = datetime.datetime.now()
        current_time = now.strftime("%H-%M-%S")

        for class_id in classes_id:
            new_class_schedule = self.create_class_schedule(days)
            self.add_class_schedule(class_id, new_class_schedule)

            for subject_num, subject in enumerate(subject_per_class[class_id]):
                for i in range(subject.subject_count_in_week):

                    while True:
                        day = random.choice(days)
                        next_lesson_index = len(new_class_schedule[day])

                        same_time_subjects = []
                        for other_class_schedule_id in self.school_schedule:
                            other_class_schedule_day = self.school_schedule[other_class_schedule_id][day]
                            try:
                                other_class_subject = other_class_schedule_day[next_lesson_index]
                                same_time_subjects.append(other_class_subject)
                            except IndexError:
                                pass

                        interfierence = False
                        for same_time_subject in same_time_subjects:
                            if same_time_subject.teacher_id == subject.teacher_id:
                                if settings.DEBUG:
                                    print(
                                        "INTERFIERENCE",
                                        f"teacher_id: {subject.teacher_id}, subject_id: {subject.subject_id}, other subject_id: {same_time_subject.subject_id}\n"
                                        f"day: {day}, class: {class_id} subject_num: {subject_num} subject_iteration: {i}\n"
                                    )
                                interfierence = True
                                break

                            if settings.DEBUG:
                                print(f"teacher_id: {subject.teacher_id}, subject_id: {subject.subject_id}, other subject_id: {same_time_subject.subject_id}\n"
                                      f"day: {day}, class: {class_id} subject_num: {subject_num} subject_iteration: {i}\n")

                        if interfierence:
                            continue

                        if len(new_class_schedule[day]) >= conditions.general['max_lessons_per_day']:
                            pass
                        else:
                            subject.lesson_hours_id = next_lesson_index
                            new_class_schedule[day].append(subject)
                            tkinter_schedule_vis(self.school_schedule, days, capture_name=f'{class_id}_{subject_num}_{i}', dir_name=current_time)
                            break

        return self

    @staticmethod
    def create_class_schedule(days):
        """
        :param days: list of days that the lessons can be in
        :return: empty schedule of passed in days
        """
        new_class_schedule = {}
        for day in days:
            new_class_schedule[day] = []
        return new_class_schedule

    def print(self, classes_id, days, print_subjects=False):
        for i, class_schedule in enumerate(self.school_schedule):
            print(f'class {classes_id[i]}')
            for j in range(len(class_schedule)):
                print(f'\t{days[j]}\n\t\tlen={len(class_schedule[days[j]])}')
                if print_subjects:
                    for subject in class_schedule[days[j]]:
                        print(f'\t\t{subject.subject_name_id} teacher:{subject.teacher_id}')
                print('\n')
            print('-' * 10)

    def move_subject_to_day(self, class_id, day_to, day_from, subject_position):
        self.school_schedule[class_id][day_to].append(
            self.school_schedule[class_id][day_from].pop(subject_position)
        )

    def swap(self, class_id, day_x, subject_x_position, day_y, subject_y_position):
        (
            self.school_schedule[class_id][day_x][subject_x_position],
            self.school_schedule[class_id][day_y][subject_y_position]
        ) = (
            self.school_schedule[class_id][day_y][subject_y_position],
            self.school_schedule[class_id][day_x][subject_x_position]
        )
