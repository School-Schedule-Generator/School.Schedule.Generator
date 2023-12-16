class Teacher:
    def __init__(self, name, surname, possible_subjects, start_hour_index, end_hour_index, days, main_classroom):
        self.name = name
        self.surname = surname
        self.possible_subjects = possible_subjects
        self.start_hour_index = start_hour_index
        self.end_hour_index = end_hour_index
        self.days = days
        self.main_classroom = main_classroom


def create_teachers(teachers_df):
    teachers_df['main_classroom'] = teachers_df['main_classroom'].replace('Null', None)
    teachers = {}
    for _, row in teachers_df.iterrows():
        teachers[row['teacher_ID']] = Teacher(
            name=row['name'],
            surname=row['surname'],
            possible_subjects=row['possible_subjects'],
            start_hour_index=row['start_hour_index'],
            end_hour_index=row['end_hour_index'],
            days=row['days'],
            main_classroom=row['main_classroom']
        )

    return teachers
