import pickle
from collections import deque
from typing import List

from job import Job, JobStatus
from utils import get_logger

logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10, file: str = 'jobs_storage.pkl',):
        self.pool_size = pool_size
        self.queue: deque[Job] = deque(maxlen=pool_size)
        self.storage_file: str = file

    def schedule(self, job_list: List[Job]):
        for job in job_list:
            if len(self.queue) < self.pool_size:
                self.queue.append(job)
                logger.info(f'Job %s added to queue' % job.id_)

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