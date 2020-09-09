import datetime
import logging

from ._version import __version__


# ------------------------------------------------------------------------------
# Exception Classes
# ------------------------------------------------------------------------------

class DSGridError(Exception): pass

class DSGridAttributeError(DSGridError, AttributeError): pass

class DSGridIndexError(DSGridError, IndexError): pass

class DSGridNotImplementedError(DSGridError, NotImplementedError): pass

class DSGridRuntimeError(DSGridError, RuntimeError): pass

class DSGridValueError(DSGridError, ValueError): pass


# ------------------------------------------------------------------------------
# Runtime Helpers
# ------------------------------------------------------------------------------

def current_datetime(format='%Y_%m_%d_%Hh%Mm%Ss'):
    dt = datetime.datetime.strftime(datetime.datetime.now(), format)
    return dt


# ------------------------------------------------------------------------------
# Logging Helpers
# ------------------------------------------------------------------------------

DEFAULT_LOG_FORMAT = '%(asctime)s|%(levelname)s|%(name)s|\n\t%(message)s'


def start_console_log(log_level=logging.WARN,log_format=DEFAULT_LOG_FORMAT):
    """
    Starts logging to the console.
    Parameters
    ----------
    log_level : enum
        logging package log level, i.e. logging.ERROR, logging.WARN, 
        logging.INFO or logging.DEBUG
    log_format : str
        format string to use with the logging package
    
    Returns
    -------
    logging.StreamHandler
        console_handler
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    logformat = logging.Formatter(log_format)
    console_handler.setFormatter(logformat)
    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(console_handler)
    return console_handler


def start_file_log(filename, log_level=logging.WARN, log_format=DEFAULT_LOG_FORMAT):
    """
    Starts logging to a file.
    Parameters
    ----------
    filename : str
        path to the log file
    log_level : enum
        logging package log level, i.e. logging.ERROR, logging.WARN, 
        logging.INFO or logging.DEBUG
    log_format : str
        format string to use with the logging package
    Returns
    -------
    logging.FileHandler
        logfile
    """
    logfile = logging.FileHandler(filename=filename)
    logfile.setLevel(log_level)
    logformat = logging.Formatter(log_format)
    logfile.setFormatter(logformat)
    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(logfile)
    return logfile
    

def end_file_log(logfile):
    logfile.close()
    logging.getLogger().removeHandler(logfile)
    