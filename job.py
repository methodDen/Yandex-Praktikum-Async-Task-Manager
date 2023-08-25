from enum import Enum
from typing import List, Callable, Optional

from uuid import uuid4


class JobStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    STARTED = 'STARTED'
    PAUSED = 'PAUSED'
    POSTPONED = 'POSTPONED'
    FAILED = 'FAILED'
    FINISHED_SUCCESSFULLY = 'FINISHED_SUCCESSFULLY'


class Job:
    def __init__(
            self,
            fn: Callable,
            id_: Optional[str] = None,
            args: Optional[tuple] = None,
            kwargs: Optional[dict] = None,
            start_at: Optional[str] = None,
            working_time: int = 0,
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
        self.working_time = working_time
        self.max_working_time = max_working_time
        self.tries = tries
        self.max_tries = max_tries
        self.dependencies = dependencies or list()
        self.status = status
        self.fn = fn(*self.args, **self.kwargs)

    def run(self):
        self.status = JobStatus.STARTED
        self.fn.send(None)

    def pause(self):
        self.status = JobStatus.PAUSED

    def stop(self):
        self.status = JobStatus.FINISHED
