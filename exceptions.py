class QueueLengthExceededException(Exception):
    pass


class JobExecutionFailedException(Exception):
    pass


class JobExecutionTimeLimitExceededException(Exception):
    pass