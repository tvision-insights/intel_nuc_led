"""
The `test.unit.asus_nuc_wmi.update_led_group_attribute_test` module provides unit tests for the functions in
`asus_nuc_wmi.update_led_group_attribute`.

Classes:
    TestUpdateLedGroupAttribute: A unit test class for the functions in `asus_nuc_wmi.update_led_group_attribute`.
"""

import unittest

from mock import patch

from asus_nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, NucWmiError
from asus_nuc_wmi.update_led_group_attribute import FUNCTION_NUMBER, METHOD_ID, update_led_group_attribute

import asus_nuc_wmi


class TestUpdateLedGroupAttribute(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.update_led_group_attribute`

    Methods:
        setUp: Unit test initialization.
        test_update_led_group_attribute: Tests that it sends the expected byte list to the control file, tests that the
                                         returned control file response is properly processed, tests that it raises an
                                         exception when the control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('asus_nuc_wmi.update_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.update_led_group_attribute.write_control_file')
    def test_update_led_group_attribute(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `update_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 1: Test that update_led_group_attribute sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        expected_write_byte_list = [0x00] * 257

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('update_led_group_attribute')
        expected_write_byte_list[7] = 0x00
        expected_write_byte_list[8] = 0x01
        expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator')
        expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
            'Normally OFF, ON when active'
        )
        expected_write_byte_list[30] = LED_COLOR.index('Red')
        expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        expected_write_byte_list[37] = LED_COLOR.index('Amber')
        expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        returned_update_led_group_attribute = update_led_group_attribute(
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active'),
            LED_COLOR.index('Red'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100'),
            LED_COLOR.index('Amber'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100'),
            control_file=None,
            debug=False,
            metadata=None
        )

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_update_led_group_attribute, None)


    @patch('asus_nuc_wmi.update_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.update_led_group_attribute.write_control_file')
    def test_update_led_group_attribute2(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `update_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 2: Test that update_led_group_attribute raises an exception when the control file returns an
        #           error code.

        expected_write_byte_list = [0x00] * 257

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('update_led_group_attribute')
        expected_write_byte_list[7] = 0x00
        expected_write_byte_list[8] = 0x01
        # Incorrect led indicator option
        expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator') + 1
        expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
            'Normally OFF, ON when active'
        )
        expected_write_byte_list[30] = LED_COLOR.index('Red')
        expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        expected_write_byte_list[37] = LED_COLOR.index('Amber')
        expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        read_byte_list[0] = 0xE2 # Return undefined device

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            update_led_group_attribute(
                LED_INDICATOR_OPTION.index('Software Indicator') + 1, # Incorrect led indicator option
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active'),
                LED_COLOR.index('Red'),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
                LED_BLINK_FREQUENCY.index('1.0Hz'),
                LED_BRIGHTNESS_MULTI_COLOR.index('100'),
                LED_COLOR.index('Amber'),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
                LED_BLINK_FREQUENCY.index('1.0Hz'),
                LED_BRIGHTNESS_MULTI_COLOR.index('100'),
                control_file=None,
                debug=False,
                metadata=None
            ) # Set incorrect led indicator option

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Undefined device)')


    @patch('asus_nuc_wmi.update_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.update_led_group_attribute.write_control_file')
    def test_update_led_group_attribute3(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `update_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 3: Test that update_led_group_attribute sends the expected byte string to the control file
        #           and that the returned control file response is properly processed when provided a default query led
        #           group attribute byte list.

        expected_write_byte_list = [0x00] * 257

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('update_led_group_attribute')
        expected_write_byte_list[7] = 0x00
        expected_write_byte_list[8] = 0x01
        expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator')
        expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
            'Normally OFF, ON when active'
        )
        expected_write_byte_list[30] = LED_COLOR.index('Red')
        expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        expected_write_byte_list[37] = LED_COLOR.index('Amber')
        expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        returned_update_led_group_attribute = update_led_group_attribute(
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active'),
            LED_COLOR.index('Red'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100'),
            LED_COLOR.index('Amber'),
            LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
            LED_BLINK_FREQUENCY.index('1.0Hz'),
            LED_BRIGHTNESS_MULTI_COLOR.index('100'),
            control_file=None,
            debug=False,
            metadata={
                'query_led_group_attribute_raw_bytes': tuple([0x00] * 256)
            }
        )

        asus_nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_update_led_group_attribute, None)


    @patch('asus_nuc_wmi.update_led_group_attribute.read_control_file')
    @patch('asus_nuc_wmi.update_led_group_attribute.write_control_file')
    def test_update_led_group_attribute4(self, asus_nuc_wmi_write_control_file, asus_nuc_wmi_read_control_file):
        """
        Tests that `update_led_group_attribute` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.read_control_file is asus_nuc_wmi_read_control_file)
        self.assertTrue(asus_nuc_wmi.update_led_group_attribute.write_control_file is asus_nuc_wmi_write_control_file)

        # Branch 4: Test that update_led_group_attribute raises an exception when the provided default query led
        #           group attribute byte list is of invalid length.

        expected_write_byte_list = [0x00] * 257

        expected_write_byte_list[0] = METHOD_ID
        expected_write_byte_list[1] = FUNCTION_NUMBER.index('update_led_group_attribute')
        expected_write_byte_list[7] = 0x00
        expected_write_byte_list[8] = 0x01
        expected_write_byte_list[28] = LED_INDICATOR_OPTION.index('Software Indicator')
        expected_write_byte_list[29] = CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(
            'Normally OFF, ON when active'
        )
        expected_write_byte_list[30] = LED_COLOR.index('Red')
        expected_write_byte_list[31] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[32] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[33] = LED_BRIGHTNESS_MULTI_COLOR.index('100')
        expected_write_byte_list[37] = LED_COLOR.index('Amber')
        expected_write_byte_list[38] = LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid')
        expected_write_byte_list[39] = LED_BLINK_FREQUENCY.index('1.0Hz')
        expected_write_byte_list[40] = LED_BRIGHTNESS_MULTI_COLOR.index('100')

        read_byte_list = [0x00] * 256

        asus_nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            update_led_group_attribute(
                LED_INDICATOR_OPTION.index('Software Indicator'),
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index('Normally OFF, ON when active'),
                LED_COLOR.index('Red'),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
                LED_BLINK_FREQUENCY.index('1.0Hz'),
                LED_BRIGHTNESS_MULTI_COLOR.index('100'),
                LED_COLOR.index('Amber'),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index('Solid'),
                LED_BLINK_FREQUENCY.index('1.0Hz'),
                LED_BRIGHTNESS_MULTI_COLOR.index('100'),
                control_file=None,
                debug=False,
                metadata={
                    'query_led_group_attribute_raw_bytes': tuple([0x00] * 255)
                }
            )

        asus_nuc_wmi_write_control_file.assert_not_called()

        self.assertEqual(
            str(err.exception),
            'ASUS NUC WMI query_led_group_attribute_raw_bytes default must a list of 256 bytes'
        )
