import numpy

from settings import *
import pandas as pd
import os
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


def class_to_json(obj):
    def todict(_obj):
        if isinstance(_obj, list):
            _list = []
            for _value in _obj:
                _list.append(todict(_value))

            return _list
        elif (
            isinstance(_obj, (int, bool, float, str)) or
            _obj is None
        ):
            return _obj
        elif isinstance(_obj, numpy.int64):
            return int(_obj)
        else:
            _dict = {}

            iter_dict = _obj.items() if isinstance(_obj, dict) else _obj.__dict__.items()

            for key, value in iter_dict:
                if isinstance(key, numpy.int64):
                    key = int(key)

                if isinstance(value, list):
                    for _value in value:
                        _dict[key] = [todict(_value)]
                elif "class" in str(type(value)):
                    _dict[key] = todict(value)
                else:
                    _dict[key] = str(value)

            return _dict

    return todict(obj)


def schedule_to_json(schedule, time):
    with open(f'../data/json_schedule_{time}.json', 'a') as file:
        file.write('')
        json.dump(class_to_json(schedule), file)
