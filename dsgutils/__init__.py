import datetime
import logging

from ._version import __version__

logger = logging.getLogger(__name__)


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
    

log_levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

log_level_strs = {
    logging.CRITICAL: 'CRITICAL',
    logging.ERROR: 'ERROR',
    logging.WARNING: 'WARNING',
    logging.INFO: 'INFO',
    logging.DEBUG: 'DEBUG'
}

def get_log_level(option, default_level = logging.WARNING):
    """
    Get the logging level from a str option. Useful for passing desired log level
    in on the command line.

    Parameters
    ----------
    option : str
    default_level : one of the log_levels.values()

    Returns
    -------
    one of the log_levels.values()
    """
    level = None
    if isinstance(option, str):
        level = log_levels.get(option.upper())
    elif option in log_level_strs:
        level = log_levels[log_level_strs[option]]
    if level is None:
        logger.warning(f"Unable to parse {option} as a log level. Defaulting to {default_level}.")
        level = default_level
    return level

def get_log_level_str(log_level):
    """
    Get a str that corresponds to log_level. Useful, e.g., for saving a log 
    level to json.
    """
    return log_level_strs[log_level]
