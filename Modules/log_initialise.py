#packages
from datetime import datetime
import logging
import os

def setup_logging(log_dir:str,timestamp:str):
    """This will initialise the logger

    Args:
        log_dir (str): where to save the log
        timestamp (str): this will be the name of the log file
    """

    #make a folder for log files if it doesn't already exist
    os.makedirs(log_dir, exist_ok = True)
    log_filename = f'{log_dir}/{timestamp}.log'

    # Configure logging so messages are written to the log file
    logging.basicConfig(
        filename=log_filename,
        format='%(asctime)s - %(levelname)s - %(message)s',
        level= logging.INFO
    )

    #Making a logger and confirming it has been set up
    #Return = def output
    return logging.getLogger()

