"""
`asus_nuc_wmi.version_control` provides an interface to the WMI version functions.
"""

from asus_nuc_wmi import NucWmiError, RETURN_ERROR
from asus_nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x09
VERSION_TYPE = [
    'version_control'
]


def version_control(control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    Returns the version for the WMI version control.

    Args:
      control_file: Sets the control file to use if provided, otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the ASUS NUC LED control file to stderr.
      metadata: Metadata that may be required to change functional behavior.
    Exceptions:
      Raises `asus_nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      Tuple of two bytes representing the version number.
    """

    version_control_byte_list = [
        METHOD_ID,
        VERSION_TYPE.index('version_control')
    ]

    write_control_file(version_control_byte_list, control_file=control_file, debug=debug)

    version_control_result = read_control_file(control_file=control_file, debug=debug)

    error_code = version_control_result[0]
    version_byte_1 = version_control_result[1]
    version_byte_2 = version_control_result[2]

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    return tuple([version_byte_2, version_byte_1])
