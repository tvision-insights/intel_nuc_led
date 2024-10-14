"""
`asus_nuc_wmi.cli.update_led_group_attribute` provides a CLI interface to the WMI update led group attribute of
function.
"""

import sys

from argparse import ArgumentParser
from json import dumps

from asus_nuc_wmi import CONTROL_FILE, CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR, LED_COLOR
from asus_nuc_wmi import LED_BLINK_BEHAVIOR_MULTI_COLOR, LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR
from asus_nuc_wmi import LED_INDICATOR_OPTION, LOCK_FILE
from asus_nuc_wmi.update_led_group_attribute import update_led_group_attribute
from asus_nuc_wmi.utils import acquire_file_lock


def update_led_group_attribute_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `asus_nuc_wmi.update_led_group_attribute` `update_led_group_attribute`
    function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led_indicator_option: The LED indicator option for the Power Button LED.
       hdd_activity_behavior: The LED HDD activity behavior for the Power Button LED.
       led_color: The LED color for the Power Button LED.
       led_blink_behavior: The LED blink behavior for the Power Button LED.
       led_blink_frequency: The LED blink frequency for the Power Button LED.
       led_brightness: The LED brightness for the Power Button LED.
       sleep_state_led_color: The LED color for the Power Button LED sleep state.
       sleep_state_led_blink_behavior: The LED blink behavior for the Power Button LED sleep state.
       sleep_state_led_blink_frequency: The LED blink frequency for the Power Button LED sleep state.
       sleep_state_led_brightness: The LED brightness for the Power Button LED sleep state.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
       --debug: Enable debug logging of read and write to the ASUS NUC LED control file to stderr.
       --lock-file <lock_file>: The path to the ASUS NUC WMI lock file.
    Outputs:
       stdout: JSON object with LED group attributes.
    Exit code:
       0 on successfully updating the LED group attributes or 1 on error.
    """

    try:
        parser = ArgumentParser(
            description='Update all Power Button LED group attributes.'
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
        parser.add_argument(
            'led_indicator_option',
            choices=LED_INDICATOR_OPTION,
            help='The LED indicator option for the Power Button LED.'
        )
        parser.add_argument(
            'hdd_activity_behavior',
            choices=CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR,
            help='The LED HDD activity behavior for the Power Button LED.'
        )
        parser.add_argument(
            'led_color',
            choices=LED_COLOR,
            help='The LED color for the Power Button LED.'
        )
        parser.add_argument(
            'led_blink_behavior',
            choices=LED_BLINK_BEHAVIOR_MULTI_COLOR,
            help='The LED blink behavior for the Power Button LED.'
        )
        parser.add_argument(
            'led_blink_frequency',
            choices=LED_BLINK_FREQUENCY,
            help='The LED blink frequency for the Power Button LED.'
        )
        parser.add_argument(
            'led_brightness',
            choices=LED_BRIGHTNESS_MULTI_COLOR,
            help='The LED brightness for the Power Button LED.'
        )
        parser.add_argument(
            'sleep_state_led_color',
            choices=LED_COLOR,
            help='The LED color for the Power Button LED sleep state.'
        )
        parser.add_argument(
            'sleep_state_led_blink_behavior',
            choices=LED_BLINK_BEHAVIOR_MULTI_COLOR,
            help='The LED blink behavior for the Power Button LED sleep state.'
        )
        parser.add_argument(
            'sleep_state_led_blink_frequency',
            choices=LED_BLINK_FREQUENCY,
            help='The LED blink frequency for the Power Button LED sleep state.'
        )
        parser.add_argument(
            'sleep_state_led_brightness',
            choices=LED_BRIGHTNESS_MULTI_COLOR,
            help='The LED brightness for the Power Button LED sleep state.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            update_led_group_attribute(
                LED_INDICATOR_OPTION.index(args.led_indicator_option),
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_BEHAVIOR.index(args.hdd_activity_behavior),
                LED_COLOR.index(args.led_color),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index(args.led_blink_behavior),
                LED_BLINK_FREQUENCY.index(args.led_blink_frequency),
                LED_BRIGHTNESS_MULTI_COLOR.index(args.led_brightness),
                LED_COLOR.index(args.sleep_state_led_color),
                LED_BLINK_BEHAVIOR_MULTI_COLOR.index(args.sleep_state_led_blink_behavior),
                LED_BLINK_FREQUENCY.index(args.sleep_state_led_blink_frequency),
                LED_BRIGHTNESS_MULTI_COLOR.index(args.sleep_state_led_brightness),
                control_file=args.control_file,
                debug=args.debug
            )

            print(
                dumps(
                    {
                        'led': {
                            'type': 'Power Button LED',
                            'indicator_option': args.led_indicator_option,
                            'hdd_activity_behavior': args.hdd_activity_behavior,
                            'color': args.led_color,
                            'blinking_behavior': args.led_blink_behavior,
                            'blinking_frequency': args.led_blink_frequency,
                            'brightness': args.led_brightness,
                            'sleep_state_color': args.sleep_state_led_color,
                            'sleep_state_blinking_behavior': args.sleep_state_led_blink_behavior,
                            'sleep_state_blinking_frequency': args.sleep_state_led_blink_frequency,
                            'sleep_state_brightness': args.sleep_state_led_brightness
                        }
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
