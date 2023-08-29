import time

import pytest

from job import Job, JobStatus


@pytest.fixture
def job():
    def task_1():
        for i in range(3):
            time.sleep(1)
            yield
    return Job(fn=task_1, max_working_time=5, id_="job1")


def test_job_creation(job):
    assert isinstance(job, Job)
    assert job.status == JobStatus.NOT_STARTED


def test_job_run(job):
    job.run()
    assert job.status == JobStatus.STARTED

