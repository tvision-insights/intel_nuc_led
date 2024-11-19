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
    description='ASUS NUC WMI CLI userland for asus_nuc_wmi kernel module',
    download_url='https://github.com/tvision-insights/intel_nuc_led',
    entry_points={
        'console_scripts': [
            'asus_nuc_wmi-query_led_group_attribute = asus_nuc_wmi.cli.query_led_group_attribute:query_led_group_attribute_cli',
            'asus_nuc_wmi-update_led_group_attribute = asus_nuc_wmi.cli.update_led_group_attribute:update_led_group_attribute_cli',
            'asus_nuc_wmi-version_control = asus_nuc_wmi.cli.version_control:version_control_cli'
        ]
    },
    license='GPLv2',
    long_description=read_file('README.md'),
    keywords='asus cli kernel led nuc wmi',
    maintainer='Julio Lajara',
    maintainer_email='julio@tvisioninsights.com',
    name='asus_nuc_wmi',
    package_dir={
        '': 'python'
    },
    packages=find_packages('python', exclude=['test', 'test.*']),
    # tests_require=[
    #     'coverage=',
    #     'mock',
    #     'pylint',
    #     'setuptools'
    # ],
    url='https://github.com/tvision-insights/intel_nuc_led',
    version='1.1.0',
    zip_safe=True,
    **PYTHON_3_EXTRAS
)
