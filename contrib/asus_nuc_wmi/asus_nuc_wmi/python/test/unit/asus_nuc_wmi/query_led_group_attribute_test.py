"""
The `test.unit.asus_nuc_wmi.query_led_group_attribute_test` module provides unit tests for the functions in
`asus_nuc_wmi.query_led_group_attribute`.

Classes:
    TestQueryLedGroupAttribute: A unit test class for the functions in `asus_nuc_wmi.query_led_group_attribute`.
"""

import unittest

from mock import patch

from asus_nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, NucWmiError
from asus_nuc_wmi.query_led_group_attribute import FUNCTION_NUMBER, METHOD_ID, query_led_group_attribute

import asus_nuc_wmi


class TestQueryLedGroupAttribute(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.query_led_group_attribute`

    Methods:
        setUp: Unit test initialization.
        test_query_led_group_attribute: Tests that it sends the expected byte list to the control file, tests that the
                                        returned control file response is properly processed, tests that it raises an
                                        exception when the control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.query_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.query_led_group_attribute.write_control_file')
    def test_query_led_group_attribute(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `query_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.query_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.query_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 1: Test that query_led_group_attribute sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        expected_query_led_group_attribute = tuple([
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active'),
            LED_COLOR.index('Red'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100'),
            LED_COLOR.index('Amber'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100')
        ])

        expected_write_byte_list = [0x00] * 3

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('query_led_group_attribute')
        expected_write_byte_list[2] = 0x00

        #expected_write_byte_list[7] = 0x00
        # expected_write_byte_list[8] = 0x01
        # expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator')
        # expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
        #     'Normally OFF, ON when active'
        # )
        # expected_write_byte_list[30] = LED_COLOR.index('Red')
        # expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        # expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        # expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        # expected_write_byte_list[37] = LED_COLOR.index('Amber')
        # expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        # expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        # expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        read_byte_list[0] = 0x00
        read_byte_list[27] = LED_INDICATOR_OPTION.index('Software Indicator')
        read_byte_list[28] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active')
        read_byte_list[29] = LED_COLOR.index('Red')
        read_byte_list[30] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        read_byte_list[31] = LED_BLINK_FREQUENCY.index('1.0Hz')
        read_byte_list[32] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        read_byte_list[36] = LED_COLOR.index('Amber')
        read_byte_list[37] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        read_byte_list[38] = LED_BLINK_FREQUENCY.index('1.0Hz')
        read_byte_list[39] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        returned_query_led_group_attribute = query_led_group_attribute(
            control_file=None,
            debug=False
        )

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_led_group_attribute, tuple(expected_query_led_group_attribute))


    @patch('asus_nuc_wmi.query_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.query_led_group_attribute.write_control_file')
    def test_query_led_group_attribute2(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `query_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.query_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.query_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 2: Test that query_led_group_attribute raises an exception when the control file returns an
        #           error code.

        expected_write_byte_list = [0x00] * 3

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('query_led_group_attribute')
        expected_write_byte_list[2] = 0x00
        # expected_write_byte_list[7] = 0x00
        # expected_write_byte_list[8] = 0x01
        # # Incorrect led indicator option
        # expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator') + 1
        # expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
        #     'Normally OFF, ON when active'
        # )
        # expected_write_byte_list[30] = LED_COLOR.index('Red')
        # expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        # expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        # expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        # expected_write_byte_list[37] = LED_COLOR.index('Amber')
        # expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        # expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        # expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        read_byte_list[0] = 0xE2 # Return undefined device

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            query_led_group_attribute(
                control_file=None,
                debug=False
            ) # Set incorrect led indicator option

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Undefined device)')
