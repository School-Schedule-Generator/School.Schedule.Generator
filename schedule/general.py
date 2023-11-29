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


def move_subject_to_day(self, class_id, day_to, day_from, subject_position,
                        subject_to_position=-1, group=None, log_file_name=''):

    try:
        old = self.school_schedule[class_id][day_from][subject_position]
    except IndexError:
        # TODO: For some reason subject position is compleatly wrong - day is smaller than index we want to enter
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

        old = self.school_schedule[class_id][day_from][subject_position][group-1]
        try:
            self.school_schedule[class_id][day_from][subject_position][group-1] = Subject(
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
            print(
                self.school_schedule[class_id][day_to][subject_to_position], '\n',
                self.school_schedule[class_id][day_to][subject_to_position][-1]
            )

    return True


def swap_subject_in_place(self, class_id, day_x, subject_x_position, day_y, subject_y_position):
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


def safe_move(self, teachers_id, day_from, day_to, subject_new_position, class_id, days, tk_capture_count,
              group=None, log_file_name=''):
    """
    :param self: class schedule
    :param teachers_id: ids of teachers to check
    :param day_from: day which we take subject from
    :param day_to: day which we add subject to
    :param subject_new_position: new position to add subject to
    :param class_id:
    :param days: list of days with lessons in
    :param tk_capture_count:
    :param group: class group to move
    :param log_file_name: file name for run information
    :description: before trying to move using move_subject_to_day(), function checks if action is possible
    and notifies program
    :return: was operation successful
    """

    if subject_new_position == 0:
        subject_new_position = find_first_lesson_index(
            self.school_schedule[class_id][day_from],
            log_file_name=log_file_name
        )
    elif subject_new_position < find_first_lesson_index(
            self.school_schedule[class_id][day_from],
            log_file_name=log_file_name
    ):
        debug_log(log_file_name, "ERROR: can't move subject before first lesson")
        raise BaseException

    first_lesson_index = find_first_lesson_index(self.school_schedule[class_id][day_from], log_file_name=log_file_name)

    subject_to_position = -1
    lesson_index = len(self.school_schedule[class_id][day_to])
    if first_lesson_index != 0:
        first_empty_space = first_lesson_index - 1
        lesson_index = first_empty_space
        subject_to_position = first_empty_space

    if not self.are_teachers_taken(
            teachers=teachers_id,
            day=day_to,
            lesson_index=lesson_index,
            class_id=class_id
    ):
        if not self.move_subject_to_day(
                class_id=class_id,
                day_to=day_to,
                day_from=day_from,
                subject_position=subject_new_position,
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
        tkinter_schedule_vis(
            self,
            days,
            capture_name=f'update_min_day_len_{class_id}_{tk_capture_count}_post_change',
            dir_name=log_file_name
        )
        return True
    return False


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
