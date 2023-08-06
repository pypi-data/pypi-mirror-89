"""The logger module contains the configurations for the global

"""
import logging


def initLogger(verbose: bool = True,
               logfile: bool = True) -> logging.Logger:
    """Creates the log instance, if not present.
    """
    log: logging.Logger = logging.getLogger("FileWizard")
    logFormatter: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    fileHandler: logging.FileHandler = logging.FileHandler("debug.log",
                                                           mode="a")
    consoleFormatter: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    consoleHandler: logging.StreamHandler = logging.StreamHandler()
    fileHandler.setFormatter(logFormatter)
    consoleHandler.setFormatter(consoleFormatter)
    log.handlers.clear()
    if verbose is True:
        log.addHandler(consoleHandler)
    if logfile is True:
        log.addHandler(fileHandler)
    if logfile is False and verbose is False:
        nullHandler: logging.NullHandler = logging.NullHandler()
        log.addHandler(nullHandler)
    log.setLevel(logging.DEBUG)
    return log
