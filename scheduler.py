import pickle
from collections import deque, defaultdict
from typing import List
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

    def schedule(self, job: Job) -> None:
        if len(self.queue) >= self.pool_size:
            raise QueueLengthExceededException

        self.queue.appendleft(job)
        logger.info(f'Job %s added to queue' % job.id_)

        if job.dependencies:
            logger.info(f'Job %s has dependencies' % job.id_)
            for dependency in job.dependencies:
                logger.info(f'Job %s has dependency %s' % (job.id_, dependency))
                self.dependency_mapping[dependency].append(job)


    def run(self):
        pass

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