"""
The `test.unit.asus_nuc_wmi.cli.update_led_group_attribute_test` module provides unit tests for the functions in
`asus_nuc_wmi.cli.update_led_group_attribute`.

Classes:
    TestCliUpdateLedGroupAttribute: A unit test class for the functions in
                                    `asus_nuc_wmi.cli.update_led_group_attribute`.
"""

import json
import unittest

from mock import patch

from asus_nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, NucWmiError
from asus_nuc_wmi.cli.update_led_group_attribute import update_led_group_attribute_cli

import asus_nuc_wmi


class TestCliUpdateLedGroupAttribute(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.cli.update_led_group_attribute`

    Methods:
        setUp: Unit test initialization.
        test_update_led_group_attribute_cli: Tests that it returns the proper JSON response and exit code for
                                             valid cli args, tests that it captures raised errors and returns
                                             the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.cli.update_led_group_attribute.update_led_group_attribute')
    @patch('asus_nuc_wmi.cli.update_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.update_led_group_attribute.sys.exit')
    def test_update_led_group_attribute_cli( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_update_led_group_attribute
    ):
        """
        Tests that `update_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.update_led_group_attribute.update_led_group_attribute is \
            asus_nuc_wmi_update_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.update_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.update_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 1: Test that update_led_group_attribute_cli returns the proper JSON response and exit
        #           code for valid cli args

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_update_led_group_attribute = tuple([
            led_indicator_option_index,
            hdd_activity_behavior_index,
            led_color_index,
            led_blink_behavior_index,
            led_blink_frequency_index,
            led_brightness,
            sleep_state_led_color_index,
            sleep_state_led_blink_behavior_index,
            sleep_state_led_blink_frequency_index,
            sleep_state_led_brightness
        ])

        asus_nuc_wmi_update_led_group_attribute.return_value = expected_update_led_group_attribute

        returned_update_led_group_attribute_cli = update_led_group_attribute_cli(
            [
                LED_INDICATOR_OPTION[led_indicator_option_index],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR[hdd_activity_behavior_index],
                LED_COLOR[led_color_index],
                LED_BLINK_BEHAVIOR_MULTI_COLOR[led_blink_behavior_index],
                LED_BLINK_FREQUENCY[led_blink_frequency_index],
                LED_BRIGHTNESS_MULTI_COLOR[led_brightness],
                LED_COLOR[sleep_state_led_color_index],
                LED_BLINK_BEHAVIOR_MULTI_COLOR[sleep_state_led_blink_behavior_index],
                LED_BLINK_FREQUENCY[sleep_state_led_blink_frequency_index],
                LED_BRIGHTNESS_MULTI_COLOR[sleep_state_led_brightness]
            ]
        )

        asus_nuc_wmi_update_led_group_attribute.assert_called_with(
            led_indicator_option_index,
            hdd_activity_behavior_index,
            led_color_index,
            led_blink_behavior_index,
            led_blink_frequency_index,
            led_brightness,
            sleep_state_led_color_index,
            sleep_state_led_blink_behavior_index,
            sleep_state_led_blink_frequency_index,
            sleep_state_led_brightness,
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(asus_nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': 'Power Button LED',
                    'indicator_option': LED_INDICATOR_OPTION[led_indicator_option_index],
                    'hdd_activity_behavior': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR[
                        hdd_activity_behavior_index
                    ],
                    'color': LED_COLOR[led_color_index],
                    'blinking_behavior': LED_BLINK_BEHAVIOR_MULTI_COLOR[led_blink_behavior_index],
                    'blinking_frequency': LED_BLINK_FREQUENCY[led_blink_frequency_index],
                    'brightness': LED_BRIGHTNESS_MULTI_COLOR[led_brightness],
                    'sleep_state_color': LED_COLOR[sleep_state_led_color_index],
                    'sleep_state_blinking_behavior': LED_BLINK_BEHAVIOR_MULTI_COLOR[
                        sleep_state_led_blink_behavior_index
                    ],
                    'sleep_state_blinking_frequency': LED_BLINK_FREQUENCY[
                        sleep_state_led_blink_frequency_index
                    ],
                    'sleep_state_brightness': LED_BRIGHTNESS_MULTI_COLOR[sleep_state_led_brightness]
                }
            }
        )

        self.assertEqual(returned_update_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.update_led_group_attribute.update_led_group_attribute')
    @patch('asus_nuc_wmi.cli.update_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.update_led_group_attribute.sys.exit')
    def test_update_led_group_attribute_cli2( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_update_led_group_attribute
    ):
        """
        Tests that `update_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.update_led_group_attribute.update_led_group_attribute is \
            asus_nuc_wmi_update_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.update_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.update_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 2: Test that update_led_group_attribute_cli captures raised errors and returns
        #           the proper JSON error response and exit code.

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        asus_nuc_wmi_update_led_group_attribute.side_effect = NucWmiError('Error (Function not supported)')

        returned_update_led_group_attribute_cli = update_led_group_attribute_cli(
            [
                LED_INDICATOR_OPTION[led_indicator_option_index],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR[hdd_activity_behavior_index],
                LED_COLOR[led_color_index],
                LED_BLINK_BEHAVIOR_MULTI_COLOR[led_blink_behavior_index],
                LED_BLINK_FREQUENCY[led_blink_frequency_index],
                LED_BRIGHTNESS_MULTI_COLOR[led_brightness],
                LED_COLOR[sleep_state_led_color_index],
                LED_BLINK_BEHAVIOR_MULTI_COLOR[sleep_state_led_blink_behavior_index],
                LED_BLINK_FREQUENCY[sleep_state_led_blink_frequency_index],
                LED_BRIGHTNESS_MULTI_COLOR[sleep_state_led_brightness]
            ]
        )

        asus_nuc_wmi_update_led_group_attribute.assert_called_with(
            led_indicator_option_index,
            hdd_activity_behavior_index,
            led_color_index,
            led_blink_behavior_index,
            led_blink_frequency_index,
            led_brightness,
            sleep_state_led_color_index,
            sleep_state_led_blink_behavior_index,
            sleep_state_led_blink_frequency_index,
            sleep_state_led_brightness,
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_update_led_group_attribute_cli, None)
