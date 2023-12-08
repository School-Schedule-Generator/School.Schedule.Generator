from schedule.update_min_day_len import *


def format_schedule(self, conditions, days, teachers, log_file_name):
    if self.valid is False:
        return self
    return update_min_day_len(self, conditions, days, teachers, log_file_name)
