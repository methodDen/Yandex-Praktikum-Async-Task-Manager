import os
import requests
from utils import sleep_random_time, FILE_NAME_FOR_JOB, get_logger

logger = get_logger()

# flow 1 : create_dir_task => create_file_task => write_to_file_task => read_from_file_task
# flow 2 : create_dir_task => create_file_task => delete_file_task => delete_dir_task
# flow 3: get_swapi_data, create_file_task (random time + retries)


def create_file_task() -> None:
    sleep_random_time()
    with open(FILE_NAME_FOR_JOB, 'w') as file:
        file.write('Random first line\n')
    logger.info(f"File %s successfully created and data written", FILE_NAME_FOR_JOB)
    yield


def write_to_file_task() -> None:
    sleep_random_time()
    with open(FILE_NAME_FOR_JOB, 'a') as f:
        f.writelines([f'Random text {i + 1}\n' for i in range(10)])
    logger.info('Writing to file finished')
    yield


def read_from_file_task() -> None:
    sleep_random_time()
    with open(FILE_NAME_FOR_JOB, 'r') as f:
        for i, line in enumerate(f.readlines()):
            logger.info(f'Line # %d: %s', i + 1, line.strip('\n'))
            yield
    logger.info('Reading from file finished')


def delete_file_task() -> None:
    sleep_random_time()
    if os.path.exists(FILE_NAME_FOR_JOB):
        os.unlink(FILE_NAME_FOR_JOB)
        logger.info(f"File %s successfully deleted", FILE_NAME_FOR_JOB)
        yield
    else:
        logger.info(f"File %s doesn't exist", FILE_NAME_FOR_JOB)


def create_dirs_task() -> None:
    for i in range(5):
        sleep_random_time()
        path = f'./dir_{i + 1}'
        os.mkdir(path)
        logger.info('Created directory %s', path)
        yield
    logger.info('Directory creation finished')


def delete_dir_task() -> None:
    sleep_random_time()
    for i in range(3):
        path = f'./dir_{i + 1}'
        os.rmdir(path)
        logger.info('Deleted directory %s', path)
        yield
    logger.info('Directory deletion finished')


def get_swapi_data():
    sleep_random_time()
    data = requests.get('https://swapi.dev/api/people/1/')
    logger.info('Got data from swapi')
    yield
    logger.info('Data from swapi: %s', data.json())
    yield
