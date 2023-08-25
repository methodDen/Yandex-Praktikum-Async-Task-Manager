import logging
import sys
import time
from typing import Callable

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


def timing_decorator(func: Callable):

    def wrapper(self, *args, **kwargs):

        if not self.max_running_time:
            return func(self, *args, **kwargs)

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Время выполнения функции {func.__name__}: {end - start}')