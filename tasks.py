import os
import requests
from utils import sleep_random_time
from logger import get_logger

logger = get_logger()


def create_file_job(file_path: str) -> None:
    sleep_random_time()
    with open(file_path, 'w') as file:
        file.write('Random first line\n')
    logger.info(f"File %s successfully created and data written", file_path)
    yield


def write_to_file_job(file_path: str) -> None:
    sleep_random_time()
    with open(file_path, 'a') as f:
        f.writelines([f'Random text {i + 1}\n' for i in range(10)])
    logger.info('Writing to file %s finished', file_path,)
    yield


def read_from_file_job(file_path: str) -> None:
    sleep_random_time()
    with open(file_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            logger.info(f'Line # %d: %s', i + 1, line.strip('\n'))
            yield
    logger.info('Reading from file %s finished', file_path)


def delete_file_job(file_path: str) -> None:
    sleep_random_time()
    if os.path.exists(file_path):
        os.unlink(file_path)
        logger.info(f"File %s successfully deleted", file_path)
        yield
    else:
        logger.info(f"File %s doesn't exist", file_path)


def create_dirs_job() -> None:
    for i in range(5):
        sleep_random_time()
        path = f'./dir_{i + 1}'
        os.mkdir(path)
        logger.info('Created directory %s', path)
        yield
    logger.info('Directory creation finished')


def delete_dir_job() -> None:
    sleep_random_time()
    for i in range(3):
        path = f'./dir_{i + 1}'
        os.rmdir(path)
        logger.info('Deleted directory %s', path)
        yield
    logger.info('Directory deletion finished')


def get_swapi_data_job():
    sleep_random_time()
    data = requests.get('https://swapi.dev/api/people/1/')
    logger.info('Got data from swapi')
    yield
    logger.info('Data from swapi: %s', data.json())
    yield
