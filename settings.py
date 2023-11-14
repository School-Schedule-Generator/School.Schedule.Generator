class Settings:
    def __init__(self):
        self.DEBUG = True
        self.TKCAPTURE = True

        if self.DEBUG:
            self.TEST_DATA_PATH = './data/testData'
            self.DATABASE_PATH = './data'
            self.DF_NAMES = ['SSG_LESSON_HOURS', 'SSG_SUBJECT_NAMES', 'SSG_SUBJECTS', 'SSG_TEACHERS', 'SSG_CLASSES',
                             'SSG_CLASSROOMS']

            self.COLLUMN_NAMES = {
                'SSG_LESSON_HOURS': ['lesson_ID', 'start_hour', 'duration'],
                'SSG_SUBJECT_NAMES': ['subject_name_ID', 'name'],
                'SSG_SUBJECTS': ['subject_ID', 'subject_name_ID', 'class_ID', 'subject_count_in_week',
                                 'number_of_groups', 'subject_length', 'lesson_hours_ID', 'teachers_ID',
                                 'classroom_ID'],
                'SSG_TEACHERS': ['teacher_ID', 'name', 'surname', 'possible subjects'],
                'SSG_CLASSES': ['Class_ID', 'grade', 'class_sygnature', 'class_sygnature_number',
                                'supervising_teacher'],
                'SSG_CLASSROOMS': ['classroom_ID', 'classroom_name', 'possible_lessons']
            }


settings = Settings()
