from specificConditions import *


def format_schedule(conditions, schedule, days, log_file_name):
    condition_func = {
        'min_lessons_per_day': update_min_day_len(conditions, schedule, days, log_file_name),
    }

    for condition in conditions.general:
        try:
            condition_func[condition]
        except KeyError:
            continue