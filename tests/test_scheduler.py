import time

import pytest

from scheduler import Scheduler, Job, JobStatus


@pytest.fixture
def job():
    def task_1():
        for i in range(3):
            time.sleep(1)
            yield
    return Job(fn=task_1, max_working_time=5, id_="job1")


# Test the Scheduler class
def test_scheduler_creation():
    scheduler = Scheduler()
    assert isinstance(scheduler, Scheduler)
    assert scheduler.pool_size == 10


def test_scheduler_schedule(job):
    scheduler = Scheduler()
    scheduler.schedule(job)
    assert len(scheduler.queue) == 1

