from settings import *
import pandas as pd
import os
import sqlite3

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
