from settings import *
import pandas as pd
import os
import sqlite3
from subject import *
import ast


def load_data(
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
    dataframes = {}
    if settings.DEBUG:
        for file in tables:
            if file_type == 'xlsx':
                dataframes[file] = pd.read_excel(os.path.join(settings.TEST_DATA_PATH, file + '.' + file_type))
            if file_type == 'csv':
                dataframes[file] = pd.read_csv(os.path.join(settings.TEST_DATA_PATH, file + '.' + file_type))
            elif file_type == 'mdf':
                table_name = file
                con = sqlite3.connect(settings.DATABASE_PATH)
                sql_query = pd.read_sql(f'SELECT * FROM {table_name}', con)
                dataframes[file] = pd.DataFrame(sql_query, columns=settings.COLLUMN_NAMES[table_name])

        dataframes['SSG_SUBJECTS']['teachers_ID'] = dataframes['SSG_SUBJECTS']['teachers_ID'].apply(ast.literal_eval)

        dataframes['SSG_TEACHERS']['start_hour_index'] = dataframes['SSG_TEACHERS']['start_hour_index'].apply(ast.literal_eval)
        dataframes['SSG_TEACHERS']['end_hour_index'] = dataframes['SSG_TEACHERS']['end_hour_index'].apply(ast.literal_eval)
        dataframes['SSG_TEACHERS']['days'] = dataframes['SSG_TEACHERS']['days'].apply(ast.literal_eval)
    else:
        for file in tables:
            if file_type == 'xlsx':
                dataframes[file] = pd.read_excel(os.path.join(path, file + '.' + file_type))
            if file_type == 'csv':
                dataframes[file] = pd.read_csv(os.path.join(path, file + '.' + file_type))
            elif file_type == 'mdf':
                table_name = file
                con = sqlite3.connect(path)
                sql_query = pd.read_sql(f'SELECT * FROM {table_name}', con)
                dataframes[file] = pd.DataFrame(sql_query, columns=sql_tables[table_name])

    return list(dataframes.values())


def split_subject_per_class(subjects_df, school_classes):
    """
    :param subjects_df: dataframe of all subjects
    :param school_classes: list of school_classes
    :return: returns splitet into classes lists of subjects
    """
    subject_per_class = {}
    for school_class in school_classes:
        class_id = school_class.class_id
        subject_per_class_df = subjects_df.loc[subjects_df['class_ID'] == class_id]
        subject_per_class[class_id] = []
        for index, row in subject_per_class_df.iterrows():
            for _ in range(row['subject_count_in_week']):
                subject_per_class[class_id].append(
                    Subject(
                        subject_id=row['subject_ID'],
                        subject_name_id=row['subject_name_ID'],
                        class_id=row['class_ID'],
                        number_of_groups=row['number_of_groups'],
                        teachers_id=[x for x in row['teachers_ID']],
                        classroom_id=row['classroom_ID'],
                        subject_length=row['subject_length'],
                        lesson_hours_id=row['lesson_hours_ID']
                    )
                )
    return subject_per_class
