import pandas as pd

classes = pd.read_excel('./data/testData/SSG_CLASSES.xlsx')
classrooms = pd.read_excel('./data/testData/SSG_CLASSROOMS.xlsx')
lesson_hours = pd.read_excel('./data/testData/SSG_LESSON_HOURS.xlsx')
subject_names = pd.read_excel('./data/testData/SSG_SUBJECT_NAMES.xlsx')
subjects = pd.read_excel('./data/testData/SSG_SUBJECTS.xlsx')
teachers = pd.read_excel('./data/testData/SSG_TEACHERS.xlsx')

tables = [classes, classrooms, lesson_hours, subject_names, subjects, teachers]

for table in tables:
    print('\n\n', '-'*20)
    print(table.head(10))

#nauczyciel wybierany z inputa usera na podstawie listy z teachers_db