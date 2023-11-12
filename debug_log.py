from settings import settings


def debug_log(file_name, *args, **kwargs):
    if not settings.DEBUG:
        return
    print(*args, **kwargs)
    with open(f'logs/{file_name}/{file_name}.txt', 'a') as f:
        f.write('------------------------------------\n')
        for arg in args:
            f.write(str(arg)+' ')
        f.write('\n------------------------------------\n')
