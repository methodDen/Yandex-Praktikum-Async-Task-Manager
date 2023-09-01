import time
from enum import Enum
from typing import Callable
from tasks import (
    create_dirs_job,
    create_file_job,
    write_to_file_job,
    read_from_file_job,
    delete_file_job,
    delete_dir_job,
    get_swapi_data_job,
)
from exceptions import JobExecutionTimeLimitExceededException
from logger import get_logger

logger = get_logger()

FILE_NAME_FOR_JOB_FLOW_1 = './dir_4/job_file_1.txt'
FILE_NAME_FOR_JOB_FLOW_2 = './dir_2/job_file_2.txt'
FILE_NAME_FOR_JOB_FLOW_3 = './job_file_3.txt'
JOB_PICKLE_FILE_NAME = 'jobs.pickle'


class JobStatus(str, Enum):
    NOT_STARTED = 'NOT STARTED'
    STARTED = 'STARTED'
    PAUSED = 'PAUSED'
    POSTPONED = 'POSTPONED'
    FAILED = 'FAILED'
    FINISHED_SUCCESSFULLY = 'FINISHED_SUCCESSFULLY'


function_name_to_function_mapping = {
    'create_dirs_job': create_dirs_job,
    'create_file_job': create_file_job,
    'write_to_file_job': write_to_file_job,
    'read_from_file_job': read_from_file_job,
    'delete_file_job': delete_file_job,
    'delete_dir_job': delete_dir_job,
    'get_swapi_data': get_swapi_data_job,
}


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
            raise JobExecutionTimeLimitExceededException

        return result

    return wrapper
