class Teacher:
    def __init__(self, name, surname, possible_subjects, start_hour_index, end_hour_index, days):
        self.name = name
        self.surname = surname
        self.possible_subjects = possible_subjects
        self.start_hour_index = start_hour_index
        self.end_hour_index = end_hour_index
        self.days = days


def create_teachers(teachers_df):
    teachers = {}
    for _, row in teachers_df.iterrows():
        teachers[row['teacher_ID']] = Teacher(
            name=row['name'],
            surname=row['surname'],
            possible_subjects=row['possible_subjects'],
            start_hour_index=row['start_hour_index'],
            end_hour_index=row['end_hour_index'],
            days=row['days']
        )

    return teachers
