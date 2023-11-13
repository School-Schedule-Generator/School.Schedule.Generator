from settings import settings


def debug_log(file_name, *args, **kwargs):
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
            f.write('------------------------------------\n')
