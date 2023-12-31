import pickle
import time
from datetime import datetime
from collections import deque, defaultdict

from exceptions import QueueLengthExceededException
from job import Job, JobStatus
from logger import get_logger
from utils import (
    JOB_PICKLE_FILE_NAME,
    function_name_to_function_mapping,
)

logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.queue: deque[Job] = deque(maxlen=pool_size)
        self.dependency_mapping = defaultdict(list)
        self.dependency_status_mapping = dict()

    def run_until_complete(self, job_list: list[Job]) -> None:
        job_counter = 0

        while job_counter < len(job_list):
            try:
                self.schedule(job_list[job_counter])
                job_counter += 1
            except QueueLengthExceededException:
                try:
                    next(self.run())
                except StopIteration:
                    break

        while True:
            try:
                next(self.run())
            except StopIteration:
                break

        logger.info(f'All jobs are processed')

    def schedule(self, job: Job) -> None:
        if len(self.queue) >= self.pool_size:
            raise QueueLengthExceededException

        self.queue.appendleft(job)
        logger.info(f'Job %s added to queue' % job.id_)

        if job.dependencies:
            logger.info(f'Job %s has dependencies' % job.id_)
            for dependency in job.dependencies:
                logger.info(f'Job %s has dependency %s' % (job.id_, dependency))
                self.dependency_mapping[job].append(dependency)
                self.dependency_status_mapping[dependency] = JobStatus.NOT_STARTED

    def stop(self) -> None:
        queue_dump = deque()
        for job in self.queue:
            job.stop()
            queue_dump.appendleft({
                'id_': job.id_,
                'status': job.status,
                'tries': job.tries,
                'max_tries': job.max_tries,
                'dependencies': job.dependencies,
                'start_at': job.start_at,
                'max_working_time': job.max_working_time,
                'function_name': job.fn.__name__,
                'args': job.args,
                'kwargs': job.kwargs,
            })

        with open(JOB_PICKLE_FILE_NAME, 'wb') as f:
            pickle.dump(queue_dump, f)

    def restart(self):
        with open(JOB_PICKLE_FILE_NAME, 'rb') as f:
            queue_dump = pickle.load(f)

        for job_dump in queue_dump:
            job_function = function_name_to_function_mapping[job_dump['function_name']]
            job = Job(
                id_=job_dump['id_'],
                status=JobStatus.NOT_STARTED,
                tries=job_dump['tries'],
                max_tries=job_dump['max_tries'],
                dependencies=None,
                start_at=job_dump['start_at'],
                max_working_time=job_dump['max_working_time'],
                fn=job_function,
                args=job_dump['args'],
                kwargs=job_dump['kwargs'],
            )
            self.schedule(job)

        while True:
            try:
                next(self.run())
            except StopIteration:
                break

    def run(self) -> None:
        while self.queue:
            job = self.queue[-1]

            if not self.is_job_can_start(job, self.queue):
                continue

            try:
                logger.info(f'Job %s started' % job.id_)
                job.run()
            except StopIteration:
                job.status = JobStatus.FINISHED_SUCCESSFULLY
                logger.info(f'Job %s finished successfully' % job.id_)
                self.cleanup_after_job_execution(job, self.queue,)
                yield
                continue
            except Exception as e:
                logger.info(f'Job %s failed' % job.id_)
                if job.tries > job.max_tries:
                    job.status = JobStatus.FAILED
                    logger.info(f'Job %s finished unsuccessfully' % job.id_)
                    self.cleanup_after_job_execution(job, self.queue,)
                    yield
                else:
                    job.tries += 1
                    logger.info(f'Job %s failed, retrying again later' % job.id_)
                    self.queue.rotate(1)
                continue

            self.queue.rotate(1)

    def is_job_can_start(self, job: Job, job_queue: deque[Job]) -> bool:
        if job.dependencies:
            job_dependencies_ids = self.dependency_mapping[job]
            job_dependencies_statuses = [
                self.dependency_status_mapping[dependency_id]
                for dependency_id in job_dependencies_ids
            ]
            if not all(
                status in (JobStatus.FINISHED_SUCCESSFULLY, JobStatus.FAILED)
                for status in job_dependencies_statuses
            ):
                logger.info(f'Job %s has not started yet because of incomplete dependencies' % job.id_)
                job.status = JobStatus.POSTPONED
                job_queue.rotate(1)
                return False

        # check start at
        if job.start_at and time.time() < datetime.strptime(job.start_at, '%Y-%m-%d %H:%M:%S').timestamp():
            logger.info(f'Job %s has not started yet' % job.id_)
            job_queue.rotate(1)
            return False

        return True

    def cleanup_after_job_execution(self, job: Job, job_queue: deque[Job]) -> None:
        for dependent_job, independent_job_list in self.dependency_mapping.items():
            if job.id_ in independent_job_list:
                independent_job_list.remove(job.id_)

        self.dependency_status_mapping[job.id_] = job.status
        job_queue.pop()
