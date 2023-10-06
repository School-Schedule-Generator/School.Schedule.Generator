import pandas as pd

classes = pd.read_excel('./data/testData/SSG_CLASSES.xlsx')
classrooms = pd.read_excel('./data/testData/SSG_CLASSROOMS.xlsx')
lesson_hours = pd.read_excel('./data/testData/SSG_LESSON_HOURS.xlsx')
subject_names = pd.read_excel('./data/testData/SSG_SUBJECT_NAMES.xlsx')
subjects = pd.read_excel('./data/testData/SSG_SUBJECTS.xlsx')
teachers = pd.read_excel('./data/testData/SSG_TEACHERS.xlsx')

subjects['teacher_ID']

print(subjects.head(10))
