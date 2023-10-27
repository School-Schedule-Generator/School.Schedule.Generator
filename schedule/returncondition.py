def is_teacher_taken(self, teacher, day, lesson_index):
    same_time_subjects = self.get_same_time_teacher(
        day=day,
        lesson_index=lesson_index
    )

    for same_time_teacher in same_time_subjects:
        if same_time_teacher == teacher:
            return True
    return False
