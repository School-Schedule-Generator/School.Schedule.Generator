from subject import Subject
from debug_log import *
from tkinter_schedule_vis import tkinter_schedule_vis


def create_class_schedule(days):
    """
    :param days: list of days that the lessons can be in
    :return: empty schedule of passed in days
    """
    new_class_schedule = {}
    for day in days:
        new_class_schedule[day] = []
    return new_class_schedule


def move_subject_to_day(self, class_id, day_to, day_from, subject_position,
                        subject_to_position=-1, group=None, log_file_name=''):
    try:
        old = self.school_schedule[class_id][day_from][subject_position]
    except IndexError:
        debug_log(log_file_name, f'subject pos: {subject_position}, '
                                 f'len of day: {len(self.school_schedule[class_id][day_from])}')
        raise BaseException

    if old[0].is_empty:
        debug_log(log_file_name, "ERROR: can't move empty space")
        return False

    first_lesson = find_first_lesson_index(self.school_schedule[class_id][day_from], log_file_name=log_file_name)

    if subject_position == first_lesson:
        self.school_schedule[class_id][day_from][first_lesson] = [Subject(
            is_empty=True,
            lesson_hours_id=first_lesson,
            log_file_name=log_file_name
        )]
    elif subject_position == -1:
        self.school_schedule[class_id][day_from].pop()
    else:
        if group is None:
            debug_log(log_file_name,
                      "ERROR: if you want to move lesson in between other, "
                      "specify group so ther is no empty space in schedule")
            return False
        debug_log(log_file_name, "DEBUG: moved lesson at index diffrent than 0 or -1")

        old = self.school_schedule[class_id][day_from][subject_position][group - 1]
        try:
            self.school_schedule[class_id][day_from][subject_position][group - 1] = Subject(
                is_empty=True,
                lesson_hours_id=subject_position,
                log_file_name=log_file_name,
                group=group
            )
        except IndexError:
            debug_log(log_file_name, f'ERROR: index error '
                                     f'while trying to pop subject from subjects position at:{subject_position},'
                                     f'check if subject exists')
            return False

    if subject_to_position == -1:
        self.school_schedule[class_id][day_to].append(old)

        if len(self.school_schedule[class_id][day_to]) > 1:
            if subject_position == first_lesson:
                for subject in self.school_schedule[class_id][day_to][-1]:
                    subject.lesson_hours_id = (len(self.school_schedule[class_id][day_to]) - 1)

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
    else:
        if not len(self.school_schedule[class_id][day_to][subject_to_position]):
            debug_log(log_file_name, "DEBUG: moved 'old' to 0 len subject space")
            self.school_schedule[class_id][day_to][subject_to_position] = [old]
        elif self.school_schedule[class_id][day_to][subject_to_position][0].is_empty:
            debug_log(log_file_name, "DEBUG: moved 'old' to default empty space")
            self.school_schedule[class_id][day_to][subject_to_position] = [old]
        else:
            debug_log(log_file_name, "DEBUG: moved 'old' to occupied space")
            self.school_schedule[class_id][day_to][subject_to_position].append(old)

        try:
            self.school_schedule[class_id][day_to][subject_to_position][-1].lesson_hours_id = subject_to_position
        except AttributeError:
            debug_log(log_file_name,
                      self.school_schedule[class_id][day_to][subject_to_position], '\n',
                      self.school_schedule[class_id][day_to][subject_to_position][-1]
                      )

    return True


def swap_subject_in_groups(self, group, subjects_list_x, subjects_list_y):
    group -= 1
    (
        subjects_list_x[group].lesson_hours_id,
        subjects_list_y[group].lesson_hours_id
    ) = (
        subjects_list_y[group].lesson_hours_id,
        subjects_list_x[group].lesson_hours_id
    )

    (
        subjects_list_x[group],
        subjects_list_y[group]
    ) = (
        subjects_list_y[group],
        subjects_list_x[group]
    )


def safe_move(self, teachers_id, day_from, day_to, subject_position, subject_new_position, class_id,
              group=None, log_file_name=''):
    """
    :param self: class schedule
    :param teachers_id: ids of teachers to check
    :param day_from: day which we take subject from
    :param day_to: day which we add subject to
    :param subject_position: old position of subject
    :param subject_new_position: new position to add subject to
    :param class_id:
    :param group: class group to move
    :param log_file_name: file name for run information
    :description: before trying to move using move_subject_to_day(), function checks if action is possible
    and notifies program
    :return: was operation successful
    """

    subject_to_position = lesson_index = None
    if subject_new_position == 0:
        first_lesson_index = find_first_lesson_index(self.school_schedule[class_id][day_to], log_file_name=log_file_name)

        if first_lesson_index is None:
            subject_to_position = -1
            lesson_index = 0
        elif first_lesson_index != 0:
            subject_to_position = lesson_index = first_lesson_index - 1
        else:
            return False

    elif subject_new_position == -1:
        subject_to_position = -1
        lesson_index = len(self.school_schedule[class_id][day_to])

    elif subject_new_position < find_first_lesson_index(
            self.school_schedule[class_id][day_from],
            log_file_name=log_file_name
    ):
        debug_log(log_file_name, f"ERROR: can't move subject before first lesson\n")
        raise BaseException

    if not self.are_teachers_taken(
        teachers=teachers_id,
        day_to=day_to,
        lesson_index=lesson_index,
    ):
        if not self.move_subject_to_day(
                class_id=class_id,
                day_to=day_to,
                day_from=day_from,
                subject_position=subject_position,
                subject_to_position=subject_to_position,
                group=group,
                log_file_name=log_file_name
        ):
            debug_log(
                log_file_name,
                f'While 1: class_schedule_id: '
                f'{class_id} '
                f'lesson_index={-1} '
                f'day_to: {day_to} day_from: '
                f'{day_from}'
            )
            raise BaseException
        return True
    return False


def get_same_time_teacher(self, day_to, lesson_index):
    same_time_teachers = []
    for class_schedule_id in self.school_schedule:
        try:
            subjects_list = self.school_schedule[class_schedule_id][day_to][lesson_index]
            for subject in subjects_list:
                for teacher_id in subject.teachers_id:
                    same_time_teachers.append(teacher_id)
        except IndexError:
            pass
    return same_time_teachers


def find_another_grouped_lessons(self, class_id, lesson_day, lesson_index, number_of_groups, days):
    class_schedule = self.school_schedule[class_id]
    possibilities = []
    for day in days:
        class_schedule_at_day = class_schedule[day]
        for subjects_list in class_schedule_at_day:
            if (
                    (
                            lesson_day == day
                            and lesson_index == subjects_list[0].lesson_hours_id
                            and subjects_list[0].number_of_groups != number_of_groups
                    )
                    or len(subjects_list) <= 1
            ):
                continue
            else:
                possibilities.append([day, subjects_list[0].lesson_hours_id, subjects_list])

    return possibilities


def find_first_lesson_index(schedule_at_day, log_file_name):
    for i, subjects in enumerate(schedule_at_day):
        for subject in subjects:
            if subject.is_empty:
                debug_log(log_file_name, 'DEBUG: empty cell')
            else:
                return i
    return None


def get_num_of_lessons(schedule_at_day, log_file_name):
    first_lesson_index = find_first_lesson_index(schedule_at_day, log_file_name)
    return len(schedule_at_day[first_lesson_index:])
