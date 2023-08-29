import logging
import sys


def get_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
    )
    return logging.getLogger('schedule-logger')