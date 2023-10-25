def create_class_schedule(days):
    """
    :param days: list of days that the lessons can be in
    :return: empty schedule of passed in days
    """
    new_class_schedule = {}
    for day in days:
        new_class_schedule[day] = []
    return new_class_schedule


def print_debug(self, classes_id, days, print_subjects=False):
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


def get_same_time_subject(self, day, lesson_index):
    temp = []
    for other_class_schedule_id in self.school_schedule:
        other_class_schedule_day = self.school_schedule[other_class_schedule_id][day]
        try:
            other_class_subject = other_class_schedule_day[lesson_index]
            temp.append(other_class_subject)
        except IndexError:
            pass
    return temp


def swap(self, class_id, day_x, subject_x_position, day_y, subject_y_position):
    (
        self.school_schedule[class_id][day_x][subject_x_position],
        self.school_schedule[class_id][day_y][subject_y_position]
    ) = (
        self.school_schedule[class_id][day_y][subject_y_position],
        self.school_schedule[class_id][day_x][subject_x_position]
    )
