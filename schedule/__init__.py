import random
from tkinter_schedule_vis import tkinter_schedule_vis
import datetime
from settings import settings


class Schedule:
    def __init__(self):
        self.school_schedule = {}

    from .general import create_class_schedule, print_debug, move_subject_to_day, swap, get_same_time_subject
    from .returncondition import is_teacher_taken

    create_class_schedule = staticmethod(create_class_schedule)

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

                    days_with_teacher_conflict = set()
                    while True:
                        if days_with_teacher_conflict == set(days):
                            return self.create(classes_id, conditions, days, subject_per_class)

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

                        interference = False
                        for same_time_subject in same_time_subjects:
                            if same_time_subject.teacher_id == subject.teacher_id:
                                if settings.DEBUG:
                                    print(
                                        "INTERFERENCE",
                                        f"teacher_id: {subject.teacher_id}, subject_id: {subject.subject_id},"
                                        f" other subject_id: {same_time_subject.subject_id}\n"
                                        f"day: {day}, class: {class_id}"
                                        f" subject_num: {subject_num} subject_iteration: {i}\n"
                                    )
                                    interference = True
                                    break

                            if settings.DEBUG:
                                print(
                                    f"teacher_id: {subject.teacher_id}, subject_id: {subject.subject_id},"
                                    f" other subject_id: {same_time_subject.subject_id}\n"
                                    f"day: {day}, class: {class_id} subject_num: {subject_num} subject_iteration: {i}\n"
                                )

                        if interference:
                            days_with_teacher_conflict.add(day)
                            continue

                        if len(new_class_schedule[day]) >= conditions.general['max_lessons_per_day']:
                            days_with_teacher_conflict.add(day)
                        else:
                            subject.lesson_hours_id = next_lesson_index
                            new_class_schedule[day].append(subject)
                            tkinter_schedule_vis(self.school_schedule, days,
                                                 capture_name=f'{class_id}_{subject_num}_{i}', dir_name=current_time)
                            break

        return self
