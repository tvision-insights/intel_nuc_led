# asus_nuc_wmi Python userland for ASUS NUC WMI kernel module

## Compatibility

This `asus_nuc_wmi` userland was written from the available ASUS NUC WMI guide for the NUC 14
(included in the [contrib/reference/](../reference) folder).

It has been tested on NUC 14.

Although we followed the specification documents, we have found that compatibility varies by a number of factors:

* BIOS version (for some settings, the BIOS version may impact what options are available).
* BIOS configuration (for some settings, the BIOS configuration for LEDs can affect whether they are usable and
  in what default state they are in).
* BIOS bugs (we have found some device BIOS have bugs where LEDs which should support RGB are only capable of
  dual color mode through WMI, but are capable of RGB when manually configuring them via the BIOS only).

Aside from the above, command options can change based on the combination of what the BIOS allows and what
indicator option mode LEDs are put in.

Once an LED has been set to `SW Control` in the BIOS, it will remain off initially until a color is explicitly
set, after which the set color is retained across reboots.

## Warnings

The `asus_nuc_wmi` kernel module only allows return values for the last command issued to be read once. If multiple
commands are issued in rapid succession without reading the return code for each in between, then the return
codes are lost.

The CLI commands use a lock file to prevent overlapping concurrent access to the ASUS NUC WMI control file, however
if you are sending commands manually to the control file then it is up to you to make sure you dont send concurrent
commands and potentially lose the return value. If you are using the `asus_nuc_wmi` CLI commands accross multiple users,
you should take care to ensure that the user/group of the lock file is not owned by root or is assigned a group shared by
all users as non root users may not be able to open it if its owner and group are both root.

## Installing from source

The tool conforms to standard Python `pip` packaging and can be installed using `pip` or `setuptools` using
Python >= `3.6`.

When installing from source using the instructions below, be sure to modify the `python` or `pip` executable
commands based on how you have your system setup as they may require appending the version to the end such
as `python3`, `python3.6`, `pip3`, or `pip3.6`.

### Installing from source using system `python`

#### Install using setuptools

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` Python package.
2. Install the `asus_nuc-wmi` package using setuptools:
    ```
    python setup.py install
    ```
3. Run `asus_nuc_wmi-*` commands available in `/usr/bin`.

#### Install using pip

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` and `pip` Python
   packages.
2. Install the package using setuptools or pip:
    ```
    # Install into the system Python library path
    python -m pip install ./

    # Install into the per user Python library path at `~/.local/`
    python -m pip install --user ./
    ```
3. Run `asus_nuc_wmi-*` commands available in `/usr/bin` or `~/.local/bin/` (this may not automatically be in
   your `PATH`) if installed per user.

### Installing from source using `virtualenv`

You can install your own per user `python` and associated virtual library path using normal `virtualenv` tools or
wrappers like [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

Once you have your `virtualenv` setup, activate it and then follow the normal install steps above. When using a
`virtualenv` however, the library path and `bin` paths will be relative to the `virtualenv` parent directory.

## Packaging

The tool conforms to standard Python `pip` packaging using `setuptools` and can be turned into normal PyPi compatible
package in the form of a `wheel`, or distro specific package using `setuptools` helpers.

### Python wheel

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` and `wheel` Python
   packages.
2. Build the `wheel`:
    ```
    python setup.py build bdist_wheel
    ```
3. The `wheel` package is available in the `dist/` folder.

### Debian/Ubuntu deb

1. Use `apt` to install your choice of `python` version and `setuptools` and `stdeb` Python packages.
2. Use `apt` to install `debhelper`, `dh-python`,  and `fakeroot`.
2. Build the `deb` (Note: the Python used for packaging is based on the one used to run the command, we recommend being
    being explicit and using `python3` when creating the deb package):
    ```
    DEB_BUILD_OPTIONS=nocheck python setup.py --command-packages=stdeb.command bdist_deb
    ```
3. The `deb` package is available in the `dist/` folder.

WARNING: Do not use a virtualenv for this build step as stdeb relies on Debian specific Python patches which are only included
in Python when installed at the system level using apt and are not available when using Python in a virtualenv.

## Testing

Use your system's package manager to install your choice of `python` version and `coverage`, `mock`, `pylint`, and `setuptools`
Python packages.

Clean directory:

```
rm -rf .coverage build/ deb_dist/ dist/ python/cover python/asus_nuc_wmi.egg-info asus_nuc_wmi-*.tar.gz
find . -type f -name "*~" -exec rm {} +
find . -type f -name "*.pyc" -exec rm {} +
find . -type d -name "__pycache__" -exec rmdir {} +
```

Run tests:

```
pylint python/asus_nuc_wmi python/test/
python -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
```

Run detailed code coverage report (HTML report available in `htmlcov/`):

```
coverage run --branch --source python/asus_nuc_wmi -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
coverage report -m
coverage html
```

## Example Usage

All `asus_nuc_wmi-*` CLI commands provided by `asus_nuc_wmi` Python module have builtin help via `-h` or `--help` and will
show allowed argument values. Some commands allow a large number of combinations in terms of accepted input values,
so please be sure to reference the WMI spec for the device you are using to see what is actually supported.

### NUC 14:

```
$ asus_nuc_wmi-query_led_group_attribute
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Red' 'Solid' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}
```

## Known Issues

Unfortunately there can be a large set of differences across the devices and sometimes bugs in the BIOS
implementation make it out into the wild.

### NUC 14

* None currently.
