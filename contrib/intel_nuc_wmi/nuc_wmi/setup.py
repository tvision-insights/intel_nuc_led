"""
Python setuptools wrapper for Python 3.
"""

import os
import setuptools
import sys
import unittest

from setuptools import find_packages, setup


def read_file(file_name):
    """
    File read wrapper for loading data unmodified from arbritrary file.
    """

    file_data = None

    try:
        with open(file_name, 'r') as fin:
            file_data = fin.read()
    except Exception as err: # pylint: disable=broad-except
        print('Failed to read data from file \'%s\': %s' % (file_name, str(err)), file=sys.stderr)
        sys.exit(1)

    return file_data


PYTHON_3_EXTRAS = {}

setuptools.use_2to3_on_doctests = True

setup( # pylint: disable=star-args
    author='Julio Lajara',
    author_email='julio@tvisioninsights.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    description='NUC WMI CLI userland for intel_nuc_led kernel module',
    download_url='https://github.com/tvision-insights/intel_nuc_led',
    entry_points={
        'console_scripts': [
            'nuc_wmi-get_led = nuc_wmi.cli.get_led:get_led_cli',
            'nuc_wmi-get_led_control_item = nuc_wmi.cli.get_led_new:get_led_control_item_cli',
            'nuc_wmi-get_led_indicator_option = nuc_wmi.cli.get_led_new:get_led_indicator_option_cli',
            'nuc_wmi-query_led_control_items = nuc_wmi.cli.query_led:query_led_control_items_cli',
            'nuc_wmi-query_led_color_type = nuc_wmi.cli.query_led:query_led_color_type_cli',
            'nuc_wmi-query_led_indicator_options = nuc_wmi.cli.query_led:query_led_indicator_options_cli',
            'nuc_wmi-query_leds = nuc_wmi.cli.query_led:query_leds_cli',
            'nuc_wmi-save_led_config = nuc_wmi.cli.led_app_notification:save_led_config_cli',
            'nuc_wmi-set_led = nuc_wmi.cli.set_led:set_led_cli',
            'nuc_wmi-set_led_control_item = nuc_wmi.cli.set_led_control_item:set_led_control_item_cli',
            'nuc_wmi-set_led_indicator_option = nuc_wmi.cli.set_led_indicator_option:set_led_indicator_option_cli',
            'nuc_wmi-switch_led_type = nuc_wmi.cli.switch_led_type:switch_led_type_cli',
            'nuc_wmi-wmi_interface_spec_compliance_version = nuc_wmi.cli.version:wmi_interface_spec_compliance_version_cli'
        ]
    },
    license='GPLv2',
    long_description=read_file('README.md'),
    keywords='cli intel kernel led nuc wmi',
    maintainer='Julio Lajara',
    maintainer_email='julio@tvisioninsights.com',
    name='nuc_wmi',
    package_data={
         'nuc_wmi': ['etc/nuc_wmi/nuc_wmi_spec/*']
    },
    package_dir={
        '': 'python'
    },
    packages=find_packages('python', exclude=['test', 'test.*']),
    #tests_require=[
    #    'coverage',
    #    'mock',
    #    'pylint',
    #    'setuptools'
    #],
    url='https://github.com/tvision-insights/intel_nuc_led',
    version='4.0.1',
    zip_safe=True,
    **PYTHON_3_EXTRAS
)
