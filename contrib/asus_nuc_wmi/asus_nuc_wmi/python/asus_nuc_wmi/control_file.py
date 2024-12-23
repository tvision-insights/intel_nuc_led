"""
`asus_nuc_wmi.control_file` module provides interfaces for interacting with ASUS NUC LED kernel module control file.
"""

import sys

from asus_nuc_wmi import CONTROL_FILE, NucWmiError


def read_control_file(control_file=None, debug=False):
    """
    Read the ASUS NUC LED control file hex bytes string.

    Args:
      control_file: Sets the control file to use if provided, otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the ASUS NUC LED control file to stderr.
    Exceptions:
      Raises normal `IOError`/`OSError` on failure to read the control file, or `ValueError` for hex conversion error.
    Returns:
      Tuple of ints representing the hex numbers read in from the control file.
    """

    with open(control_file or CONTROL_FILE, 'rb', buffering=0) as fin:
        raw_hex_byte_string = fin.read(767).decode('utf8')

    # Remove the new line and null char the driver leaves
    raw_hex_byte_string = raw_hex_byte_string.rstrip("\x00").rstrip("\n")

    if debug:
        print('asus_nuc_wmi read: ', raw_hex_byte_string, file=sys.stderr)

    byte_list = [int(hex_byte_str, 16) for hex_byte_str in raw_hex_byte_string.split(' ')]

    for hex_byte in byte_list:
        if hex_byte < 0 or hex_byte > 255:
            raise NucWmiError('ASUS NUC WMI returned hex byte outside of 0-255 range')

    if len(byte_list) != 256:
        raise NucWmiError('ASUS NUC WMI control file did not return an expected 256 bytes')

    return tuple(byte_list)


def write_control_file(int_byte_list, control_file=None, debug=False):
    """
    Converts the integer byte list into a hex byte string and writes it to the ASUS NUC control file.

    Args:
      control_file: Sets the control file to use if provided, otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the ASUS NUC LED control file to stderr.
      int_byte_list: List of integers bytes to be converted into a hex byte string to send to the ASUS NUC control file.
                     May be int byte strings. Integers must be 0-255.
    Exceptions:
      Raises normal `IOError`/`OSError` on failure to read the control file, `ValueError` for hex conversion error, or
      `asus_nuc_wmi.NucWmiError` for input value errors.
    """

    if len(int_byte_list) > 0:
        if int(int_byte_list[0]) < 0 or int(int_byte_list[0]) > 4294967295:
            raise NucWmiError('Error (ASUS NUC LED method id 32bit value must be 0-4294967295)')

        for int_byte in int_byte_list[1:]:
            if int(int_byte) < 0 or int(int_byte) > 255:
                raise NucWmiError('Error (ASUS NUC LED byte values must be 0-255)')
    else:
        raise NucWmiError('Error (ASUS NUC LED byte values must at least provide the first 32bit method id)')

    raw_hex_byte_string = ' '.join(
        ['{:02x}'.format(int(int_byte)) for int_byte in int_byte_list + ([0] * (257 - len(int_byte_list)))]
    )

    if debug:
        print('asus_nuc_wmi write: ', raw_hex_byte_string, file=sys.stderr)

    with open(control_file or CONTROL_FILE, 'wb', buffering=0) as fout:
        fout.write(raw_hex_byte_string.encode('utf8'))
