import copy
import random
import pandas as pd
from debug_log import debug_log
from tkinter_schedule_vis import tkinter_schedule_vis
from math import ceil


class Schedule:
    from .general import (create_class_schedule, move_subject_to_day, swap_subject_in_groups, safe_move,
                          get_same_time_teacher, find_first_lesson_index, get_num_of_lessons,
                          find_another_grouped_lessons)
    from .returncondition import are_teachers_taken, check_teacher_conditions
    from .formatschedule import format_schedule

    create_class_schedule = staticmethod(create_class_schedule)
    find_first_lesson_index = staticmethod(find_first_lesson_index)
    get_num_of_lessons = staticmethod(get_num_of_lessons)
    check_teacher_conditions = staticmethod(check_teacher_conditions)

    def __init__(self, version):
        self.version = version
        self.data = {}
        self.valid = True

    def push_class_schedule(self, class_id, class_schedule):
        """
        :param class_id: id of passed in class
        :param class_schedule: schedule of class to push
        """
        self.data[class_id] = class_schedule

    def create(self, classes_id, conditions, days, days_ordered, subjects, teachers, teachers_order, log_file_name):
        """
        :param classes_id: list of ids
        :param conditions: global conditions of schedule
        :param days: list of days with lessons in
        :param days_ordered: list of days but with order wich in the teachers are added in
        :param subjects: splited per teacher splited per class subjects
        :param teachers: list of teachers (obj)
        :param teachers_order: order in wich teachers are added (set to: -1 - random; 0 - ascending; 1 - descending)
        :param log_file_name: file name for run information
        :return: structured and logical schedule
        """

        if self.valid is False:
            return self

        def avg_subjects_per_day(num_of_days) -> dict:
            avg_subjects = {}
            for day in days:
                avg_subjects[day] = {}
                for class_id in classes_id:
                    avg_subjects[day][class_id] = 0

            for day_i, day in enumerate(days):
                for teacher_id, subjects_list in subjects.items():
                    for class_id, values in subjects_list.items():
                        if teachers[teacher_id].days[day_i]:
                            avg_subjects[day][class_id] += len(values)

            for day in days:
                for class_id in classes_id:
                    avg_subjects[day][class_id] /= num_of_days

            return avg_subjects

        def map_teachers():
            data = {'id': list(teachers.keys()), 'value': list(teachers.values())}
            df = pd.DataFrame(data)
            mapped = {}
            for i, day in enumerate(days):

                teachers_at_day = df[df['value'].apply(lambda x: x.days[i] == 1)]['id'].tolist()

                teachers_at_day_subject_count = {}
                for teacher_id in teachers_at_day:
                    teachers_at_day_subject_count[teacher_id] = 0
                    for class_id in classes_id:
                        teachers_at_day_subject_count[teacher_id] += len(subjects[teacher_id][class_id])

                mapped[day] = teachers_at_day_subject_count
            return mapped

        tkcapture_count = 0
        mapped_teachers = map_teachers()

        for class_id in classes_id:
            self.data[class_id] = {}
            for day in days:
                self.data[class_id][day] = []

        for day_i, day in enumerate(days_ordered):
            avg_day_len = avg_subjects_per_day(len(days) - day_i)[day]

            if teachers_order == 0:
                teachers_at_order = dict(sorted(mapped_teachers[day].items(), key=lambda item: item[1]))
            elif teachers_order == 1:
                teachers_at_order = dict(sorted(mapped_teachers[day].items(), key=lambda item: item[1], reverse=True))
            elif teachers_order == -1:
                teachers_at_order = mapped_teachers[day]
            else:
                self.valid = False
                return self

            for teacher_id in teachers_at_order:
                if self.check_teacher_conditions(
                        teachers_id=teacher_id,
                        day=day,
                        days=days,
                        lesson_index=len(self.data[class_id][day]),
                        teachers=teachers
                ):
                    for class_id in classes_id:
                        for subject in subjects[teacher_id][class_id]:
                            lesson_index = len(self.data[class_id][day])
                            if (
                                len(self.data[class_id][day]) < ceil(avg_day_len[class_id])
                                and not self.are_teachers_taken(
                                    teachers_id=subject.teachers_id,
                                    day_to=day,
                                    lesson_index=lesson_index
                                )
                            ):
                                subject.lesson_hours_id = lesson_index
                                self.data[class_id][day].append([subject])
                                subjects[teacher_id][class_id].remove(subject)
                            else:
                                continue
            tkinter_schedule_vis(
                self,
                days,
                capture_name=f'create_{day_i}_{day}',
                dir_name=log_file_name,
            )

        return self

    def split_to_groups(self, days, conditions, log_file_name):
        """
        :param days: list of days used in schedule
        :param conditions: global conditions of schedule
        :param log_file_name: file name for run information
        :return: schedule with split subjects
        """

        if self.valid is False:
            return self

        # counting number of screenshots to avoid identical names of them
        tk_capture_count = 0

        # loop through all the classes to create separated schedules for them

        # deciding on how (if needed) to split groups based on number of teachers
        # if there is only one group we just need to write that information and reformat subject,
        #   which is done with every case
        # if there is 1 teacher we need to separate groups to avoid duplicate teacher conflict
        # else we can store two groups at the same time

        for class_id in self.data:
            class_schedule = self.data[class_id]
            for day in days:

                # loop trough subjects
                class_schedule_at_day = class_schedule[day]
                for subjects_list in class_schedule_at_day:
                    # we will reformat subjects from one class to list to be able to store multiple at once
                    subject = subjects_list[0]

                    if subject.number_of_groups == 1 or subject.is_empty:
                        subject.teachers_id = [subject.teachers_id[0]]
                        subject.group = 0
                    else:
                        # creating duplicates of subject, assigning to them different group ids and appending to list
                        for group in range(1, subject.number_of_groups):
                            new_subject = copy.deepcopy(subject)
                            new_subject.group = group + 1
                            if len(subject.teachers_id) > 1:
                                subject.teachers_id = [subject.teachers_id[group]]
                            subjects_list.append(new_subject)

                        # filling out the original subject with updated information
                        subject.teachers_id = [subject.teachers_id[0]]
                        subject.group = 1

                        # tkinter_schedule_vis(
                        #     self,
                        #     days,
                        #     capture_name=f'splitting_{tk_capture_count}',
                        #     dir_name=log_file_name,
                        # )
                        tk_capture_count += 1

        tk_capture_count = 0
        for class_id in self.data:
            class_schedule = self.data[class_id]
            for day in days:

                # loop trough subjects
                class_schedule_at_day = class_schedule[day]
                for subjects_list in class_schedule_at_day:
                    if len(subjects_list) <= 1:
                        continue

                    base_teacher = subjects_list[0].teachers_id[0]
                    same_teacher = True
                    for subject in subjects_list[1:]:
                        if not subject.teachers_id[0] == base_teacher:
                            same_teacher = False
                            break

                    if same_teacher:
                        for subject in subjects_list[1:]:
                            possibilities = self.find_another_grouped_lessons(class_id, day, subject.lesson_hours_id,
                                                                              subject.number_of_groups, days)

                            if len(possibilities) == 0:
                                debug_log('ERROR: no possible schedule with this setup')
                                return
                            else:
                                for another_day, another_index, another_subjects_list in possibilities:
                                    group_index = subject.group - 1
                                    if (
                                            base_teacher not in self.get_same_time_teacher(
                                        day_to=another_day,
                                        lesson_index=another_index,
                                    )
                                            and
                                            another_subjects_list[
                                                group_index].teachers_id not in self.get_same_time_teacher(
                                        day_to=day,
                                        lesson_index=subject.lesson_hours_id,
                                    )
                                    ):
                                        self.swap_subject_in_groups(
                                            group=subject.group,
                                            subjects_list_x=subjects_list,
                                            subjects_list_y=another_subjects_list
                                        )
                                        tkinter_schedule_vis(
                                            self,
                                            days,
                                            capture_name=f'grouping_{tk_capture_count}',
                                            dir_name=log_file_name,
                                        )
                                        tk_capture_count += 1
                                        break

        return self
