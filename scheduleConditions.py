from distutils.util import strtobool

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
        elif len(self.conditions_list) > 0:
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
                conditions_list.append({
                    'arg': condition[0],
                    'value': condition[1],
                    'line_number': i,
                    'line': raw_line
                })
            except IndexError:
                print(f"Error at line {i}: {raw_line}")
                print("Passed in argument is not fully defined")
                return False
        condition_raw.close()
        return conditions_list

    def load_conditions_list(self):
        for condition in self.conditions_list:
            if condition['arg'][0] == '.':
                condition['arg'] = condition['arg'][1:]
                if not self.update_general_condition(condition):
                    return False

        return True

    def update_general_condition(self, condition):
        if condition['arg'] in self.general.keys():
            if condition['value'].isdigit():
                self.general[condition['arg']] = int(condition['value'])
            elif condition['value'] in ['True', 'False']:
                self.general[condition['arg']] = strtobool(condition['value'])
            else:
                print(f"Error at line {condition['arg']}: {condition['value']}")
                print("Cannot convert general conditon into type string")
                return False
        else:
            print(f"Error at line {condition['arg']}: {condition['value']}")
            print("Passed in argument doesn't exist")
            return False
        return True

    def format_schedule(self, schedule):
        """
        :param schedule: schedule for all school classes
        :return: returns conditionalized schedule
        """
        pass