from collections import deque
from typing import List

from job import Job
from utils import get_logger

logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10, file: str = 'jobs.pkl',):
        self.pool_size = pool_size
        self.executable_queue: deque[Job] = deque(maxlen=pool_size)
        self.global_queue: deque[Job] = deque()
        self.storage_file: str = file
        self.dependent_jobs_mapping_dict = {}
        self.dependent_jobs_status_dict = {}

    def schedule(self, job_list: List[Job]):
        for job in job_list:
            if len(self.queue) < self.pool_size:
                self.queue.append(job)
                logger.info(f'Job %s added to queue' % job.id_)

    def run(self):
        pass

    def restart(self):
        pass

    def stop(self):
        for task in self.executable_queue:
            task.pause()
