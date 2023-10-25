def is_teacher_taken(self, teacher, day, lesson_index):
    same_time_subjects = self.get_same_time_subject(
        day=day,
        lesson_index=lesson_index
    )

    for same_time_subject in same_time_subjects:
        if same_time_subject.teacher_id == teacher:
            return True
    return False
