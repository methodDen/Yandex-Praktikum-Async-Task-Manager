import os

import pytest
import time
from scheduler import Scheduler, Job, JobStatus


@pytest.fixture
def scheduler():
    return Scheduler()


def test_create_and_delete_file(scheduler):
    def create_file():
        with open("test_file.txt", "w") as file:
            file.write("Test content")
            yield

    job = Job(create_file)
    scheduler.schedule(job)

    scheduler.run_until_complete([job])

    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    os.remove("test_file.txt")


def test_create_file_with_wait(scheduler):
    def create_file_with_wait():
        time.sleep(5)
        with open("test_file.txt", "w") as file:
            file.write("Test content")
            yield

    job = Job(create_file_with_wait)
    scheduler.schedule(job)

    scheduler.run_until_complete([job])

    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    os.remove("test_file.txt")


def test_create_file_in_future(scheduler):
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 5))

    def create_file_in_future():
        with open("test_file.txt", "w") as file:
            file.write("Test content")
            yield

    job = Job(create_file_in_future, start_at=start_time)
    scheduler.schedule(job)

    scheduler.run_until_complete([job])

    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    os.remove("test_file.txt")


def test_create_file_with_retry_and_success(scheduler):
    def create_file_with_retry_and_failure():
        time.sleep(5)
        yield

    job = Job(create_file_with_retry_and_failure, max_tries=3, max_working_time=5)
    scheduler.schedule(job)

    scheduler.run_until_complete([job])

    assert job.status == JobStatus.FINISHED_SUCCESSFULLY


if __name__ == "__main__":
    pytest.main()
