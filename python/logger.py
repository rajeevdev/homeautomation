import logging
import logging.handlers
import sys
import os

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
                self.logger.log(self.level, message.rstrip())

def setupLogger():
    # Deafults
    if (os.name == "nt"):
        LOG_FILENAME = "../logging/automation.log"
        if not os.path.exists(os.path.dirname(LOG_FILENAME)):
            try:
                os.makedirs(os.path.dirname(LOG_FILENAME))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    else:
        LOG_FILENAME = "/var/log/automation.log"

    LOG_LEVEL = logging.DEBUG  # Could be e.g. "DEBUG" or "WARNING"

    # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
    # Give the logger a unique name (good practice)
    logger = logging.getLogger("deviceserver.log")
    # Set the log level to LOG_LEVEL
    logger.setLevel(LOG_LEVEL)
    # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    consoleHandler = logging.StreamHandler()
    # Format each log message like this
    formatter = logging.Formatter('%(asctime)s %(thread)d %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    # Attach the handler to the logger
    logger.addHandler(handler)
    logger.addHandler(consoleHandler)
    
    # Replace stdout with logging to file at INFO level
    sys.stdout = MyLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = MyLogger(logger, logging.INFO)

def info(msg):
    logger = logging.getLogger("deviceserver.log")
    logger.info(msg)
    
def debug(msg):
    logger = logging.getLogger("deviceserver.log")
    logger.debug(msg)
    
def error(msg):
    logger = logging.getLogger("deviceserver.log")
    logger.error(msg)
