from subject import *

def print_school_schedule(school_schedule, classes_id, days, print_subjects=False):
    for i, class_schedule in enumerate(school_schedule):
        print(f'class {classes_id[i]}')
        for j in range(len(class_schedule)):
            print(f'\t{days[j]}\n\t\tlen={len(class_schedule[days[j]])}')
            if print_subjects:
                for subject in class_schedule[days[j]]:
                    print(f'\t\t{subject.subject_name_id}')
            print('\n')
        print('-' * 10)

def get_classes_id(df):
    """
    :param df: dataframe of classes
    :return: list of classes ids
    """
    return df['Class_ID'].to_numpy()


def create_schedule(days):
    """
    :param days: list of days that the lessons can be in
    :return: empty schedule of passed in days
    """
    new_schedule = {}
    for day in days:
        new_schedule[day] = []
    return new_schedule


def split_subject_per_class(subjects_df, subject_per_class_df):
    """
    :param subjects_df: dataframe of all subjects
    :param subject_per_class_df: list of dataframes of subjects per class
    :return: returns splitet into classes lists of subjects
    """
    subject_per_class = {}
    for class_df_id in subject_per_class_df:
        class_df = subject_per_class_df[class_df_id]
        subject_per_class[class_df_id] = [Subject(
            subject_id=subjects_df.loc[i, 'subject_ID'],
            subject_name_id=subjects_df.loc[i, 'subject_name_ID'],
            class_id=subjects_df.loc[i, 'class_ID'],
            subject_count_in_week=subjects_df.loc[i, 'subject_count_in_week'],
            number_of_groups=subjects_df.loc[i, 'number_of_groups'],
            teacher_id=subjects_df.loc[i, 'teacher_ID'],
            classroom_id=subjects_df.loc[i, 'classroom_ID'],
            subject_length=subjects_df.loc[i, 'subject_length'],
            lesson_hours_id=subjects_df.loc[i, 'lesson_hours_ID']
        ) for i in range(len(class_df))]
    return subject_per_class