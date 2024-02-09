from settings import *
import pandas as pd
import os
import sqlite3
import ast
import json


def load_data(
        path='.',
        tables=settings.DF_NAMES,
        file_type='xlsx',
        sql_tables={}
):
    """
    :param path: path to either SQL database or folder with tables of type CSV or Excel
    :param tables: list of files/tables
    :param file_type: type of file to read, can be xlsx (Excel file), CSV (comma-separated values), defaults to xlsx
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

    dataframes['SSG_SUBJECTS']['teachers_ID'] = dataframes['SSG_SUBJECTS']['teachers_ID'].apply(ast.literal_eval)
    dataframes['SSG_SUBJECTS']['classroom_types'] = dataframes['SSG_SUBJECTS']['classroom_types'].apply(ast.literal_eval)

    dataframes['SSG_TEACHERS']['start_hour_index'] = dataframes['SSG_TEACHERS']['start_hour_index'].apply(ast.literal_eval)
    dataframes['SSG_TEACHERS']['end_hour_index'] = dataframes['SSG_TEACHERS']['end_hour_index'].apply(ast.literal_eval)
    dataframes['SSG_TEACHERS']['days'] = dataframes['SSG_TEACHERS']['days'].apply(ast.literal_eval)

    return list(dataframes.values())


def class_to_json(obj, file_path):
    def convert_to_dict(_obj):
        if isinstance(_obj, (int, float, str, bool)):
            return _obj
        elif isinstance(_obj, dict):
            return {k: convert_to_dict(v) for k, v in _obj.items()}
        elif isinstance(_obj, (list, tuple)):
            return [convert_to_dict(item) for item in _obj]
        elif hasattr(_obj, '__dict__'):
            return {k: convert_to_dict(v) for k, v in _obj.__dict__.items() if not k.startswith('__')}
        else:
            return str(_obj)

    with open(file_path, 'w') as file:
        json.dump(convert_to_dict(obj), file, indent=4)


def schedule_to_json(schedule, time):
    with open(f'./data/json_schedule_{time}.json', 'w', encoding='utf-8') as file:
        class_to_json(schedule, file)
