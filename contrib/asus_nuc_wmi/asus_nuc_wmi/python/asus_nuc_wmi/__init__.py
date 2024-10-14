"""
asus_nuc_wmi CLI userland for the ASUS NUC LED kernel module.
"""

import os
import tempfile

CONTROL_FILE = '/proc/acpi/asus_nuc_wmi'

CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR = [
    'Normally OFF, ON when active',
    'Normally ON, OFF when active'
]

LED_COLOR = [
    'Black',
    'Blue',
    'Green',
    'Cyan',
    'Red',
    'Magenta',
    'Amber',
    'White'
]

LED_BLINK_BEHAVIOR_MULTI_COLOR = [
    'Solid',
    'Breathing',
    'Pulsing',
    'Strobing'
]

LED_BLINK_FREQUENCY = [
    '0Hz',
    '0.1Hz',
    '0.2Hz',
    '0.3Hz',
    '0.4Hz',
    '0.5Hz',
    '0.6Hz',
    '0.7Hz',
    '0.8Hz',
    '0.9Hz',
    '1.0Hz'
]

LED_BRIGHTNESS_MULTI_COLOR = [str(brightness) for brightness in range(0x00, 0x64 + 1)]

LED_INDICATOR_OPTION = [
    'Disable',
    'Power State Indicator',
    'HDD Activity Indicator',
    'Software Indicator'
]

LOCK_FILE = os.path.join(tempfile.gettempdir(), 'asus_nuc_wmi.lock')

# Return value of FF FF FF FF is specific to the driver, not the actual WMI implementation.
# Some of these return errors are the generic ASUS NUC WMI errors, not all are specific to the NUC LEDs.
RETURN_ERROR = {
    0xE1: 'Error (Function not supported)',
    0xE2: 'Error (Undefined device)',
    0xE3: 'Error (EC doesn\'t respond)',
    0xE4: 'Error (Invalid Parameter)',
    0xE5: 'Error (Node busy. Command could not be executed because ' + \
    'command processing resources are temporarily unavailable.)',
    0xE6: 'Error (Command execution failure. ' + \
    'Parameter is illegal because destination device has been disabled or is unavailable)',
    0xE7: 'Error (Invalid CEC Opcode)',
    0xE8: 'Error (Data Buffer size is not enough)',
    0xEF: 'Error (Unexpected error)',
    0xFF: 'Error (Return value has already been read and reset)'
}

class NucWmiError(Exception):
    """
    ASUS NUC WMI error exception type.
    """
    pass # pylint: disable=unnecessary-pass
