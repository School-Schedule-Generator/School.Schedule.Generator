import copy
import random
from tkinter_schedule_vis import tkinter_schedule_vis


class Schedule:
    from .general import (create_class_schedule, log_schedule, move_subject_to_day, swap_subject_in_place, safe_move,
                          get_same_time_teacher, find_first_lesson_index, get_num_of_lessons)
    from .returncondition import are_teachers_taken
    from .formatschedule import format_schedule

    create_class_schedule = staticmethod(create_class_schedule)
    format_schedule = staticmethod(format_schedule)
    find_first_lesson_index = staticmethod(find_first_lesson_index)
    get_num_of_lessons = staticmethod(get_num_of_lessons)

    def __init__(self):
        self.school_schedule = {}

    def push_class_schedule(self, class_id, class_schedule):
        """
        :param class_id: id of passed in class
        :param class_schedule: schedule of class to push
        """
        self.school_schedule[class_id] = class_schedule

    def create(self, classes_id, conditions, days, subject_per_class, log_file_name):
        """
        :param classes_id: list of ids
        :param conditions: global conditions of schedule
        :param days: list of days with lessons in
        :param subject_per_class: split into classes lists of subjects
        :param log_file_name: file name for run information
        :return: structured and logical schedule
        """

        # loop through all the classes to create separated schedules for them
        for class_id_index, class_id in enumerate(classes_id):
            # create empty class schedule to fill in
            new_class_schedule = self.create_class_schedule(days)
            self.push_class_schedule(class_id, new_class_schedule)

            # loop through all the subjects of class to add to schedule
            for subject_num, subject in enumerate(subject_per_class[class_id]):

                # set of days to remember for avoiding infinite loops in case of impossible situation
                days_with_teacher_conflict = set()

                # looping until subject is possible to add with met conditions:
                # - none of the teachers have two lessons at once (are_teachers_taken)
                # - checking if adding subject conflicts max possible length of day
                # - (return with error) if there is no available position to add new subject to

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

    def split_to_groups(self, days, conditions, log_file_name):
        """
        :param days: list of days used in schedule
        :param conditions: global conditions of schedule
        :param log_file_name: file name for run information
        :return: schedule with split subjects
        """

        # counting number of screenshots to avoid identical names of them
        tk_capture_count = 0

        # loop through all the classes to create separated schedules for them
        for class_id in self.school_schedule:
            class_schedule = self.school_schedule[class_id]
            for day in days:

                # loop trough subjects
                class_schedule_at_day = class_schedule[day]
                for subjects_list in class_schedule_at_day:
                    # we will reformat subjects from one class to list to be able to store multiple   once
                    subject = subjects_list[0]

                    # deciding on how (if needed) to split groups based on number of teachers
                    # if there is only one group we just need to write that information and reformat subject,
                    #   which is done with every case
                    # if there is 1 teacher we need to separate groups to avoid duplicate teacher conflict
                    # else we can store two groups at the same time

                    if subject.number_of_groups == 1 or subject.is_empty:
                        subject.teachers_id = [subject.teachers_id[0]]
                        subject.group = 0
                    elif len(subject.teachers_id) == 1:

                        # creating duplicates of subject, assigning to them different group ids and appending to list
                        for group in range(1, subject.number_of_groups):
                            new_subject = copy.deepcopy(subject)
                            new_subject.group = group + 1
                            subjects_list.append(new_subject)

                        # filling out the original subject with updated information
                        subject.teachers_id = [subject.teachers_id[0]]
                        subject.group = 1
                        subjects_list.insert(0, subject)

                        # based on subject position we can in some cases simplify for natural look of schedule
                        #   and avoiding logical issues as for e.g. one group having empty hour in between lessons
                        first_lesson_index = self.find_first_lesson_index(class_schedule_at_day, log_file_name)
                        if subject.lesson_hours_id == first_lesson_index:
                            for group in range(1, subject.number_of_groups):
                                for day_to in days:
                                    tk_capture_count += 1

                                    # checking if moving group creates conflict with conditions
                                    #   and if ok trying to move it
                                    if (self.get_num_of_lessons(self.school_schedule[class_id][day_to], log_file_name)
                                            >= conditions.general['max_lessons_per_day']):
                                        continue
                                    elif self.safe_move(
                                            teachers_id=subject.teachers_id,
                                            group=subject.group,
                                            day_from=day,
                                            day_to=day_to,
                                            subject_new_position=subject.lesson_hours_id,
                                            class_id=class_id,
                                            days=days,
                                            tk_capture_count=tk_capture_count,
                                            log_file_name=log_file_name
                                    ):
                                        pass
                                    else:
                                        continue
                                else:
                                    pass
                    else:
                        # TODO: this fragment is reapeting
                        # creating duplicates of subject, assigning to them different group ids and appending to list
                        for group in range(1, subject.number_of_groups):
                            new_subject = copy.deepcopy(subject)
                            new_subject.group = group + 1
                            new_subject.teachers_id = [subject.teachers_id[group]]
                            subjects_list.append(new_subject)

                        # filling out the original subject with updated information
                        subject.group = 1
                        subject.teachers_id = [subject.teachers_id[0]]
                        subjects_list.insert(0, subject)
