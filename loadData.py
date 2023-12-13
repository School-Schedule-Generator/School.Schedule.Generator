from settings import *
import pandas as pd
import os
import sqlite3
from subject import *
from teacher import  *
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
    for file in tables:
        if file_type == 'xlsx':
            try:
                dataframes[file] = pd.read_excel(os.path.join(settings.TEST_DATA_PATH, file + '.' + file_type))
            except FileNotFoundError:
                dataframes[file] = pd.read_excel(os.path.join(settings.TEST_DATA_PATH, file + '.' + 'ods'), engine="odf")
        if file_type == 'csv':
            dataframes[file] = pd.read_csv(os.path.join(settings.TEST_DATA_PATH, file + '.' + file_type))
        elif file_type == 'mdf':
            # TODO: change to proper conection to sql
            table_name = file
            con = sqlite3.connect(settings.BASE_DATA_PATH)
            sql_query = pd.read_sql(f'SELECT * FROM {table_name}', con)
            dataframes[file] = pd.DataFrame(sql_query, columns=settings.COLLUMN_NAMES[table_name])

    dataframes['SSG_SUBJECTS']['teachers_ID'] = dataframes['SSG_SUBJECTS']['teachers_ID'].apply(ast.literal_eval)

    dataframes['SSG_TEACHERS']['start_hour_index'] = dataframes['SSG_TEACHERS']['start_hour_index'].apply(ast.literal_eval)
    dataframes['SSG_TEACHERS']['end_hour_index'] = dataframes['SSG_TEACHERS']['end_hour_index'].apply(ast.literal_eval)
    dataframes['SSG_TEACHERS']['days'] = dataframes['SSG_TEACHERS']['days'].apply(ast.literal_eval)

    return list(dataframes.values())
