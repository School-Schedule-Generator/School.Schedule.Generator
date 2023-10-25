from distutils.util import strtobool
from enum import Enum


class ScheduleConditions:
    """
    class for conditionalising a schedule
    """
    def __init__(self, file_path, min_lessons_per_day=5, max_lessons_per_day=9):
        self.general = {
            'min_lessons_per_day': min_lessons_per_day,
            'max_lessons_per_day': max_lessons_per_day,
        }

        self.valid = True
        self.conditions_list = self.get_condition_list(file_path)
        if self.conditions_list:
            valid_conditions = self.load_conditions_list()
            self.valid = valid_conditions
        elif type(self.conditions_list) is bool:  # if there is an unusual occurrence
            self.valid = self.conditions_list
        elif type(self.conditions_list) is dict and len(self.conditions_list) > 0:  # if file is empty
            self.valid = False

    @staticmethod
    def get_condition_list(file_path):
        """
        :param file_path: path
        :return: list of conditions written in a file
        """
        condition_raw = open(file_path, 'r')
        lines = condition_raw.readlines()
        conditions_list = []
        for i, raw_line in enumerate(lines):
            line = raw_line.strip().replace(' ', '').lower()
            condition = line.split(':')
            try:
                if condition[1] == '':
                    raise IndexError

                if raw_line in ['\n', '']:
                    continue

                conditions_list.append({
                    'arg': condition[0],
                    'value': condition[1],
                    'line_num': i,
                    'line': repr(raw_line)
                })
            except IndexError:
                print(f"""Error at line {i}:\n\t{repr(raw_line)}\n""")
                print(f"""Passed in condition: {repr(raw_line)} is not fully defined""")
                return False
        condition_raw.close()
        return conditions_list

    def load_conditions_list(self):
        for condition in self.conditions_list:
            if condition['arg'][0] == '.':
                condition['arg'] = condition['arg'][1:]
                if not self.update_general_condition(condition):
                    return False
            elif not self.add_specific_condition(condition):
                return False
        return True

    def add_specific_condition(self, condition):
        # TODO
        #  split up condition to actual condition and specified range and type
        #  check if condition is in specific.keys() if not return False and show error
        pass

    def update_general_condition(self, condition):
        if condition['arg'] in self.general.keys():
            if condition['value'].isdigit():
                self.general[condition['arg']] = int(condition['value'])
            elif condition['value'] in ['True', 'False']:
                self.general[condition['arg']] = strtobool(condition['value'])
            else:
                print(f"""Error at line {condition['line_num']}:\n\t"{condition['arg']}: {condition['value']}"\n""")
                print(f"""Cannot convert general condition argument into type string""")
                return False
        else:
            print(f"""Error at line {condition['line_num']}:\n\t"{condition['arg']}: {condition['value']}"\n""")
            print(f"""Passed in argument: "{condition['arg']}" doesn't exist""")
            return False
        return True

    def update_min_day_len(self, schedule, days):

        for class_schedule_id in schedule.school_schedule:
            class_schedule = schedule.school_schedule[class_schedule_id]
            for i in range(len(class_schedule)):
                class_schedule_list = list(class_schedule.values())
                max_len_day_i = class_schedule_list.index(max(class_schedule.values(), key=len))

                day = class_schedule[days[i]]
                while len(day) < self.general['min_lessons_per_day']:
                    while True:
                        if not schedule.is_teacher_taken():

                            schedule.move_subject_to_day(
                                class_id=class_schedule_id,
                                day_to=days[i],
                                day_from=days[max_len_day_i],
                                subject_position=-1
                            )
                            break
                        else:
                            # TODO
                            # find new max len day
                            # znaleść inną lekcje ktorą można przenieść do tego dnia
                            # jeśli żaden dzień na 1 lub -1 lekcji nie
                            # jest w stanie dodać do tego dnia też na 1 lub -1
                            # lekcji to staramy się wsadzić tą lekcje w środek dnia,
                            # jeśli i to nie zadziała to musimy wygenerować plan na nowo lub wyrzucić error
                            pass

    def format_schedule(self, schedule, days):
        condition_func = {
            'min_lessons_per_day': self.update_min_day_len(schedule, days),
        }
        for condition in self.general:
            try:
                condition_func[condition]
            except KeyError:
                continue
