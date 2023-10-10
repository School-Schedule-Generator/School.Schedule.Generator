from settings import *
import pandas as pd
import os
import sqlite3
from subject import *


def loadData(
        path='.',
        tables=settings.DF_NAMES,
        file_type='xlsx',
        sql_tables={}
):
    """
    :param path: path to either SQL database or folder with tables of type CSV or Excel
    :param tables: list of files/tables
    :param file_type: type of file to read, can be mdl (SQL database), xlsx (Excel file), CSV (comma-separated values), defaults to xlsx
    :param sql_tables: list of table names and their columns formatted like:
        {
            'table_1': ['column_1', 'column_2'],
            'table_2': ['column_1', 'column_2']
        }
    :return: list of pandas dataframes
    """
    dataframes = []
    if settings.DEBUG:
        for file in tables:
            if file_type=='xlsx':
                dataframes.append(pd.read_excel(os.path.join(settings.TEST_DATA_PATH, file+'.'+file_type)))
            if file_type=='csv':
                dataframes.append(pd.read_csv(os.path.join(settings.TEST_DATA_PATH, file + '.' + file_type)))
            elif file_type=='mdf':
                table_name=file
                con = sqlite3.connect(settings.DATABASE_PATH)
                sql_query = pd.read_sql(f'SELECT * FROM {table_name}', con)
                dataframes.append(pd.DataFrame(sql_query, columns=settings.COLLUMN_NAMES[table_name]))
    else:
        for file in tables:
            if file_type=='xlsx':
                dataframes.append(pd.read_excel(os.path.join(path, file+'.'+file_type)))
            if file_type=='csv':
                dataframes.append(pd.read_csv(os.path.join(path, file + '.' + file_type)))
            elif file_type=='mdf':
                table_name=file
                con = sqlite3.connect(path)
                sql_query = pd.read_sql(f'SELECT * FROM {table_name}', con)
                dataframes.append(pd.DataFrame(sql_query, columns=sql_tables[table_name]))

    return dataframes


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
