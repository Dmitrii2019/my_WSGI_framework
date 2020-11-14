from datetime import datetime
import time


def debug(function):
    def wrapped(*args, **kwargs):
        start_time = datetime.now()
        res = function(*args, **kwargs)
        print(f'вызвана функции - {function.__name__} '
              f'время ее выполнения {datetime.now() - start_time}')
        return res
    return wrapped


if __name__ == "__main__":
    @debug
    def func():
        time.sleep(1)
        return 'test'

    func()

