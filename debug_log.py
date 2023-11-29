from settings import settings


def debug_log(file_name, *args, **kwargs):
    """
    :param file_name: file to log to
    :param args: args for print
    :param kwargs: kwargs for print
    :description: functions is extention to print as it does the same but writes all of it in a file
    """
    if not settings.DEBUG:
        return
    print(*args, **kwargs)
    dir_name = f'logs/{file_name}'
    if '_schedule' in file_name:
        dir_name = f'logs/{file_name[:-9]}'
    with open(f'{dir_name}/{file_name}.txt', 'a') as f:

        if '_schedule' not in file_name:
            f.write('------------------------------------\n')
        for arg in args:
            f.write(str(arg)+' ')
        if '_schedule' not in file_name:
            f.write('\n------------------------------------\n')
