"""
`asus_nuc_wmi.query_led_group_attribute` provides an interface to the WMI query led group attribute function.
"""

from asus_nuc_wmi import NucWmiError, RETURN_ERROR
from asus_nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x101

FUNCTION_NUMBER = [
    None,
    'query_led_group_attribute'
]


def query_led_group_attribute(control_file=None, debug=False, metadata=None): # pylint: disable=too-many-locals
    """
    List all LED group attributes.

    Args:
      control_file: Sets the control file to use if provided, otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the ASUS NUC LED control file to stderr.
      metadata: Metadata that may be required to change functional behavior.
    Exceptions:
      Raises `asus_nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      Tuple of LED group attributes indexes for `asus_nuc_wmi.LED_INDICATOR_OPTION`,
      `asus_nuc_wmi.CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR`, `asus_nuc_wmi.LED_COLOR',
      `asus_nuc_wmi.LED_BLINK_BEHAVIOR_MULTI_COLOR`, `asus_nuc_wmi.LED_BLINK_FREQUENCY`,
      `asus_nuc_wmi.LED_BRIGHTNESS_MULTI_COLOR`, `asus_nuc_wmi.LED_COLOR',
      `asus_nuc_wmi.LED_BLINK_BEHAVIOR_MULTI_COLOR`, `asus_nuc_wmi.LED_BLINK_FREQUENCY`,
      `asus_nuc_wmi.LED_BRIGHTNESS_MULTI_COLOR` .
    """

    query_led_group_attribute_byte_list = [METHOD_ID, FUNCTION_NUMBER.index('query_led_group_attribute'), 0x00]

    write_control_file(query_led_group_attribute_byte_list, control_file=control_file, debug=debug)

    query_led_group_attribute_result = read_control_file(control_file=control_file, debug=debug)

    error_code = query_led_group_attribute_result[0]
    led_indicator_option = query_led_group_attribute_result[27]
    hdd_activity_behavior = query_led_group_attribute_result[28]
    led_color = query_led_group_attribute_result[29]
    led_blink_behavior = query_led_group_attribute_result[30]
    led_blink_frequency = query_led_group_attribute_result[31]
    led_brightness = query_led_group_attribute_result[32]
    sleep_state_led_color = query_led_group_attribute_result[36]
    sleep_state_led_blink_behavior = query_led_group_attribute_result[37]
    sleep_state_led_blink_frequency = query_led_group_attribute_result[38]
    sleep_state_led_brightness = query_led_group_attribute_result[39]

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown ASUS NUC WMI error code)'))

    if metadata and \
       metadata.get('nuc_wmi_spec', {}).get('function_return_type', {}).get(
           'query_led_group_attribute', ''
       ) == 'raw_bytes':
        return query_led_group_attribute_result

    return (led_indicator_option,
            hdd_activity_behavior,
            led_color,
            led_blink_behavior,
            led_blink_frequency,
            led_brightness,
            sleep_state_led_color,
            sleep_state_led_blink_behavior,
            sleep_state_led_blink_frequency,
            sleep_state_led_brightness)
