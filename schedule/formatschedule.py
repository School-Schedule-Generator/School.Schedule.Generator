from schedule.update_min_day_len import *
from schedule.add_classrooms import *


def format_schedule(self, conditions, days, teachers, classrooms, log_file_name):
    if self.valid is False:
        return self

    update_min_day_len(self, conditions, days, teachers, log_file_name)
    add_classrooms(self, classrooms, days, log_file_name)
    return self
