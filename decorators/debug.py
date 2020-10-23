from datetime import datetime
import time


def debug(function):
    def wrapped(*args):
        start_time = datetime.now()
        res = function(*args)
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

