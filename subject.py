class Subject:
    """
    subject from subjects dataframe turned into an object
    """
    def __init__(self, subject_id, subject_name_id, class_id, subject_count_in_week, number_of_groups, subject_length,
                 lesson_hours_id, teacher_id, classroom_id):
        self.subject_id = subject_id
        self.subject_name_id = subject_name_id
        self.class_id = class_id
        self.subject_count_in_week = subject_count_in_week
        self.number_of_groups = number_of_groups
        self.subject_length = subject_length
        self.lesson_hours_id = lesson_hours_id
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id