from uuid import uuid4
from typing import List, Callable, Optional

from logger import get_logger
from utils import timing_decorator, JobStatus

logger = get_logger()


class Job:
    def __init__(
            self,
            fn: Callable,
            id_: Optional[str] = None,
            args: Optional[tuple] = None,
            kwargs: Optional[dict] = None,
            start_at: Optional[str] = None,
            max_working_time: Optional[int] = None,
            tries: int = 0,
            max_tries: int = 0,
            dependencies: List[str] = None,
            status: JobStatus = JobStatus.NOT_STARTED,
    ) -> None:
        self.id_ = id_ or str(uuid4())
        self.args = args or tuple()
        self.kwargs = kwargs or dict()
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.max_tries = max_tries
        self.dependencies = dependencies or list()
        self.status = status
        self.fn = fn(*self.args, **self.kwargs)

    @timing_decorator
    def run(self):
        self.status = JobStatus.STARTED
        self.fn.send(None)

    def stop(self):
        self.status = JobStatus.PAUSED
        self.fn.close()
