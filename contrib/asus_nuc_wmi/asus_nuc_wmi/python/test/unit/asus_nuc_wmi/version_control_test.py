"""
The `test.unit.asus_nuc_wmi.version_control_test` module provides unit tests for the functions in
`asus_nuc_wmi.version_control`.

Classes:
    TestVersionControl: A unit test class for the functions in `asus_nuc_wmi.version_control`.
"""

import unittest

from mock import patch

from asus_nuc_wmi import NucWmiError
from asus_nuc_wmi.version_control import METHOD_ID, VERSION_TYPE, version_control

import asus_nuc_wmi


class TestVersionControl(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.version_control`

    Methods:
        setUp: Unit test initialization.
        test_version_control: Tests that it sends the expected byte list to the control file,
                              tests that the returned control file response is properly processed,
                              tests that it raises an exception when the control file returns an
                              error code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.version_control.read_control_file')
    @patch('asus_nuc_wmi.version_control.write_control_file')
    def test_version_control(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `version_control` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.version_control.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.version_control.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 1: Test that version_control send the expected byte string to the control file
        #           and that the returned control file response is properly processed.
        expected_wmi_version = (0x01, 0x36)
        expected_write_byte_list = [METHOD_ID, VERSION_TYPE.index('version_control')]
        read_byte_list = [0x00, 0x36, 0x01, 0x00]

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        returned_wmi_version = version_control(
            control_file=None,
            debug=False,
            metadata=None
        )

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_wmi_version, expected_wmi_version)


    @patch('asus_nuc_wmi.version_control.read_control_file')
    @patch('asus_nuc_wmi.version_control.write_control_file')
    def test_version_control2(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `version_control` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.version_control.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.version_control.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 2: Test that version_control raises an exception when the control file returns an
        #           error code.
        expected_write_byte_list = [METHOD_ID, VERSION_TYPE.index('version_control')]
        read_byte_list = [0xE1, 0x00, 0x00, 0x00] # Return function not supported

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            version_control(
                control_file=None,
                debug=False,
                metadata=None
            )

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Function not supported)')
