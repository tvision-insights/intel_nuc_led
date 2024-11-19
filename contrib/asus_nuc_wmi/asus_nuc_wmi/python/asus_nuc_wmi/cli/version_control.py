"""
`asus_nuc_wmi.cli.version` provides a CLI interface to the WMI version control functions.
"""

import sys

from argparse import ArgumentParser
from json import dumps

from asus_nuc_wmi import CONTROL_FILE, LOCK_FILE
from asus_nuc_wmi.utils import acquire_file_lock
from asus_nuc_wmi.version_control import version_control


def version_control_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `asus_nuc_wmi.version_control` `version_control` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Options:
       --blocking-file-lock: Acquire a blocking lock on the ASUS NUC WMI lock file instead of the default
                             non blocking lock.
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `asus_nuc_wmi.CONTROL_FILE` is used.
       --debug: Enable debug logging of read and write to the ASUS NUC LED control file to stderr.
       --lock-file <lock_file>: The path to the ASUS NUC WMI lock file.
    Outputs:
       stdout: JSON object with version and type or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the WMI version control version or 1 on error.
    """

    try:
        parser = ArgumentParser(
            description='Get the WMI version control version.'
        )

        parser.add_argument(
            '-b',
            '--blocking-file-lock',
            action='store_true',
            help='Acquire a blocking lock on the ASUS NUC WMI lock file instead of the default non blocking lock.'
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
            acquire_file_lock(lock_file, blocking_file_lock=args.blocking_file_lock)

            wmi_version = version_control(
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            wmi_semver = '.'.join([str(semver_component) for semver_component in wmi_version])

            print(
                dumps(
                    {
                        'version_control': {
                            'type': 'version',
                            'semver': wmi_semver
                        }
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
