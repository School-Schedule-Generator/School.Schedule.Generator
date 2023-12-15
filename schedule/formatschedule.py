from schedule.update_min_day_len import *


def format_schedule(self, conditions, days, teachers, classes_id,
                    classes_start_hour_index, days_ordered, log_file_name):
    if self.valid is False:
        return self
    return update_min_day_len(
        self,
        conditions,
        days,
        teachers,
        log_file_name
    )
