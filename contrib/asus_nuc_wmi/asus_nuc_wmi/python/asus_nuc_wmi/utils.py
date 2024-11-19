"""
`asus_nuc_wmi.utils` provides utility functions for the WMI functions.
"""

import fcntl

from asus_nuc_wmi import NucWmiError

EXCLUSIVE_BLOCKING_FILE_LOCK = fcntl.LOCK_EX
EXCLUSIVE_NON_BLOCKING_FILE_LOCK = fcntl.LOCK_EX | fcntl.LOCK_NB


def acquire_file_lock(filehandle, blocking_file_lock=False):
    """
    Acquires a lock on the open file descriptor.

    Args:
      filehandle: File object handle to acquire file lock on. Must respond to fileno and name requests.
    Exceptions:
      Raises `NucWmiError` on failure to acquire the NUC WMI lock file.
    Returns:
      None
    """

    if blocking_file_lock:
        lock_type = EXCLUSIVE_BLOCKING_FILE_LOCK
    else:
        lock_type = EXCLUSIVE_NON_BLOCKING_FILE_LOCK

    try:
        fcntl.flock(filehandle.fileno(), lock_type)
    except (IOError, OSError) as err:
        raise NucWmiError(
            'Error (ASUS NUC WMI failed to acquire lock file %s: %s)' % (filehandle.name, str(err))
        ) from err


def defined_indexes(items):
    """
    Returns the indexes from the items list with a non None value.

    Args:
      items: Item list for which to return non None indexes.
    Returns:
      List of index numbers that had non None values.
    """

    if issubclass(items.__class__, list):
        return [index for index, value in enumerate(items) if value is not None]

    return []
