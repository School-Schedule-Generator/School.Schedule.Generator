import copy
import sys
import numpy
import pandas as pd
import os
import ast
import json
import sqlite3
from .settings import *
from ..models import *


def table_import_validation(dataframes, table):
    if len(set(settings.COLUMN_NAMES[table])) < len(set(dataframes[table].columns.values)):
        print(
            f"There is too many columns in {table}\n"
            f"Unwanted columns: {set(dataframes[table].columns.values) - set(settings.COLUMN_NAMES[table])}",
            file=sys.stderr
        )
        return False
    elif set(settings.COLUMN_NAMES[table]) != set(dataframes[table].columns.values):
        print(
            f"Column names in passed in data file: \"{table}\" don't mach default schedule column names:\n"
            f"Passed in: {set(dataframes[table].columns.values) - set(settings.COLUMN_NAMES[table])}\n"
            f"Needed: {set(settings.COLUMN_NAMES[table]) - set(dataframes[table].columns.values)}",
            file=sys.stderr
        )
        return False

    return True


def load_data(
        path=None,
        tables=settings.DF_NAMES,
        dtype='xlsx',
        schedule=None
):
    """
    :param path: path to either SQL database or folder with tables of type CSV or Excel
    :param tables: list of files/tables
    :param dtype: type of data to read, can be .xlsx/.ods (Excel file), .csv (comma-separated values) or sql, defaults to xlsx
    :param schedule: id of the schedule to pull from sql database
    :return: list of pandas dataframes or False if files don't match schedule data
    """

    if settings.DEBUG:
        path = settings.TEST_DATA_PATH
    elif not settings.DEBUG and path == settings.TEST_DATA_PATH:
        raise FileNotFoundError(f"Path {settings.TEST_DATA_PATH} is reserved for debugging purposes, please specify \
        a different path when using this function in release mode.")
    elif not settings.DEBUG and path is None:
        path = settings.BASE_DATA_PATH

    dataframes = {}

    if dtype == 'sql':
        # try:
        #     conn = sqlite3.connect(settings.DATABASE_NAME)
        # except sqlite3.Error:
        #     print(f'Failed to connect to database...', file=sys.stderr)
        #     return False
        #     columns = settings.SQLTABLES[table]['Columns']
        #     sql_table = settings.SQLTABLES[table]['Name']
        #
        #     query_db = pd.read_sql_query(f'SELECT {", ".join(columns)} FROM {sql_table} WHERE schedule_id_id={schedule_id}', conn)\

        for table in tables:
            table_to_model = {
                'SSG_LESSON_HOURS': LessonHours,
                'SSG_SUBJECT_NAMES': SubjectNames,
                'SSG_SUBJECTS': Subject,
                'SSG_TEACHERS': Teachers,
                'SSG_CLASSES': Classes,
                'SSG_CLASSROOMS': Classrooms,
                'SSG_CLASSROOM_TYPES': ClassroomTypes
            }

            if table in table_to_model:
                model = table_to_model[table]
                query_db = pd.DataFrame(list(model.objects.filter(schedule_id=schedule).values()))

            column_mapper = dict(zip(settings.SQL_COLUMN_NAMES[table], settings.COLUMN_NAMES[table]))
            query_db = query_db.rename(columns=column_mapper)
            dataframes[table] = pd.DataFrame(query_db, columns=settings.COLUMN_NAMES[table])
    else:
        files_in_directory = os.listdir(path)
        for table in tables:
            file_exists = False
            for file in files_in_directory:
                if file.startswith(table):
                    file_exists = True
                    if dtype == 'xlsx':
                        try:
                            dataframes[table] = pd.read_excel(os.path.join(path, table + '.' + dtype))
                        except FileNotFoundError:
                            print(f'There is one or more files missing, please pass in: {file}.xlsx file or change directory of your\
                             data.', file=sys.stderr)
                            return False
                    elif dtype == 'ods':
                        try:
                            dataframes[table] = pd.read_excel(os.path.join(path, table + '.' + 'ods'), engine="odf")
                        except FileNotFoundError:
                            print(f'There is one or more files missing, please pass in: {file}.ods file or change directory\
                             of your data.', file=sys.stderr)
                            return False
                    elif dtype == 'csv':
                        try:
                            dataframes[table] = pd.read_csv(os.path.join(path, table + '.' + dtype))
                        except FileNotFoundError:
                            print(f'There is one or more files missing, please pass in: {file}.csv file or change directory\
                             of your data.', file=sys.stderr)
                            return False
                    else:
                        print(f'File type: {dtype} is not suported, please pass in files in .xlsx, .ods or .csv',
                              file=sys.stderr)
                        return False

            if not table_import_validation(dataframes, table):
                return False

            if not file_exists:
                print(f'There is one or more files missing, please pass in: {file} file or change directory of your data.', file=sys.stderr)
                return False

    dataframes['SSG_SUBJECTS']['teachers_id'] = dataframes['SSG_SUBJECTS']['teachers_id'].apply(ast.literal_eval)
    dataframes['SSG_SUBJECTS']['classroom_types'] = dataframes['SSG_SUBJECTS']['classroom_types'].apply(ast.literal_eval)
    dataframes['SSG_SUBJECTS']['teachers_id'] = dataframes['SSG_SUBJECTS']['teachers_id'].apply(lambda x: [int(i) for i in x])

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
                    _dict[key] = []
                    for _value in value:
                        _dict[key].append(todict(_value))
                elif "class" in str(type(value)):
                    _dict[key] = todict(value)
                else:
                    _dict[key] = str(value)

            return _dict

    return todict(obj)


def schedule_to_json(schedule, file_path=None):
    schedule_dict = class_to_json(schedule)
    if file_path:
        with open(f'{file_path}.json', 'a') as file:
            file.write('')
            json.dump(schedule_dict, file)

    return json.dumps(schedule_dict)
