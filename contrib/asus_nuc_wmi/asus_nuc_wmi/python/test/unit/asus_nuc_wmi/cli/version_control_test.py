"""
The `test.unit.asus_nuc_wmi.cli.version_control_test` module provides unit tests for the functions in
`asus_nuc_wmi.cli.version_control`.

Classes:
    TestCliVersionControl: A unit test class for the functions in `asus_nuc_wmi.cli.version_control`.
"""

import json
import unittest

from mock import patch

from asus_nuc_wmi import NucWmiError
from asus_nuc_wmi.cli.version_control import version_control_cli

import asus_nuc_wmi


class TestCliVersionControl(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.cli.version_control`

    Methods:
        setUp: Unit test initialization.
        test_version_control_cli: Tests that it returns the proper JSON response and exit code for
                                  valid cli args, tests that it captures raised errors and returns
                                  the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.cli.version_control.print')
    @patch('asus_nuc_wmi.cli.version_control.sys.exit')
    @patch('asus_nuc_wmi.cli.version_control.version_control')
    def test_version_control_cli(
            self,
            asus_nuc_wmi_version_control,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print
    ):
        """
        Tests that `version_control_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.cli.version_control.print is asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.version_control.sys.exit is asus_nuc_wmi_sys_exit)
        self.assertTrue(asus_nuc_wmi.cli.version_control.version_control is asus_nuc_wmi_version_control)

        # Branch 1: Test that version_control_cli returns the proper JSON response and exit code for valid cli args
        wmi_version = (0x01, 0x36)

        asus_nuc_wmi_version_control.return_value = wmi_version

        returned_version_control_cli = version_control_cli([])

        asus_nuc_wmi_version_control.assert_called_with(
            control_file=None,
            debug=False,
            metadata=None
        )
        asus_nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(asus_nuc_wmi_print.call_args.args[0]),
            {
                'version_control': {
                    'semver': '1.54',
                    'type': 'version'
                }
            }
        )

        self.assertEqual(returned_version_control_cli, None)


    @patch('asus_nuc_wmi.cli.version_control.print')
    @patch('asus_nuc_wmi.cli.version_control.sys.exit')
    @patch('asus_nuc_wmi.cli.version_control.version_control')
    def test_version_control_cli2(
            self,
            asus_nuc_wmi_version_control,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print
    ):
        """
        Tests that `version_control_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.cli.version_control.print is asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.version_control.sys.exit is asus_nuc_wmi_sys_exit)
        self.assertTrue(asus_nuc_wmi.cli.version_control.version_control is asus_nuc_wmi_version_control)

        # Branch 2: Test that version_control_cli captures raised errors and returns the proper JSON error response and
        #           exit code.
        asus_nuc_wmi_version_control.side_effect = NucWmiError('Error (Function not supported)')

        returned_version_control_cli = version_control_cli([])

        asus_nuc_wmi_version_control.assert_called_with(
            control_file=None,
            debug=False,
            metadata=None
        )
        asus_nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_version_control_cli, None)
