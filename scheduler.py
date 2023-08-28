import pickle
import time
from collections import deque, defaultdict
from exceptions import QueueLengthExceededException
from job import Job, JobStatus
from utils import get_logger

logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10, file: str = 'jobs_storage.pkl',):
        self.pool_size = pool_size
        self.queue: deque[Job] = deque(maxlen=pool_size)
        self.storage_file: str = file
        self.dependency_mapping = defaultdict(list)
        self.dependency_status_mapping = dict()

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

    def run(self) -> None:
        while self.queue:
            task = self.queue[-1]


    def is_job_can_start(self, job: Job, job_queue: deque[Job]) -> bool:
        # check dependencies statuses
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
        if job.start_at and time.time() < job.start_at:
            logger.info(f'Job %s has not started yet' % job.id_)
            job_queue.rotate(1)
            return False

        return True


    def restart(self) -> None:
        with open(self.storage_file, 'rb') as f:
            tasks_list = pickle.load(f)

        for task in tasks_list:
            task.status = JobStatus.NOT_STARTED
            self.schedule(task)

        self.run()


    def stop(self) -> None:
        for task in self.queue:
            task.pause()

        with open(self.storage_file, 'wb') as f:
            pickle.dump(self.queue, f, pickle.HIGHEST_PROTOCOL)