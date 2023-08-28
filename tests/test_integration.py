import os

import pytest
import time
from scheduler import Scheduler, Job, JobStatus


@pytest.fixture
def scheduler():
    return Scheduler()


def test_create_and_delete_file(scheduler):
    # Create a job that creates a file
    def create_file():
        with open("test_file.txt", "w") as file:
            file.write("Test content")

    job = Job(create_file)
    scheduler.schedule(job)

    # Run the scheduler until the job is completed
    scheduler.run_until_complete([job])

    # Check if the file exists
    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    os.remove("test_file.txt")


def test_create_file_with_wait(scheduler):
    # Create a job that creates a file after waiting for 5 seconds
    def create_file_with_wait():
        time.sleep(5)
        with open("test_file.txt", "w") as file:
            file.write("Test content")

    job = Job(create_file_with_wait)
    scheduler.schedule(job)

    # Run the scheduler until the job is completed
    scheduler.run_until_complete([job])

    # Check if the file exists
    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    # Clean up: Delete the file
    os.remove("test_file.txt")


def test_create_file_in_future(scheduler):
    # Calculate the start time in the future (e.g., 5 seconds from now)
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 5))

    # Create a job that creates a file in the future
    def create_file_in_future():
        with open("test_file.txt", "w") as file:
            file.write("Test content")

    job = Job(create_file_in_future, start_at=start_time)
    scheduler.schedule(job)

    # Run the scheduler until the job is completed
    scheduler.run_until_complete([job])

    # Check if the file exists
    assert job.status == JobStatus.FINISHED_SUCCESSFULLY
    assert os.path.exists("test_file.txt")

    # Clean up: Delete the file
    os.remove("test_file.txt")

def test_create_file_with_retry_and_failure(scheduler):
    # Create a job that fails with 3 retries
    def create_file_with_retry_and_failure():
        raise Exception("Job failed")

    job = Job(create_file_with_retry_and_failure, max_tries=3)
    scheduler.schedule(job)

    # Run the scheduler until the job is completed (will eventually fail)
    scheduler.run_until_complete([job])

    # Check if the job has failed
    assert job.status == JobStatus.FAILED

if __name__ == "__main__":
    pytest.main()
