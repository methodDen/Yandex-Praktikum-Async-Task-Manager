import time
from enum import Enum
from typing import Callable
from logger import get_logger

logger = get_logger()

FILE_NAME_FOR_JOB_FLOW_1 = './dir_4/job_file_1.txt'
FILE_NAME_FOR_JOB_FLOW_2 = './dir_2/job_file_2.txt'
FILE_NAME_FOR_JOB_FLOW_3 = './job_file_3.txt'


class JobStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    STARTED = 'STARTED'
    PAUSED = 'PAUSED'
    POSTPONED = 'POSTPONED'
    FAILED = 'FAILED'
    FINISHED_SUCCESSFULLY = 'FINISHED_SUCCESSFULLY'


def sleep_random_time():
    import random
    import time
    time.sleep(random.uniform(1, 5))


def timing_decorator(func: Callable):

    def wrapper(self, *args, **kwargs):

        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        passed_time = end_time - start_time

        max_working_time = self.max_working_time

        if max_working_time and passed_time > max_working_time:
            logger.error("Function exceeded the maximum possible execution time. Actual time: %s when "
                         "this amount of time is expected: %s",
                         passed_time, max_working_time)
        return result

    return wrapper
