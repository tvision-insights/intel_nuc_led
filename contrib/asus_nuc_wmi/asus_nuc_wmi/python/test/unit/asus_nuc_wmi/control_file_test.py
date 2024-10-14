"""
The `test.unit.asus_nuc_wmi.control_file_test` module provides unit tests for the functions in
`asus_nuc_wmi.control_file`.

Classes:
    TestControlFile: A unit test class for the functions in `asus_nuc_wmi.control_file`.
"""

import os
import sys
import unittest

from tempfile import NamedTemporaryFile

from mock import patch

from asus_nuc_wmi import NucWmiError
from asus_nuc_wmi.control_file import read_control_file, write_control_file

import asus_nuc_wmi


class TestControlFile(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.control_file`

    Methods:
        setUp: Unit test initialization.
        tearDown: Unit test cleanup.
        test_read_control_file: Tests that `read_control_file` raises the expected exception when
                                asus_nuc_wmi.CONTROL_FILE doesnt exist, tests that exception is raised if less than 256
                                bytes are returned, tests that overriding control_file with existing file works,
                                tests that overriding control_file with non existing file raises exception, and tests
                                that exception is raised if ASUS NUC WMI provides a hex byte value outside of the 0-255
                                range.
        test_write_control_file: Tests that `write_control_file` raises the expected exception when
                                 asus_nuc_wmi.CONTROL_FILE doesnt exist, tests that number of bytes written to control
                                 file are padded to 257 bytes if less than 257 bytes are passed in, tests that both
                                 integer and string bytes are accepted, tests that byte strings outside of 0-255 value
                                 raise an exception, tests that overriding control_file with different file works.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """
        with NamedTemporaryFile(delete=False) as control_file:
            self.control_file = control_file

        self.maxDiff = None # pylint: disable=invalid-name


    def tearDown(self):
        """
        Cleans up the unit tests.
        """

        self.control_file.close()

        os.unlink(self.control_file.name)


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that `read_control_file` raises exception when `asus_nuc_wmi.CONTROL_FILE` doesnt exist
        #           Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)):
            read_control_file(
                control_file=None
            )

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file2(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that `read_control_file` raise exception if less than 256 bytes are read
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write((("00 " * 128) + "00\n\x00").encode('utf8'))

        with self.assertRaises(NucWmiError) as byte_list_len_err:
            read_control_file(control_file=self.control_file.name, debug=False)

        self.assertEqual(str(byte_list_len_err.exception),
                         'ASUS NUC WMI control file did not return an expected 256 bytes')

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file3(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Test that overriding control file with existing file works
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write(("0D 0E 0A 0D" + (" 00" * 252) + "\n\x00").encode('utf8'))

        byte_list = (0x0D, 0x0E, 0x0A, 0x0D) + tuple([0x00] * 252)

        self.assertEqual(
            read_control_file(control_file=self.control_file.name, debug=False),
            byte_list
        )

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file4(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 4: Test that overriding control file with non existing file raises exception
        with NamedTemporaryFile() as temp_file:
            non_existent_file = temp_file

        with self.assertRaises((IOError, OSError)):
            read_control_file(control_file=non_existent_file.name, debug=False)

        asus_nuc_wmi_print.assert_not_called()


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file5(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 5: Test that exception is raised if NUC WMI returns a hex byte outside 0-255 range
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write(("FFF 0E 0A 0D" + (" 00" * 252) + "\n\x00").encode('utf8'))

        with self.assertRaises(NucWmiError) as err:
            read_control_file(control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception), 'ASUS NUC WMI returned hex byte outside of 0-255 range')

        asus_nuc_wmi_print.assert_not_called()


    @patch('asus_nuc_wmi.control_file.print')
    def test_read_control_file6(self, asus_nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 6: Test that debug logging prints read bytes
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write(("0D 0E 0A 0D" + (" 00" * 252) + "\n\x00").encode('utf8'))

        byte_list = (0x0D, 0x0E, 0x0A, 0x0D) + tuple([0x00] * 252)

        self.assertEqual(
            read_control_file(control_file=self.control_file.name, debug=True),
            byte_list
        )

        asus_nuc_wmi_print.assert_called_with(
            'asus_nuc_wmi read: ',
            "0D 0E 0A 0D" + (" 00" * 252),
            file=sys.stderr
        )


    @patch('asus_nuc_wmi.control_file.print')
    def test_write_control_file(self, asus_nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Tests that `write_control_file` raises the expected exception when `asus_nuc_wmi.CONTROL_FILE`
        #           doesnt exist. Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)):
            read_control_file(control_file=None, debug=False)

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_write_control_file2(self, asus_nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Tests that the number of bytes written to the control file are padded to 257 bytes, and that
        #           integer byte list is properly written to the control file.
        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        expected_byte_string = '0d 0e 0a 0d 00' + (' 00' * 252)

        write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(770).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_write_control_file3(self, asus_nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Tests that an string byte list is properly written to the control file
        byte_list = [str(0x0D), str(0x0E), str(0x0A), str(0x0D), str(0x00)]
        expected_byte_string = '0d 0e 0a 0d 00' + (' 00' * 252)

        write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(770).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_write_control_file4(self, asus_nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 4: Test that byte strings outside of the 0-255 value raise an exception
        byte_list = [0xFFF]

        with self.assertRaises(NucWmiError) as err:
            write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception), 'Error (ASUS NUC LED byte values must be 0-255)')

        asus_nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('asus_nuc_wmi.control_file.print')
    def test_write_control_file5(self, asus_nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.control_file.print is asus_nuc_wmi_print) # pylint: disable=no-member

        # Branch 5: Test that debug logging prints written bytes

        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        expected_byte_string = '0d 0e 0a 0d 00' + (' 00' * 252)

        write_control_file(byte_list, control_file=self.control_file.name, debug=True)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(770).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        asus_nuc_wmi_print.assert_called_with(
            'asus_nuc_wmi write: ',
            expected_byte_string,
            file=sys.stderr
        )
