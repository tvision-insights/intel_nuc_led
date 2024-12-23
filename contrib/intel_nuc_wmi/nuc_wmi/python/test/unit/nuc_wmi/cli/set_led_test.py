"""
The `test.unit.nuc_wmi.cli.set_led_test` module provides unit tests for the functions in
`nuc_wmi.cli.set_led`.

Classes:
    TestCliSetLed: A unit test class for the functions in `nuc_wmi.cli.set_led`.
"""

import json
import unittest

from mock import patch

from nuc_wmi import LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_BLINK_FREQUENCY, LED_TYPE, NucWmiError
from nuc_wmi.cli.set_led import set_led_cli

import nuc_wmi


class TestCliSetLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.set_led`

    Methods:
        setUp: Unit test initialization.
        test_set_led_cli: Tests that it returns the proper JSON response and exit code for
                          valid cli args, tests that it captures raised errors and returns
                          the proper JSON error response and exit code, tests that invalid
                          LED color raises appropriate error.
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
                        'set_led': None
                    },
                    'recover': {
                        'function_oob_return_value': {
                            'set_led': False
                        }
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.set_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led.print')
    @patch('nuc_wmi.cli.set_led.set_led')
    @patch('nuc_wmi.cli.set_led.sys.exit')
    def test_set_led_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led.set_led is nuc_wmi_set_led)
        self.assertTrue(nuc_wmi.cli.set_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that set_led_cli returns the proper JSON response and exit
        #           code for valid cli args
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec

        # Set S0 Ring LED to brightness of 47%, frequency of Always on, and color of Cyan
        returned_set_led_cli = set_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2],
                LED_BRIGHTNESS['legacy'][47],
                LED_BLINK_FREQUENCY['legacy'][4],
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']][1]
            ]
        )

        nuc_wmi_set_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            str(LED_BRIGHTNESS['legacy'].index('47')),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['legacy'][2],
                    'brightness': str(LED_BRIGHTNESS['legacy'][47]),
                    'frequency': LED_BLINK_FREQUENCY['legacy'][4],
                    'color': LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']][1]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_set_led_cli, None)


    @patch('nuc_wmi.cli.set_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led.print')
    @patch('nuc_wmi.cli.set_led.set_led')
    @patch('nuc_wmi.cli.set_led.sys.exit')
    def test_set_led_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led.set_led is nuc_wmi_set_led)
        self.assertTrue(nuc_wmi.cli.set_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that set_led_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_set_led.side_effect = NucWmiError('Error (Function not supported)')

        returned_set_led_cli = set_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2],
                LED_BRIGHTNESS['legacy'][47],
                LED_BLINK_FREQUENCY['legacy'][4],
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']][1]
            ]
        )

        nuc_wmi_set_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            str(LED_BRIGHTNESS['legacy'].index('47')),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_cli, None)


    @patch('nuc_wmi.cli.set_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.set_led.print')
    @patch('nuc_wmi.cli.set_led.set_led')
    @patch('nuc_wmi.cli.set_led.sys.exit')
    def test_set_led_cli3(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_set_led,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `set_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.set_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.set_led.set_led is nuc_wmi_set_led)
        self.assertTrue(nuc_wmi.cli.set_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 3: Tests that invalid LED color raises appropriate error.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec

        returned_set_led_cli = set_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][1],
                LED_BRIGHTNESS['legacy'][47],
                LED_BLINK_FREQUENCY['legacy'][4],
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']][1]
            ]
        )

        nuc_wmi_set_led.assert_not_called()
        nuc_wmi_print.assert_called_with('{"error": "Invalid color for the specified legacy LED"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_cli, None)
