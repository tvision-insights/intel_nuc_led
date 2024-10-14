"""
`asus_nuc_wmi.cli.query_led_group_attribute` provides a CLI interface to the WMI query led group attribute of function.
"""

import sys

from argparse import ArgumentParser
from json import dumps

from asus_nuc_wmi import CONTROL_FILE, CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, LOCK_FILE, NucWmiError
from asus_nuc_wmi.query_led_group_attribute import query_led_group_attribute
from asus_nuc_wmi.utils import acquire_file_lock, defined_indexes


def query_led_group_attribute_cli(cli_args=None): # pylint: disable=too-many-locals
    """
    Creates a CLI interface on top of the `asus_nuc_wmi.query_led_group_attribute` `query_led_group_attribute` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
       --debug: Enable debug logging of read and write to the ASUS NUC LED control file to stderr.
       --lock-file <lock_file>: The path to the ASUS NUC WMI lock file.
    Outputs:
       stdout: JSON object with LED group attributes.
    Exit code:
       0 on successfully retrieving the LED group attributes or 1 on error.
    """

    try:
        parser = ArgumentParser(
            description='List all Power Button LED group attributes.'
        )

        parser.add_argument(
            '-c',
            '--control-file',
            default=None,
            help='The path to the ASUS NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Enable debug logging of read and write to the ASUS NUC LED control file to stderr.'
        )
        parser.add_argument(
            '-l',
            '--lock-file',
            default=None,
            help='The path to the ASUS NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            hdd_activity_behavior_range = defined_indexes(CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR)
            led_blink_behavior_range = defined_indexes(LED_BLINK_BEHAVIOR_MULTI_COLOR)
            led_blink_frequency_range = defined_indexes(LED_BLINK_FREQUENCY)
            led_brightness_range = defined_indexes(LED_BRIGHTNESS_MULTI_COLOR)
            led_color_range = defined_indexes(LED_COLOR)
            led_indicator_option_range = defined_indexes(LED_INDICATOR_OPTION)

            (led_indicator_option_index,
             hdd_activity_behavior_index,
             led_color_index,
             led_blink_behavior_index,
             led_blink_frequency_index,
             led_brightness,
             sleep_state_led_color_index,
             sleep_state_led_blink_behavior_index,
             sleep_state_led_blink_frequency_index,
             sleep_state_led_brightness) = query_led_group_attribute(
                 control_file=args.control_file,
                 debug=args.debug
             )

            if led_indicator_option_index not in led_indicator_option_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED "
                    "indicator option of %i, expected one of %s)" % \
                    (led_indicator_option_index, str(led_indicator_option_range))
                )

            if hdd_activity_behavior_index not in hdd_activity_behavior_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED HDD "
                    "activity behavior of %i, expected one of %s)" % (hdd_activity_behavior_index,
                                                                      str(hdd_activity_behavior_range))
                )

            if led_color_index not in led_color_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED color of "
                    "%i, expected one of %s)" % (led_color_index, str(led_color_range))
                )

            if led_blink_behavior_index not in led_blink_behavior_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED blinking "
                    "behavior of %i, expected one of %s)" % (led_blink_behavior_index,
                                                             str(led_blink_behavior_range))
                )

            if led_blink_frequency_index not in led_blink_frequency_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED blinking "
                    "frequency of %i, expected one of %s)" % (led_blink_frequency_index,
                                                              str(led_blink_frequency_range))
                )

            if led_brightness not in led_brightness_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED "
                    "brightness of %i, expected one of %s)" % (led_brightness, str(led_brightness_range))
                )

            if sleep_state_led_color_index not in led_color_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED sleep "
                    "state color of %i, expected one of %s)" % (sleep_state_led_color_index, str(led_color_range))
                )

            if sleep_state_led_blink_behavior_index not in led_blink_behavior_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED sleep "
                    "state blinking behavior of %i, expected one of %s)" % \
                    (sleep_state_led_blink_behavior_index, str(led_blink_behavior_range))
                )

            if sleep_state_led_blink_frequency_index not in led_blink_frequency_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED sleep "
                    "state blinking frequency of %i, expected one of %s)" % (sleep_state_led_blink_frequency_index,
                                                                             str(led_blink_frequency_range))
                )

            if sleep_state_led_brightness not in led_brightness_range:
                raise NucWmiError(
                    "Error (ASUS NUC WMI query_led_group_attribute function returned invalid Power Button LED sleep"
                    " state brightness of %i, expected one of %s)" % (sleep_state_led_brightness,
                                                                      str(led_brightness_range))
                )

            print(
                dumps(
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
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
