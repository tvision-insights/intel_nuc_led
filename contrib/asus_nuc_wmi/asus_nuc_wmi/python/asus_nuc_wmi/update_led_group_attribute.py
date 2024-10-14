"""
`asus_nuc_wmi.update_led_group_attribute` provides an interface to the WMI update led group attribute function.
"""

from asus_nuc_wmi import NucWmiError, RETURN_ERROR
from asus_nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x65

FUNCTION_NUMBER = [
    None,
    'update_led_group_attribute'
]


def update_led_group_attribute(
        led_indicator_option,
        hdd_activity_behavior,
        led_color,
        led_blink_behavior,
        led_blink_frequency,
        led_brightness,
        sleep_state_led_color,
        sleep_state_led_blink_behavior,
        sleep_state_led_blink_frequency,
        sleep_state_led_brightness,
        control_file=None,
        debug=False
):
    """
    Update all LED group attributes.

    Args:
      control_file: Sets the control file to use if provided, otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the ASUS NUC LED control file to stderr.
      hdd_activity_behavior: Index of `asus_nuc_wmi.CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR` to set Power Button
                             LED HDD activity indicator behavior.
      led_blink_behavior: Index of `asus_nuc_wmi.LED_BLINK_BEHAVIOR_MULTI_COLOR` to set Power Button LED blink behavior.
      led_blink_frequency: Index of `asus_nuc_wmi.LED_BLINK_FREQUENCY` to set Power Button LED blink frequency.
      led_brightness: Index of `asus_nuc_wmi.LED_BRIGHTNESS_MULTI_COLOR` to set Power Button LED brightness.
      led_color: Index of `asus_nuc_wmi.LED_COLOR' to set Power Button LED color.
      led_indicator_option: Index of `asus_nuc_wmi.LED_INDICATOR_OPTION` to set Power Button LED indicitator option.
      sleep_state_led_color: Index of `asus_nuc_wmi.LED_COLOR' to set Power Button LED sleep state color.
      sleep_state_led_blink_behavior: Index of `asus_nuc_wmi.LED_BLINK_BEHAVIOR_MULTI_COLOR` to set Power Button LED
                                      sleep state blink behavior.
      sleep_state_led_blink_frequency: Index of `asus_nuc_wmi.LED_BLINK_FREQUENCY` to set Power Button LED sleep state
                                       blink frequency.
      sleep_state_led_brightness: Index of `asus_nuc_wmi.LED_BRIGHTNESS_MULTI_COLOR` to set Power Button LED sleep state
                                  brightness.
    Exceptions:
      Raises `asus_nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    """

    update_led_group_attribute_byte_list = [0x00] * 257

    update_led_group_attribute_byte_list[0] = METHOD_ID
    update_led_group_attribute_byte_list[1] = FUNCTION_NUMBER.index('update_led_group_attribute')
    update_led_group_attribute_byte_list[7] = 0x00
    update_led_group_attribute_byte_list[8] = 0x01
    update_led_group_attribute_byte_list[28] = led_indicator_option
    update_led_group_attribute_byte_list[29] = hdd_activity_behavior
    update_led_group_attribute_byte_list[30] = led_color
    update_led_group_attribute_byte_list[31] = led_blink_behavior
    update_led_group_attribute_byte_list[32] = led_blink_frequency
    update_led_group_attribute_byte_list[33] = led_brightness
    update_led_group_attribute_byte_list[37] = sleep_state_led_color
    update_led_group_attribute_byte_list[38] = sleep_state_led_blink_behavior
    update_led_group_attribute_byte_list[39] = sleep_state_led_blink_frequency
    update_led_group_attribute_byte_list[40] = sleep_state_led_brightness

    write_control_file(update_led_group_attribute_byte_list, control_file=control_file, debug=debug)

    update_led_group_attribute_result = read_control_file(control_file=control_file, debug=debug)

    error_code = update_led_group_attribute_result[0]

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown ASUS NUC WMI error code)'))
