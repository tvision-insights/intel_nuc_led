"""
`nuc_wmi.set_led_control_item` provides an interface to the WMI set control item function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import verify_nuc_wmi_function_spec

METHOD_ID = 0x06
SET_LED_CONTROL_ITEM_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': [None],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}


def set_led_control_item( # pylint: disable=too-many-arguments
        nuc_wmi_spec,
        led_type,
        led_indicator_option,
        control_item,
        control_item_value,
        control_file=None,
        debug=False,
        metadata=None # pylint: disable=unused-argument
):
    """
    Set the control item for the LED indicator option for the specified LED type,

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      control_item: The control item to set the value for.
      control_item_value: The value for the control item to set.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_indicator_option: The LED indicator option of the LED type for which to set the control item.
      led_type: The LED type for which to set the control item.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'set_led_control_item',
        nuc_wmi_spec,
        **SET_LED_CONTROL_ITEM_NUC_WMI_SPEC
    )
    set_led_control_item_byte_list = [METHOD_ID, led_type, led_indicator_option, control_item, control_item_value]

    write_control_file(set_led_control_item_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        reserved_byte_1, # pylint: disable=unused-variable
        reserved_byte_2, # pylint: disable=unused-variable
        reserved_byte_3  # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
