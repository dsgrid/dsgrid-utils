import logging
from enum import Enum, auto

import numpy as np
import pandas as pd

from dsgutils import DSGridValueError, DSGridNotImplementedError

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Enumerations (regular, Python enumerations)
# ------------------------------------------------------------------------------

def ensure_enum(cls, val):
    """
    Returns the instance of cls that corresponds to val. cls is expected to be 
    an enum-type class.

    Parameters
    ----------
    cls : an enum class
    val : str or cls object

    Returns
    -------
    cls object
    """
    if isinstance(val, str):
        return cls[val]
    return cls(val)

    
# ------------------------------------------------------------------------------
# Time, especially as represented in pandas.DateTimeIndex
# ------------------------------------------------------------------------------


def assert_datetime_index(index):
    if not isinstance(index, pd.DatetimeIndex):
        raise DSGridValueError("Expected a pandas.DatetimeIndex, but got a "
            f"{type(index)}:\n{index}")


def make_index_datetime(df):
    if not isinstance(df.index, pd.DatetimeIndex):
        logger.warning("Converting pf.DataFrame index to pd.DatetimeIndex. "
            f"Before:\n{df.index}")
        df.index = pd.to_datetime(df.index)
        logger.warning(f"After:\n{df.index}")
    return


def get_time_step(index, check_integrity = True):
    """
    Returns
    -------
    None or datetime.timedelta
    """
    assert_datetime_index(index)

    dt = index.values[1] - index.values[0]
    if check_integrity:
        prev_val = None
        for i, val in enumerate(index.values):
            if i > 0:
                if abs((val - prev_val - dt) / np.timedelta64(1, 's')) > 0:
                    raise DSGridValueError("Non-constant time step. First "
                        f"time step of {dt / np.timedelta64(1, 's')} s, but {i}'th time "
                        f"step of {(val - prev_val) / np.timedelta64(1, 's')}")
            prev_val = val
    return dt


def get_time_duration(index):
    """
    Returns
    -------
    None or datetime.timedelta
    """
    assert_datetime_index(index)
    
    return index.values[-1] - index.values[0]


def get_time_extents(index):
    """
    Returns
    -------
    None or tuple of datetime.datetime
        If not None, returns (start_time, end_time)
    """
    assert_datetime_index(index)

    return (index.values[0], index.values[-1])


class TimeUnits(Enum):
    year = auto()
    month = auto()
    week = auto()
    day = auto()
    hour = auto()
    minute = auto()
    second = auto()


def to_time_unit(timedelta, time_unit):
    time_unit = ensure_enum(TimeUnits, time_unit)

    # timedelta in seconds
    result = timedelta / np.timedelta64(1, 's')
    if time_unit == TimeUnits.second:
        return result
    # in minutes
    result /= 60.0
    if time_unit == TimeUnits.minute:
        return result
    # in hours
    result /= 60.0
    if time_unit == TimeUnits.hour:
        return result
    # in days
    result /= 24.0
    if time_unit == TimeUnits.day:
        return result

    raise DSGridNotImplementedError(f"timedelta {timedelta!r} can only be "
        "converted directly to seconds, minutes, hours or days. Was asked to "
        f"convert to {time_unit}")
