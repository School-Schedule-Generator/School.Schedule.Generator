from debug_log import *
from tkinter_schedule_vis import tkinter_schedule_vis


def update_min_day_len(self, conditions, days, teachers, log_file_name):
    """
        :param self:
        :param conditions: global conditions of schedule
        :param days: list of days with lessons in
        :param teachers: list of all teachers
        :param log_file_name: file name for run information
        :return: schedule with min 5 lessons at day
    """

    if self.valid is False:
        return self

    # loop through all classes
    for class_id in self.data:
        class_schedule = self.data[class_id]
        tk_capture_count = 0
        for current_day in days:
            schedule_at_day = class_schedule[current_day]

            days_with_conflict = set()
            set_days = set(days)

            # looping until num of lessons is lower than minimum and subject is possible to add with met conditions:
            # - none of the teachers have two lessons at once
            # (return with ERROR) if there is no available position to add new subject to
            while self.get_num_of_lessons(schedule_at_day, log_file_name) < \
                    conditions.data['min_lessons_per_day']:
                class_schedule_list = list(class_schedule.values())
                max_len_day_i = class_schedule_list.index(max(class_schedule.values(), key=len))

                schedule_at_day = class_schedule[current_day]

                tk_capture_count += 1
                tkinter_schedule_vis(
                    self,
                    days,
                    capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_a_pre_change',
                    dir_name=log_file_name
                )

                if days_with_conflict == set_days:
                    debug_log(log_file_name, 'ERROR: days_with_conflict == set_days')
                    return

                first_lesson_index = self.find_first_lesson_index(schedule_at_day, log_file_name)
                if first_lesson_index is None:
                    debug_log(log_file_name, 'DEBUG: lesson from longest day moved to first_lesson_index')
                    first_lesson_index = -1

                max_day_schedule = self.data[class_id][days[max_len_day_i]]

                # common pattern to check if we can first add lesson before others and then if we can add it after other
                #   this is to ensure that schedule stays wich logic of user intentions

                # first (if and elif) check ideal case where program subract from the longest day
                #   to balance length of days
                # if not possible program loops trough every other day to find any spot to place the subject
                #   (if not possible return with ERROR)

                # Positions we check
                # subject current position | subject new position
                #           -1             |            0
                #            0             |            0
                #           -1             |           -1
                #            0             |           -1

                if self.safe_move(
                    teachers_id=max_day_schedule[-1][0].teachers_id,
                    day_from=days[max_len_day_i],
                    day_to=current_day,
                    subject_position=-1,
                    subject_new_position=0,
                    class_id=class_id,
                    days=days,
                    teachers=teachers,
                    log_file_name=log_file_name
                ):
                    tkinter_schedule_vis(
                        self,
                        days,
                        capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_{-1}_{0}_b_post_change',
                        dir_name=log_file_name
                    )
                elif self.safe_move(
                    teachers_id=max_day_schedule[first_lesson_index][0].teachers_id,
                    day_from=days[max_len_day_i],
                    day_to=current_day,
                    subject_position=first_lesson_index,
                    subject_new_position=0,
                    class_id=class_id,
                    days=days,
                    teachers=teachers,
                    log_file_name=log_file_name
                ):
                    tkinter_schedule_vis(
                        self,
                        days,
                        capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_{first_lesson_index}_{0}_b_post_change',
                        dir_name=log_file_name
                    )
                elif self.safe_move(
                    teachers_id=max_day_schedule[-1][0].teachers_id,
                    day_from=days[max_len_day_i],
                    day_to=current_day,
                    subject_position=-1,
                    subject_new_position=-1,
                    class_id=class_id,
                    days=days,
                    teachers=teachers,
                    log_file_name=log_file_name
                ):
                    tkinter_schedule_vis(
                        self,
                        days,
                        capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_{-1}_{-1}_b_post_change',
                        dir_name=log_file_name
                    )
                elif self.safe_move(
                    teachers_id=max_day_schedule[first_lesson_index][0].teachers_id,
                    day_from=days[max_len_day_i],
                    day_to=current_day,
                    subject_position=first_lesson_index,
                    subject_new_position=-1,
                    class_id=class_id,
                    days=days,
                    teachers=teachers,
                    log_file_name=log_file_name
                ):
                    tkinter_schedule_vis(
                        self,
                        days,
                        capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_{first_lesson_index}_{-1}_b_post_change',
                        dir_name=log_file_name
                    )
                else:
                    days_with_conflict.add(days[max_len_day_i])

                    for day in set_days.difference(days_with_conflict):

                        schedule_at_other_day = self.data[class_id][day]
                        first_lesson_index = self.find_first_lesson_index(schedule_at_other_day, log_file_name)

                        if first_lesson_index is None:
                            debug_log(log_file_name, 'not max move to first_lesson_index')
                            continue

                        if self.get_num_of_lessons(schedule_at_other_day, log_file_name) <= \
                                conditions.data['min_lessons_per_day']:
                            continue

                        if self.safe_move(
                            teachers_id=schedule_at_other_day[-1][0].teachers_id,
                            day_from=day,
                            day_to=current_day,
                            subject_position=-1,
                            subject_new_position=0,
                            class_id=class_id,
                            days=days,
                            teachers=teachers,
                            log_file_name=log_file_name
                        ):
                            tkinter_schedule_vis(
                                self,
                                days,
                                capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_inElse_{-1}_{0}_b_post_change',
                                dir_name=log_file_name
                            )
                        elif self.safe_move(
                            teachers_id=schedule_at_other_day[first_lesson_index][0].teachers_id,
                            day_from=day,
                            day_to=current_day,
                            subject_position=first_lesson_index,
                            subject_new_position=0,
                            class_id=class_id,
                            days=days,
                            teachers=teachers,
                            log_file_name=log_file_name
                        ):
                            tkinter_schedule_vis(
                                self,
                                days,
                                capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_inElse_{first_lesson_index}_{0}_b_post_change',
                                dir_name=log_file_name
                            )
                        elif self.safe_move(
                            teachers_id=schedule_at_other_day[-1][0].teachers_id,
                            day_from=day,
                            day_to=current_day,
                            subject_position=-1,
                            subject_new_position=-1,
                            class_id=class_id,
                            days=days,
                            teachers=teachers,
                            log_file_name=log_file_name
                        ):
                            tkinter_schedule_vis(
                                self,
                                days,
                                capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_inElse_{-1}_{-1}_b_post_change',
                                dir_name=log_file_name
                            )
                        elif self.safe_move(
                            teachers_id=schedule_at_other_day[first_lesson_index][0].teachers_id,
                            day_from=day,
                            day_to=current_day,
                            subject_position=first_lesson_index,
                            subject_new_position=-1,
                            class_id=class_id,
                            days=days,
                            teachers=teachers,
                            log_file_name=log_file_name
                        ):
                            tkinter_schedule_vis(
                                self,
                                days,
                                capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_{first_lesson_index}_{-1}_b_post_change',
                                dir_name=log_file_name
                            )
                        else:
                            days_with_conflict.add(day)
                            continue

                        tk_capture_count += 1

                    break

            if self.get_num_of_lessons(schedule_at_day, log_file_name) < conditions.data['min_lessons_per_day']:
                print('*' * 10, '\n', self.valid, '*' * 10, '\n', )
                self.valid = False
                return self

    return self
