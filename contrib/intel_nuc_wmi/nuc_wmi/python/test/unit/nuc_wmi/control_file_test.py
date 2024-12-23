"""
The `test.unit.nuc_wmi.control_file_test` module provides unit tests for the functions in
`nuc_wmi.control_file`.

Classes:
    TestControlFile: A unit test class for the functions in `nuc_wmi.control_file`.
"""

import os
import sys
import unittest

from tempfile import NamedTemporaryFile

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.control_file import read_control_file, write_control_file

import nuc_wmi


class TestControlFile(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.control_file`

    Methods:
        setUp: Unit test initialization.
        tearDown: Unit test cleanup.
        test_read_control_file: Tests that `read_control_file` raises the expected exception when nuc_wmi.CONTROL_FILE
                                doesnt exist, tests that exception is raised if less than 4 bytes are returned, tests
                                that overriding control_file with existing file works, tests that overriding
                                control_file with non existing file raises exception, and tests that exception is raised
                                if NUC WMI provides a hex byte value outside of the 0-255 range.
        test_write_control_file: Tests that `write_control_file` raises the expected exception when nuc_wmi.CONTROL_FILE
                                 doesnt exist, tests that number of bytes written to control file are padded to 5 bytes
                                 if less than 5 bytes are passed in, tests that both integer and string bytes are
                                 accepted, tests that byte strings outside of 0-255 value raise an exception, tests that
                                 overriding control_file with different file works.
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


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that `read_control_file` raises exception when `nuc_wmi.CONTROL_FILE` doesnt exist
        #           Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)):
            read_control_file(
                control_file=None
            )

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file2(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that `read_control_file` raise exception if less than 4 bytes are read
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write("00 00 00\n\x00".encode('utf8'))

        with self.assertRaises(NucWmiError) as byte_list_len_err:
            read_control_file(control_file=self.control_file.name, debug=False)

        self.assertEqual(str(byte_list_len_err.exception),
                         'Intel NUC WMI control file did not return an expected 4 bytes')

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file3(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Test that overriding control file with existing file works
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write("0D 0E 0A 0D\n\x00".encode('utf8'))

        byte_list = (0x0D, 0x0E, 0x0A, 0x0D)

        self.assertEqual(
            read_control_file(control_file=self.control_file.name, debug=False),
            byte_list
        )

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file4(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 4: Test that overriding control file with non existing file raises exception
        with NamedTemporaryFile() as temp_file:
            non_existent_file = temp_file

        with self.assertRaises((IOError, OSError)):
            read_control_file(control_file=non_existent_file.name, debug=False)

        nuc_wmi_print.assert_not_called()


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file5(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 5: Test that exception is raised if NUC WMI returns a hex byte outside 0-255 range
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write("FFF 0E 0A 0D\n\x00".encode('utf8'))

        with self.assertRaises(NucWmiError) as err:
            read_control_file(control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception), 'Intel NUC WMI returned hex byte outside of 0-255 range')

        nuc_wmi_print.assert_not_called()


    @patch('nuc_wmi.control_file.print')
    def test_read_control_file6(self, nuc_wmi_print):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 6: Test that debug logging prints read bytes
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.write("0D 0E 0A 0D\n\x00".encode('utf8'))

        byte_list = (0x0D, 0x0E, 0x0A, 0x0D)

        self.assertEqual(
            read_control_file(control_file=self.control_file.name, debug=True),
            byte_list
        )

        nuc_wmi_print.assert_called_with(
            'nuc_wmi read: ',
            '0D 0E 0A 0D',
            file=sys.stderr
        )


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Tests that `write_control_file` raises the expected exception when `nuc_wmi.CONTROL_FILE` doesnt
        #           exist. Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)):
            read_control_file(control_file=None, debug=False)

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file2(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Tests that the number of bytes written to the control file are padded to 5 bytes, and that
        #           integer byte list is properly written to the control file.
        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        expected_byte_string = '0d 0e 0a 0d 00'

        write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(14).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file3(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Tests that an string byte list is properly written to the control file
        byte_list = [str(0x0D), str(0x0E), str(0x0A), str(0x0D)]
        expected_byte_string = '0d 0e 0a 0d 00'

        write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(14).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file4(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 4: Test that byte strings outside of the 0-255 value raise an exception
        byte_list = [0x03, 0xFFF]

        with self.assertRaises(NucWmiError) as err:
            write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception), 'Error (Intel NUC LED byte values must be 0-255)')

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file5(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 5: Test that debug logging prints written bytess

        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        expected_byte_string = '0d 0e 0a 0d 00'

        write_control_file(byte_list, control_file=self.control_file.name, debug=True)

        with open(self.control_file.name, 'rb', buffering=0) as fin:
            written_byte_string = fin.read(14).decode('utf8')

        self.assertEqual(expected_byte_string, written_byte_string)

        nuc_wmi_print.assert_called_with(
            'nuc_wmi write: ',
            expected_byte_string,
            file=sys.stderr
        )


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file6(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 6: Test that method id 32bit string outside of the 0-4294967295 value raise an exception
        byte_list = [0x100000000]

        with self.assertRaises(NucWmiError) as err:
            write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception), 'Error (Intel NUC LED method id 32bit value must be 0-4294967295)')

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()


    @patch('nuc_wmi.control_file.print')
    def test_write_control_file7(self, nuc_wmi_print):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.control_file.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 7: Test that no bytes passed in raises an exception
        byte_list = []

        with self.assertRaises(NucWmiError) as err:
            write_control_file(byte_list, control_file=self.control_file.name, debug=False)

        self.assertEqual(str(err.exception),
                         'Error (Intel NUC LED byte values must at least provide the first 32bit method id)')

        nuc_wmi_print.assert_not_called()

        # Reset
        with open(self.control_file.name, 'wb', buffering=0) as fout:
            fout.truncate()
