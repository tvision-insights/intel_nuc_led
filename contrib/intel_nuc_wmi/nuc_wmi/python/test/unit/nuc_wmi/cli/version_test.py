"""
The `test.unit.nuc_wmi.cli.version_test` module provides unit tests for the functions in
`nuc_wmi.cli.version`.

Classes:
    TestCliVersion: A unit test class for the functions in `nuc_wmi.cli.version`.
"""

import json
import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.cli.version import wmi_interface_spec_compliance_version_cli

import nuc_wmi


class TestCliVersion(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.version`

    Methods:
        setUp: Unit test initialization.
        test_wmi_interface_spec_compliance_version_cli: Tests that it returns the proper JSON response and exit code for
                                                        valid cli args, tests that it captures raised errors and returns
                                                        the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name

        self.nuc_wmi_spec = {
            'TEST_DEVICE': {
                'nuc_wmi_spec': {
                    'function_return_type': {
                        'wmi_interface_spec_compliance_version': 'int'
                    },
                    'recover':{
                        'function_oob_return_value': {
                            'wmi_interface_spec_compliance_version': False
                        }
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.version.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.version.print')
    @patch('nuc_wmi.cli.version.sys.exit')
    @patch('nuc_wmi.cli.version.wmi_interface_spec_compliance_version')
    def test_wmi_interface_spec_compliance_version_cli(
            self,
            nuc_wmi_cli_wmi_interface_spec_compliance_version,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `wmi_interface_spec_compliance_version_cli` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.cli.version.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.version.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.version.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.version.wmi_interface_spec_compliance_version is \
                        nuc_wmi_cli_wmi_interface_spec_compliance_version)

        # Branch 1: Test that wmi_interface_spec_compliance_version_cli returns the proper JSON response and exit
        #           code for valid cli args
        nuc_wmi_spec_alias = 'TEST_DEVICE'
        wmi_interface_spec_compliance_version = (0x01, 0x36)

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_cli_wmi_interface_spec_compliance_version.return_value = wmi_interface_spec_compliance_version

        returned_wmi_interface_spec_compliance_version_cli = wmi_interface_spec_compliance_version_cli(
            [nuc_wmi_spec_alias]
        )

        nuc_wmi_cli_wmi_interface_spec_compliance_version.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias,
                'version': {
                    'semver': '1.54',
                    'type': 'wmi_interface_spec_compliance'
                }
            }
        )

        self.assertEqual(returned_wmi_interface_spec_compliance_version_cli, None)


    @patch('nuc_wmi.cli.version.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.version.print')
    @patch('nuc_wmi.cli.version.sys.exit')
    @patch('nuc_wmi.cli.version.wmi_interface_spec_compliance_version')
    def test_wmi_interface_spec_compliance_version_cli2(
            self,
            nuc_wmi_cli_wmi_interface_spec_compliance_version,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `wmi_interface_spec_compliance_version_cli` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.cli.version.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.version.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.version.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.version.wmi_interface_spec_compliance_version is \
                        nuc_wmi_cli_wmi_interface_spec_compliance_version)

        # Branch 2: Test that wmi_interface_spec_compliance_version_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_cli_wmi_interface_spec_compliance_version.side_effect = NucWmiError('Error (Function not supported)')

        returned_wmi_interface_spec_compliance_version_cli = wmi_interface_spec_compliance_version_cli(
            [nuc_wmi_spec_alias]
        )

        nuc_wmi_cli_wmi_interface_spec_compliance_version.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_wmi_interface_spec_compliance_version_cli, None)
