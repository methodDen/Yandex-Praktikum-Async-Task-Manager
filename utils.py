import logging
import sys

# Constants
FILE_NAME_FOR_TASK = 'task_file.txt'


def get_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
    )
    return logging.getLogger('schedule-logger')


def sleep_random_time():
    import random
    import time
    time.sleep(random.uniform(1, 5))


def timing_decorator(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'Время выполнения функции {func.__name__}: {end - start}')