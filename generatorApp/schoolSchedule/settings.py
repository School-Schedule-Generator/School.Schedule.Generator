class Settings:
    def __init__(self):
        # Describe mode to run the program on
        self.DEBUG = False

        # Take screenshots - True
        self.TKCAPTURE = False
        self.SAVELOG = False

        # if debug create default names
        self.TEST_DATA_PATH = '../../testdata'
        self.BASE_DATA_PATH = '../static/data'
        self.DATABASE_NAME = 'db.sqlite3'
        self.DF_NAMES = ['SSG_LESSON_HOURS', 'SSG_SUBJECT_NAMES', 'SSG_SUBJECTS', 'SSG_TEACHERS', 'SSG_CLASSES',
                         'SSG_CLASSROOMS', 'SSG_CLASSROOM_TYPES']

        self.COLUMN_NAMES = {
            'SSG_LESSON_HOURS': ['lesson_id', 'start_hour', 'duration'],
            'SSG_SUBJECT_NAMES': ['subject_name_id', 'name'],
            'SSG_SUBJECTS': ['subject_id', 'subject_name_id', 'class_id', 'subject_count_in_week',
                             'number_of_groups', 'lesson_hour_id', 'teachers_id',
                             'classroom_id', 'max_stack', 'classroom_types'],
            'SSG_TEACHERS': ['teacher_id', 'name', 'surname', 'possible_subjects', 'start_hour_index',
                             'end_hour_index', 'days', 'main_classroom'],
            'SSG_CLASSES': ['class_id', 'grade', 'class_signature',
                            'supervising_teacher', 'starting_lesson_hour_id'],
            'SSG_CLASSROOMS': ['classroom_id', 'classroom_name', 'type_id'],
            'SSG_CLASSROOM_TYPES': ['type_id', 'description']
        }

        self.SQL_COLUMN_NAMES = {
            'SSG_LESSON_HOURS': ['_id', 'start_hour', 'duration'],
            'SSG_SUBJECT_NAMES': ['_id', 'name'],
            'SSG_SUBJECTS': ['_id', 'subject_name_id_id', 'classes_id_id', 'subject_count_in_week',
                             'number_of_groups', 'lesson_hour_id_id', 'teachers_id',
                             'classroom_id_id', 'max_stack', 'classroom_types'],
            'SSG_TEACHERS': ['_id', 'name', 'surname', 'possible_subjects', 'start_hour_index',
                             'end_hour_index', 'days', 'main_classroom_id_id'],
            'SSG_CLASSES': ['_id', 'grade', 'class_signature',
                            'supervising_teacher_id_id', 'starting_lesson_hour_id_id'],
            'SSG_CLASSROOMS': ['_id', 'name', 'type_id_id'],
            'SSG_CLASSROOM_TYPES': ['_id', 'description']
        }

        self.SQLTABLES = {
            'SSG_LESSON_HOURS': {
                'Name': 'generatorApp_lessonhours',
                'Columns': self.SQL_COLUMN_NAMES['SSG_LESSON_HOURS']
            },
            'SSG_SUBJECT_NAMES': {
                'Name': 'generatorApp_subjectnames',
                'Columns': self.SQL_COLUMN_NAMES['SSG_SUBJECT_NAMES']
            },
            'SSG_SUBJECTS': {
                'Name': 'generatorApp_subject',
                'Columns': self.SQL_COLUMN_NAMES['SSG_SUBJECTS']
            },
            'SSG_TEACHERS': {
                'Name': 'generatorApp_teachers',
                'Columns': self.SQL_COLUMN_NAMES['SSG_TEACHERS']
            },
            'SSG_CLASSES': {
                'Name': 'generatorApp_classes',
                'Columns': self.SQL_COLUMN_NAMES['SSG_CLASSES']
            },
            'SSG_CLASSROOMS': {
                'Name': 'generatorApp_classrooms',
                'Columns': self.SQL_COLUMN_NAMES['SSG_CLASSROOMS']
            },
            'SSG_CLASSROOM_TYPES': {
                'Name': 'generatorApp_classroomtypes',
                'Columns': self.SQL_COLUMN_NAMES['SSG_CLASSROOM_TYPES']
            }
        }


settings = Settings()
