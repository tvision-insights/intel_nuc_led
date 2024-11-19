"""
The `test.unit.asus_nuc_wmi.cli.query_led_group_attribute_test` module provides unit tests for the functions in
`asus_nuc_wmi.cli.query_led_group_attribute`.

Classes:
    TestCliQueryLedGroupAttribute: A unit test class for the functions in `asus_nuc_wmi.cli.query_led_group_attribute`.
"""

import json
import unittest

from mock import patch

from asus_nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, NucWmiError
from asus_nuc_wmi.cli.query_led_group_attribute import query_led_group_attribute_cli
from asus_nuc_wmi.utils import defined_indexes

import asus_nuc_wmi


class TestCliQueryLedGroupAttribute(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.cli.query_led_group_attribute`

    Methods:
        setUp: Unit test initialization.
        test_query_led_group_attribute_cli: Tests that it returns the proper JSON response and exit code for
                                            valid cli args, tests that it captures raised errors and returns
                                            the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 1: Test that query_led_group_attribute_cli returns the proper JSON response and exit
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

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
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

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli2( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 2: Test that query_led_group_attribute_cli captures raised errors and returns
        #           the proper JSON error response and exit code.

        asus_nuc_wmi_query_led_group_attribute.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli3( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 3: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED led indicator option by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        led_indicator_option_range = defined_indexes(LED_INDICATOR_OPTION)

        led_indicator_option_index = len(LED_INDICATOR_OPTION) # Invalid LED Indicator Option
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED " + \
        "indicator option of %i, expected one of %s)" % (led_indicator_option_index, str(led_indicator_option_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli4( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 4: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED HDD activity behavior by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        hdd_activity_behavior_range = defined_indexes(CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = len(CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR) # Invalid HDD activity behavior
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED " + \
        "HDD activity behavior of %i, expected one of %s)" % (hdd_activity_behavior_index,
                                                              str(hdd_activity_behavior_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli5( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 5: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED LED color by WMI, captures raised errors and returns the proper JSON error response and exit code.

        led_color_range = defined_indexes(LED_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = len(LED_COLOR) # Invalid LED color
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED" + \
        " color of %i, expected one of %s)" % (led_color_index, str(led_color_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli6( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 6: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED led blink behavior by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        led_blink_behavior_range = defined_indexes(LED_BLINK_BEHAVIOR_MULTI_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = len(LED_BLINK_BEHAVIOR_MULTI_COLOR) # Invalid LED blink behavior
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button " + \
        "LED blinking behavior of %i, expected one of %s)" % (led_blink_behavior_index, str(led_blink_behavior_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli7( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 7: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED led blink frequency by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        led_blink_frequency_range = defined_indexes(LED_BLINK_FREQUENCY)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = len(LED_BLINK_FREQUENCY) # Invalid LED blink frequency
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button " + \
        "LED blinking frequency of %i, expected one of %s)" % (led_blink_frequency_index,
                                                               str(led_blink_frequency_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli8( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 8: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED led brightness by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        led_brightness_range = defined_indexes(LED_BRIGHTNESS_MULTI_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = len(LED_BRIGHTNESS_MULTI_COLOR) # Invalid LED brightness
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED " + \
            "brightness of %i, expected one of %s)" % (led_brightness, str(led_brightness_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli9( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 9: Test that query_led_group_attribute_cli raises exception with error message for invalid Power Button
        # LED sleep state led color by WMI, captures raised errors and returns the proper JSON error response and exit
        # code.

        led_color_range = defined_indexes(LED_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = len(LED_COLOR) # Invalid LED sleep state color
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED" + \
        " sleep state color of %i, expected one of %s)" % (sleep_state_led_color_index, str(led_color_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli10( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 10: Test that query_led_group_attribute_cli raises exception with error message for invalid Power
        # Button LED sleep state LED blink behavior by WMI, captures raised errors and returns the proper JSON error
        # response and exit code.

        led_blink_behavior_range = defined_indexes(LED_BLINK_BEHAVIOR_MULTI_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = len(LED_BLINK_BEHAVIOR_MULTI_COLOR) # Invalid LED sleep state blink
                                                                                   # behavior
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button " + \
        "LED sleep state blinking behavior of %i, expected one of %s)" % (sleep_state_led_blink_behavior_index,
                                                                          str(led_blink_behavior_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli11( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 11: Test that query_led_group_attribute_cli raises exception with error message for invalid Power
        # Button LED sleep state LED blink frequency by WMI, captures raised errors and returns the proper JSON error
        # response and exit code.

        led_blink_frequency_range = defined_indexes(LED_BLINK_FREQUENCY)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = len(LED_BLINK_FREQUENCY)
        sleep_state_led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED" + \
        " sleep state blinking frequency of %i, expected one of %s)" % (sleep_state_led_blink_frequency_index,
                                                                        str(led_blink_frequency_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)


    @patch('asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.print')
    @patch('asus_nuc_wmi.cli.query_led_group_attribute.sys.exit')
    def test_query_led_group_attribute_cli12( # pylint: disable=too-many-locals
            self,
            asus_nuc_wmi_sys_exit,
            asus_nuc_wmi_print,
            asus_nuc_wmi_query_led_group_attribute
    ):
        """
        Tests that `query_led_group_attribute_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(
            asus_nuc_wmi.cli.query_led_group_attribute.query_led_group_attribute is \
            asus_nuc_wmi_query_led_group_attribute
        )
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.print is \
                        asus_nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(asus_nuc_wmi.cli.query_led_group_attribute.sys.exit is asus_nuc_wmi_sys_exit)

        # Branch 12: Test that query_led_group_attribute_cli raises exception with error message for invalid Power
        # Button LED sleep state LED brightness by WMI, captures raised errors and returns the proper JSON error
        # response and exit code.

        led_brightness_range = defined_indexes(LED_BRIGHTNESS_MULTI_COLOR)

        led_indicator_option_index = LED_INDICATOR_OPTION.index('Software Indicator')
        hdd_activity_behavior_index = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        led_color_index = LED_COLOR.index('Red')
        led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        led_brightness = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        sleep_state_led_color_index = LED_COLOR.index('Amber')
        sleep_state_led_blink_behavior_index = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        sleep_state_led_blink_frequency_index = LED_BLINK_FREQUENCY.index('1.0Hz')
        sleep_state_led_brightness = len(LED_BRIGHTNESS_MULTI_COLOR)

        expected_error = "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED" + \
        " sleep state brightness of %i, expected one of %s)" % (sleep_state_led_brightness, str(led_brightness_range))

        expected_query_led_group_attribute = tuple([
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

        asus_nuc_wmi_query_led_group_attribute.return_value = expected_query_led_group_attribute

        returned_query_led_group_attribute_cli = query_led_group_attribute_cli([])

        asus_nuc_wmi_query_led_group_attribute.assert_called_with(
            control_file=None,
            debug=False
        )
        asus_nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error
                }
            )
        )
        asus_nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_group_attribute_cli, None)
