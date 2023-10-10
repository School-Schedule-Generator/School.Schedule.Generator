class Schedule:
    def __init__(self):
        self.school_schedule = []

    def add_class_schedule(self, class_schedule):
        self.school_schedule.append(class_schedule)

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
                        print(f'\t\t{subject.subject_name_id}')
                print('\n')
            print('-' * 10)
