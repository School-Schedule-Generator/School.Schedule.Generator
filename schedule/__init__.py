import copy
import numpy as np
import pandas as pd
from debug_log import debug_log
from tkinter_schedule_vis import tkinter_schedule_vis
from math import ceil
from subject import Subject


class Schedule:
    from .general import (create_class_schedule, move_subject_to_day, swap_subject_in_groups, safe_move,
                          get_same_time_teacher, find_first_lesson_index, get_num_of_lessons,
                          find_another_grouped_lessons, get_same_time_classrooms, get_stacked_lessons)
    from .return_condition import are_teachers_taken, check_teacher_conditions
    from .format.format_schedule import format_schedule
    from .format.add_classrooms import add_classrooms
    from .format.update_min_day_len import update_min_day_len

    create_class_schedule = staticmethod(create_class_schedule)
    find_first_lesson_index = staticmethod(find_first_lesson_index)
    get_num_of_lessons = staticmethod(get_num_of_lessons)
    check_teacher_conditions = staticmethod(check_teacher_conditions)

    def __init__(self, version=-1, valid=True):
        self.version = version
        self.data = {}
        self.valid = valid

    def push_class_schedule(self, class_id, class_schedule):
        """
        :param class_id: id of passed in class
        :param class_schedule: schedule of class to push
        """
        self.data[class_id] = class_schedule

    def create(self, classes_id, classes_start_hour_index, conditions, days, days_ordered, subjects, teachers, log_file_name):
        """
        :param classes_id: list of ids
        :param classes_start_hour_index: dict of hours when class starts
        :param conditions: global conditions of schedule
        :param days: list of days with lessons in
        :param days_ordered: list of days but with order wich in the teachers are added in
        :param subjects: split per teacher split per class subjects
        :param teachers: list of teachers (obj)
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
            teachers_data = {'id': list(teachers.keys()), 'value': list(teachers.values())}
            teachers_df = pd.DataFrame(teachers_data)
            mapped = {}
            for day_i, day in enumerate(days):

                teachers_at_day = teachers_df[teachers_df['value'].apply(lambda x: x.days[day_i] == 1)].copy()

                teachers_at_day['start_hour_index'] = teachers_at_day['value'].apply(lambda x: x.start_hour_index[day_i])
                teachers_at_day['end_hour_index'] = teachers_at_day['value'].apply(lambda x: x.end_hour_index[day_i])

                teachers_at_day['score'] = np.nan

                for i, row in teachers_at_day.iterrows():
                    score = None
                    if row['start_hour_index'] == 0 and row['end_hour_index'] == -1:
                        score = -1
                    elif row['start_hour_index'] != 0 and row['end_hour_index'] != -1:
                        score = row['end_hour_index'] - row['start_hour_index'] - 1
                    elif row['end_hour_index'] != -1:
                        score = 10 - row['end_hour_index']
                    elif row['start_hour_index'] != 0:
                        score = 5 + row['start_hour_index']

                    teachers_at_day.at[i,'score'] = score

                teachers_at_day.sort_values(by='score', inplace=True, ascending=False)

                mapped[day] = teachers_at_day['id']
            return mapped

        def is_subjects_empty():
            empty = True
            count_of_subjects = 0
            s = []
            for teacher_id in teachers.keys():
                for class_id in classes_id:
                    if len(subjects[teacher_id][class_id]) != 0:
                        count_of_subjects += len(subjects[teacher_id][class_id])
                        for sub in subjects[teacher_id][class_id]:
                            s.append((teacher_id, sub.subject_id))
                        empty = False
            debug_log(log_file_name, f'count {count_of_subjects}, subjects: {s}')
            return empty, count_of_subjects, s

        def add_subjects(iteration, stack_handle):
            first_iter = not iteration

            for day_i, day in enumerate(days_ordered):

                avg_day_len = avg_subjects_per_day(len(days) - day_i)[day]

                last_class_id = None
                last_subject_id = None

                for teacher_id in map_teachers()[day]:
                    for class_id in classes_id:
                        if self.check_teacher_conditions(
                                teachers_id=teacher_id,
                                day=day,
                                days=days,
                                lesson_index=len(self.data[class_id][day]),
                                teachers=teachers
                        ):
                            subject_stack = 0
                            for subject in subjects[teacher_id][class_id]:
                                if not subject.subject_id in stack_handle[day].keys():
                                    stack_handle[day][subject.subject_id] = False

                                if first_iter:
                                    if last_subject_id is None:
                                        last_subject_id = subject.subject_id

                                    if last_class_id is None:
                                        last_class_id = subject.class_id

                                    if subject.subject_id != last_subject_id:
                                        stack_handle[day][last_subject_id] = 'EXISTS_IN_DAY'

                                    if stack_handle[day][subject.subject_id] == 'EXISTS_IN_DAY':
                                        last_class_id = subject.class_id
                                        last_subject_id = subject.subject_id
                                        continue

                                if subject.class_id == last_class_id and subject.subject_id == last_subject_id:
                                    subject_stack += 1

                                if stack_handle[day][subject.subject_id] == 'MAX_STACK_REACHED':
                                    last_class_id = subject.class_id
                                    last_subject_id = subject.subject_id
                                    continue
                                if subject.max_stack is None:
                                    pass
                                if subject_stack > subject.max_stack:
                                    stack_handle[day][subject.subject_id] = 'MAX_STACK_REACHED'
                                    last_class_id = subject.class_id
                                    last_subject_id = subject.subject_id
                                    continue

                                last_class_id = subject.class_id
                                last_subject_id = subject.subject_id

                                first_lesson_index = self.find_first_lesson_index(self.data[class_id][day], log_file_name)
                                lesson_index = len(self.data[class_id][day])

                                if (first_lesson_index is None or first_lesson_index == 0) and not self.data[class_id][day]:
                                    while lesson_index < teachers[teacher_id].start_hour_index[day_i]:
                                        self.data[class_id][day].append([Subject(is_empty=True)])
                                        lesson_index = len(self.data[class_id][day])

                                if (
                                        first_lesson_index is not None and first_lesson_index > 0
                                        and self.data[class_id][day][first_lesson_index-1][0].movable
                                        and (not first_iter or len(self.data[class_id][day]) < ceil(avg_day_len[class_id]))
                                        and self.get_num_of_lessons(self.data[class_id][day], log_file_name) < conditions.data['max_lessons_per_day']
                                        and not self.are_teachers_taken(
                                            teachers_id=subject.teachers_id,
                                            day_to=day,
                                            lesson_index=first_lesson_index - 1
                                        )
                                ):
                                    subject.lesson_hour_id = first_lesson_index - 1
                                    self.data[class_id][day][first_lesson_index-1] = [subject]
                                    for teacher_to_remove_id in subject.teachers_id:
                                        try:
                                            subjects[teacher_to_remove_id][subject.class_id].remove(subject)
                                        except ValueError:
                                            pass
                                elif (
                                        (not first_iter or len(self.data[class_id][day]) < ceil(avg_day_len[class_id]))
                                        and self.get_num_of_lessons(self.data[class_id][day], log_file_name) < conditions.data['max_lessons_per_day']
                                        and not self.are_teachers_taken(
                                            teachers_id=subject.teachers_id,
                                            day_to=day,
                                            lesson_index=lesson_index
                                        )
                                ):
                                    subject.lesson_hour_id = lesson_index
                                    self.data[class_id][day].append([subject])
                                    for teacher_to_remove_id in subject.teachers_id:
                                        try:
                                            subjects[teacher_to_remove_id][subject.class_id].remove(subject)
                                        except ValueError:
                                            pass
                                else:
                                    continue
                tkinter_schedule_vis(
                    self,
                    days,
                    capture_name=f'create_{iteration}_{day_i}_{day}',
                    dir_name=log_file_name,
                )

        for class_id in classes_id:
            self.data[class_id] = {}
            for day in days:
                self.data[class_id][day] = [[Subject(is_empty=True, movable=False)] for _ in range(classes_start_hour_index[class_id])]

        i = 0
        empty, count, _  = is_subjects_empty()
        old_count = count + 1

        stack_handle = {}
        for day in days:
            stack_handle[day] = {}

        while count < old_count:
            if empty:
                return self
            add_subjects(i, stack_handle)
            old_count = count
            empty, count, _ = is_subjects_empty()
            i += 1

        self.valid = False
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

                        tkinter_schedule_vis(
                            self,
                            days,
                            capture_name=f'splitting_{tk_capture_count}',
                            dir_name=log_file_name,
                        )
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
                            possibilities = self.find_another_grouped_lessons(class_id, day, subject.lesson_hour_id,
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
                                                group_index].teachers_id[0] not in self.get_same_time_teacher(
                                                    day_to=day,
                                                    lesson_index=subject.lesson_hour_id,
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
