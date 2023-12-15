class ScheduleConditions:
    def __init__(self, min_lessons_per_day=5, max_lessons_per_day=9):
        self.data = {
            'min_lessons_per_day': min_lessons_per_day,
            'max_lessons_per_day': max_lessons_per_day,
        }
