import random

class Schedule:
    def __init__(self):
        self.school_schedule = []

    def add_class_schedule(self, class_schedule):
        self.school_schedule.append(class_schedule)

    def create(self, classes_id, conditions, days, subject_per_class):
        for class_id in classes_id:
            new_class_schedule = self.create_class_schedule(days)
            for subject in subject_per_class[class_id]:
                for i in range(subject.subject_count_in_week):
                    day = random.choice(days)

                    for class_schedule in self.school_schedule:
                        other_class_day = class_schedule[days[days.index(day)]]
                        if not len(other_class_day) == len(new_class_schedule[day]):
                            continue

                        while (subject.teacher_id
                               == other_class_day[
                                   len(new_class_schedule[day])-1
                               ]) or \
                                len(new_class_schedule[day]) >= conditions.general['max_lessons_per_day']:
                            day = random.choice(days)

                    subject.lesson_hours_id = len(new_class_schedule[day])
                    new_class_schedule[day].append(subject)
            self.add_class_schedule(new_class_schedule)

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
