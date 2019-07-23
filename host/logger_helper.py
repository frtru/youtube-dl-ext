import logging
import datetime
import re
import traceback


def initialize_logger():
    # Set logger level to debug
    logger = logging.getLogger('youtube-dl-ext')
    logger.setLevel(logging.DEBUG)

    # Create file in relative folder "../logs"
    # with current date and time as name
    current_datetime = re.sub('-|:| ', '_', str(datetime.datetime.now()))
    fh = logging.FileHandler("../logs/" + current_datetime + ".log")
    fh.setLevel(logging.DEBUG)

    # Add information about time of the day to each message being logged
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

log = initialize_logger()


def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            log.error(traceback.format_exc())
    return wrapper
