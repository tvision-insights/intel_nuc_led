"""
The `test.unit.nuc_wmi.cli.set_led_indicator_option_test` module provides unit tests for the functions in
`nuc_wmi.cli.set_led_indicator_option`.

Classes:
    TestCliSetLedIndicatorOption: A unit test class for the functions in `nuc_wmi.cli.set_led_indicator_option`.
"""

import json
import unittest

from mock import patch

from nuc_wmi import LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.cli.set_led_indicator_option import set_led_indicator_option_cli

import nuc_wmi


class TestCliSetLedIndicatorOption(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.set_led_indicator_option`

    Methods:
        setUp: Unit test initialization.
        test_set_led_indicator_option_cli: Tests that it returns the proper JSON response and exit code for
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
                        'set_led_indicator_option': None
                    },
                    'recover': {
                        'function_oob_return_value': {
                            'set_led_indicator_option': False
                        }
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led_indicator_option.print')
    @patch('nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option')
    @patch('nuc_wmi.cli.set_led_indicator_option.sys.exit')
    def test_set_led_indicator_option_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led_indicator_option,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_indicator_option_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option is \
                        nuc_wmi_set_led_indicator_option)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that set_led_indicator_option_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Set HDD LED indicator option to HDD Activity Indicator
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec

        returned_set_led_indicator_option_cli = set_led_indicator_option_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
            ]
        )

        nuc_wmi_set_led_indicator_option.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_set_led_indicator_option_cli, None)


    @patch('nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led_indicator_option.print')
    @patch('nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option')
    @patch('nuc_wmi.cli.set_led_indicator_option.sys.exit')
    def test_set_led_indicator_option_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led_indicator_option,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_indicator_option_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option is \
                        nuc_wmi_set_led_indicator_option)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that set_led_indicator_option_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_set_led_indicator_option.side_effect = NucWmiError('Error (Function not supported)')

        returned_set_led_indicator_option_cli = set_led_indicator_option_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
            ]
        )

        nuc_wmi_set_led_indicator_option.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_indicator_option_cli, None)


    @patch('nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led_indicator_option.print')
    @patch('nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option')
    @patch('nuc_wmi.cli.set_led_indicator_option.sys.exit')
    def test_set_led_indicator_option_cli3(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led_indicator_option,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_indicator_option_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.set_led_indicator_option is \
                        nuc_wmi_set_led_indicator_option)
        self.assertTrue(nuc_wmi.cli.set_led_indicator_option.sys.exit is nuc_wmi_sys_exit)

        # Branch 3: Test that set_led_indicator_option_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Set HDD LED indicator option to Software Indicator
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec

        returned_set_led_indicator_option_cli = set_led_indicator_option_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[4]
            ]
        )

        nuc_wmi_set_led_indicator_option.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[4]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_set_led_indicator_option_cli, None)
