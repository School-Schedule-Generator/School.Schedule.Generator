from .settings import settings


def debug_log(file_name, *args, **kwargs):
    """
    :param file_name: file to log to
    :param args: args for print
    :param kwargs: kwargs for print
    :description: functions is extension to print as it does the same but writes all of it in a file
    """
    if not settings.DEBUG:
        return
    print(*args, **kwargs)
    dir_name = f'logs/{file_name}'
    with open(f'{dir_name}/.log', 'a') as f:
        f.write('------------------------------------\n')
        for arg in args:
            f.write(str(arg)+' ')
        f.write('\n------------------------------------\n')
