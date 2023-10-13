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
        self.Types = Enum('Types', ['string', 'int', 'bool', 'strict', 'loose', 'none'])
        self.speciffic = {
            'stack': {
                'desc': 'for stacking the same type of subject in a row',
                'types': [self.Types['strict'], self.Types['loose'], self.Types['none']]
            },
            'max_stack': {
                'desc': 'decides how long can a stack be (if not defined stack will be as long as it can)',
                'types': [self.Types['int']]
            }
        }
        self.specific_in_use = {
            'max-stack': {
                'range': 'all' # range defines the reach of condition (on what collumns has it effect)
            }
        }
        self.valid = True

        self.conditions_list = self.get_condition_list(file_path)
        if self.conditions_list:
            valid_conditions = self.load_conditions_list()
            self.valid = valid_conditions
        elif type(self.conditions_list) is bool: # if there is an unusual occurrence
            self.valid = self.conditions_list
        elif type(self.conditions_list) is dict and len(self.conditions_list) > 0: #if file is empty
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

    def add_speciffic_condition(self, condition):
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

    # May not be in use!
    def update_max_day_len(self, schedule, days):
        for i, class_schedule in enumerate(schedule.school_schedule):
            for j in range(len(class_schedule)):
                class_schedule_list = list(class_schedule.values())
                min_len_day_i = class_schedule_list.index(min(class_schedule.values(), key=len))
                day = class_schedule[days[j]]
                while len(day) > self.general['max_lessons_per_day']:
                    schedule.move_subject_to_day(
                        class_id=i,
                        day_to=days[j],
                        day_from=days[min_len_day_i],
                        subject_position=-1
                    )

    def update_min_day_len(self, schedule, days):
        for i, class_schedule in enumerate(schedule.school_schedule):
            for j in range(len(class_schedule)):
                class_schedule_list = list(class_schedule.values())
                max_len_day_i = class_schedule_list.index(max(class_schedule.values(), key=len))

                day = class_schedule[days[j]]
                while len(day) < self.general['min_lessons_per_day']:
                    schedule.move_subject_to_day(
                        class_id=i,
                        day_to=days[j],
                        day_from=days[max_len_day_i],
                        subject_position=-1
                    )

    def format_schedule(self, schedule, days):
        for condition in self.general:
            pass

        for condition in self.specific_in_use:
            pass
