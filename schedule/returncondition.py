def are_teachers_taken(self, teachers, day, lesson_index, class_id):
    same_time_teachers = self.get_same_time_teacher(
        day=day,
        lesson_index=lesson_index,
        class_id=class_id
    )

    for teacher in teachers:
        for same_time_teacher in same_time_teachers:
            if same_time_teacher == teacher:
                return True
    return False
