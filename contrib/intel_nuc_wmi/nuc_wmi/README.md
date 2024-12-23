# nuc_wmi Python userland for Intel NUC WMI kernel module

## Compatibility

This `nuc_wmi` userland was written from the merger of available Intel NUC WMI guides for the NUC 7, 8, and 10
(included in the [contrib/reference/](../reference) folder).

It has been tested on NUC 7, 10, and 12 but theoretically should work for all NUCS from 6 through 12.

Although we followed the specification documents, we have found that compatibility varies by a number of factors:

* Device generation (NUC 7 devices for example only support the legacy `get_led` and `set_led` WMI methods).
* BIOS version (for some settings, the BIOS version may impact what options are available).
* BIOS configuration (for some settings, the BIOS configuration for LEDs can affect whether they are usable and
  in what default state they are in).
* BIOS bugs (we have found some device BIOS have bugs where LEDs which should support RGB are only capable of
  dual color mode through WMI, but are capable of RGB when manually configuring them via the BIOS only).

Aside from the above, command options can change based on the combination of what the BIOS allows and what
indicator option mode LEDs are put in.

The kernel side `nuc_wmi` driver used to be named `nuc_led` but this was renamed to `nuc_wmi` due the driver
being turned into a generalized RPC interface for the WMI functions and the fact that some Intel NUCs also
have additional WMI functions for HDMI and USB that can be controlled via the same WMI ID. We currently only
implement the userland functionality for the NUC LED WMI functions.

NUC 7's do not allow for the LEDs to be set to `SW Control` via the WMI calls, and thus in order to control
the LEDs with the Python userland, you must explicitly enable `SW Control` manually in the BIOS. Once an LED
has been set to `SW Control` in the BIOS, it will remain off initially until a color is explicitly set, after
which the set color is retained across reboots.

## Warnings

The `nuc_wmi` kernel module only allows return values for the last command issued to be read once. If multiple
commands are issued in rapid succession without reading the return code for each in between, then the return
codes are lost.

Starting with `nuc_wmi` version `2.3.0`, the CLI commands now use a lock file to prevent overlapping concurrent
access to the NUC WMI control file, however if you are sending commands manually to the control file then it is
up to you to make sure you dont send concurrent commands and potentially lose the return value. If you are using
the `nuc_wmi` CLI commands accross multiple users, you should take care to ensure that the user/group of the
lock file is not owned by root or is assigned a group shared by all users as non root users may not be able to
open it if its owner and group are both root.

## Installing from source

The tool conforms to standard Python `pip` packaging and can be installed using `pip` or `setuptools` using
Python >= `3.6`.

When installing from source using the instructions below, be sure to modify the `python` or `pip` executable
commands based on how you have your system setup as they may require appending the version to the end such
as `python3`, `python3.6`, `pip3`, or `pip3.6`.

### Installing from source using system `python`

#### Install using setuptools

1. Use your system's pacakge manager to install your choice of `python` version and `setuptools` Python package.
2. Install the `nuc-wmi` package using setuptools:
    ```
    python setup.py install
    ```
3. Run `nuc_wmi-*` commands available in `/usr/bin`.

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
3. Run `nuc_wmi-*` commands available in `/usr/bin` or `~/.local/bin/` (this may not automatically be in
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
rm -rf .coverage build/ deb_dist/ dist/ python/cover python/nuc_wmi.egg-info nuc_wmi-*.tar.gz
find . -type f -name "*~" -exec rm {} +
find . -type f -name "*.pyc" -exec rm {} +
find . -type d -name "__pycache__" -exec rmdir {} +
```

Run tests:

```
pylint python/nuc_wmi python/test/
python -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
```

Run detailed code coverage report (HTML report available in `htmlcov/`):

```
coverage run --branch --source python/nuc_wmi -m unittest discover --pattern "*_test.py" --start-directory python/ --verbose
coverage report -m
coverage html
```

## Example Usage

All `nuc_wmi-*` CLI commands provided by `nuc_wmi` Python module have builtin help via `-h` or `--help` and will
show allowed argument values. Some commands allow a large number of combinations in terms of accepted input values,
so please be sure to reference the WMI spec for the device you are using to see what is actually supported.

### NUC WMI Spec Configuration File

In previous 2.x releases, we had introduced the concept of `quirks` mode CLI flag to try to change the runtime behavior of the CLI
commands in order to accomodate the differences in behavior for the NUC WMI functions across different generations and to account for
BIOS bugs and allow us to better recover from different issues. This method was unfortunately cumbersome to manage as we added more
devices and did not scale well.

This is now replaced with a NUC WMI spec configuration file. This configuration file allows us to configure the expected return types
for the NUC WMI functions supported by the NUC as well as in some cases recover from "out of bound" return values where the NUC WMI
functions sometimes return invalid values in certain scenarios.

This implementation is driven by the fact that the return types of the functions may change from one NUC generation to the next and
the "out of bound" return value are the only things we can customize to try to make the NUC WMI functions work as expected. If it
still doesnt work with that, then it is likely a BIOS bug.

The supported return types and "out of bound" return value recovery support is as follows:

|NUC WMI function                       |Supported return types|OOB Return Recovery values|
|---------------------------------------|----------------------|--------------------------|
|`get_led`                              |`index`               |`false`,`true`            |
|`get_led_control_item`                 |`bitmap`, `index`     |`false`                   |
|`get_led_indicator_option`             |`bitmap`, `index`     |`false`                   |
|`query_led_color_type`                 |`bitmap`, `index`     |`false`                   |
|`query_led_control_items`              |`bitmap`              |`false`                   |
|`query_led_indicator_options`          |`bitmap`              |`false`                   |
|`query_leds`                           |`bitmap`              |`false`                   |
|`save_led_config`                      |`null`                |`false`                   |
|`set_led`                              |`null`                |`false`                   |
|`set_led_control_item`                 |`null`                |`false`                   |
|`set_led_indicator_option`             |`null`                |`false`                   |
|`switch_led_type`                      |`null`                |`false`                   |
|`wmi_interface_spec_compliance_version`|`index`               |`false`                   |

The NUC WMI spec `index` type casts the returned byte(s) into an integer and is used when a single value is returned by the function
while the `bitmap` is used for functions that can return 0 or more values at once by treating it as a binary bitmap where enabled
bits correspond to indexes in a list of value types.

The NUC WMI spec configuration file is a JSON formatted file with the following specification:

```
{
  "<nuc_wmi_spec_alias>": {
    "led_hints": {
      "color_type": {
        "<led type (nuc_wmi.LED_TYPE)>": "<led color type name (nuc_wmi.LED_COLOR_TYPE)>
      },
      "indicator_options": {
        "<led type (nuc_wmi.LED_TYPE)>": [
          "<indicator option (nuc_wmi.LED_INDICATOR_OPTION)>"
        ]
      },
      "rgb_color_type_dimensions": {
        "<led type (nuc_wmi.LED_TYPE)>": <1 or 3>
      }
    },
    "nuc_wmi_spec": {
      "function_return_type": {
        "<nuc_wmi_function_name>": "<nuc_wmi_function_return_type string|unquoted JSON null>"
      },
      "recover": {
        "function_oob_return_value": {
          "<nuc_wmi_function_name>": <JSON boolean>
        },
        "missing_disable_indicator_option": {
          "<led type (nuc_wmi.LED_TYPE)>": <JSON boolean>
        }
      }
    }
  }
}
```

The `nuc_wmi_spec_alias` is a board NUC WMI spec definition name used as the first argument to CLI commands.

The CLI commands look for the NUC WMI spec JSON file with the following precedence order and the first location
found is used:

1. `~/.nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json`
2. `/etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json`
3. `<nuc_wmi pip package install path>/etc/nuc_wmi_spec/nuc_wmi_spec.json`

Note that while we include a default NUC WMI spec JSON file in the Python package, we dont guarantee it will work
with the board generation specified as it may depend on what BIOS version you have installed. Always double check
the NUC WMI manual for your explicit NUC model and update the spec file as needed.

The `led_hints` in the NUC WMI spec is an attempt to resolve the permformance issues present in NUC 10 and NUC 12 BIOS
by adding hints for the `get_led_control_item`, `query_led_color_type`, `query_led_indicator_options`, and `set_led_control_item`
methods so that each CLI command corresponds to at most one WMI method call. Without these hints, due to simplifying
of the WMI method interfaces for the CLI and added error handling, some of the CLI commands may end up being 3 or 4 NUC
WMI calls otherwise. If you care about the performance of the WMI calls (for example, if you need to set the 3 dimension RGB
color as quickly as possible to minimize flash between different colors), then we recommend adding hints to the NUC WMI
spec alias that you use for your NUC. The hints just hard code the responses you would expect to get from the WMI methods.
If you do not specify the hints, then it falls back to making the WMI calls necessary to get the information it needs.

The `missing_disable_indicator_option` NUC WMI spec configuration recover option can be used to forcibly make sure that
`query_led_indicator_options` includes the `Disable` indicator option for BIOS that have the bug that causes it to not be included
even though it is supported by the LEDs.

### NUC 7:

```
# Note: When a legacy device (NUC 7 or older) has disabled software control in BIOS, we can't change it
# via WMI like we can on newer models. Trying to use a LED that hasnt had software control enabled will return
# this error.
$ nuc_wmi-get_led 'NUC_7' 'S0 Power LED'
{"error": "Error (Undefined device)"}

$ nuc_wmi-get_led 'NUC_7' 'S0 Ring LED'
{"led": {"color": "White", "frequency": "Always on", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}

# Brightness is an integer percentage 0-100 and not the internal WMI hex value.
$ nuc_wmi-set_led 'NUC_7' 'S0 Ring LED' 100 'Always on' 'White'
{"led": {"color": "White", "frequency": "Always on", "type": "S0 Ring LED", "brightness": "100"}, "nuc_wmi_spec_alias": "NUC_7"}
```

### NUC 10:

```
$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Brightness'
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}
# For BIOS where the HDD LED LED color type is "Dual-color Blue / White"
$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "White"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color'
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-get_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Brightness'
{"led": {"control_item": "S0 Indicator Brightness", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "50"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-get_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-get_led_indicator_option 'NUC_10' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-get_led_indicator_option 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_color_type 'NUC_10' 'HDD LED'
{"led": {"color_type": "Dual-color Blue / White", "type": "HDD LED"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_color_type 'NUC_10' 'Power Button LED'
{"led": {"color_type": "Dual-color Blue / Amber", "type": "Power Button LED"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_color_type 'NUC_10' 'HDD LED'
{"led": {"color_type": "RGB-color", "type": "HDD LED"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_control_items 'NUC_10' 'Power Button LED' 'Power State Indicator'
{"led": {"control_items": ["S0 Indicator Brightness", "S0 Indicator Blinking Behavior", "S0 Indicator Blinking Frequency", "S0 Indicator Color"], "type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_control_items 'NUC_10' 'Power Button LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "Power Button LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_control_items 'NUC_10' 'HDD LED' 'Software Indicator'
{"led": {"control_items": ["Brightness", "Blinking Behavior", "Blinking Frequency", "Color"], "type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_control_items 'NUC_10' 'HDD LED' 'HDD Activity Indicator'
{"led": {"control_items": ["Brightness", "Color", "Color 2", "Color 3"], "type": "HDD LED", "indicator_option": "HDD Activity Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-query_led_indicator_options 'NUC_10' 'HDD LED'
{"led": {"type": "HDD LED", "indicator_options": ["HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-query_led_indicator_options 'NUC_10' 'Power Button LED'
{"led": {"type": "Power Button LED", "indicator_options": ["Power State Indicator", "HDD Activity Indicator", "Software Indicator"]}, "nuc_wmi_spec_alias": "NUC_10"}

# RGB Header is only available if on the latest BIOS
$ nuc_wmi-query_leds 'NUC_10'
{"leds": ["Power Button LED", "HDD LED", "RGB Header"], "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-save_led_config 'NUC_10'
{"led_app_notification": {"type": "save_led_config"}, "nuc_wmi_spec_alias": "NUC_10"}

# Brightness is an integer percentage 0-100 and not the internal WMI hex value.
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Brightness' 100
{"led": {"control_item": "Brightness", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "100"}, "nuc_wmi_spec_alias": "NUC_10"}
# Blinking Frequency is 0.1Hz-1.0Hz
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Blinking Frequency' '1.0Hz'
{"led": {"control_item": "Blinking Frequency", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "1.0Hz"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-set_led_control_item 'NUC_10' 'Power Button LED' 'Power State Indicator' 'S0 Indicator Color' Blue
{"led": {"control_item": "S0 Indicator Color", "type": "Power Button LED", "indicator_option": "Power State Indicator", "control_item_value": "Blue"}, "nuc_wmi_spec_alias": "NUC_10"}
# For BIOS where the HDD LED LED color type is "RGB-color" but 1D (where only 'Color' is a supported control item)
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color' 'Indigo'
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "Indigo"}, "nuc_wmi_spec_alias": "NUC_10"}
# For LEDs where the color type is RGB-color but 3D, the color is controlled by 3 dimension settings (one for Red, Green, and Blue respectively) that accept
# an integer value from 0-255 for each color dimension. There may be multiple control item triplets for RGB colors per indicator option. For
# this example we pretend the HDD LED reports its color type as RGB-color and we set the LED to Red (you must set all 3 dimensions to ensure you end up with the correct color).
# If you want to avoid having the color change as you set the dimensions, your only option is to drop the brightness down to 0 before settng the color and back to a
# non zero brightness once its set.
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color' '255' # Red dimension
{"led": {"control_item": "Color", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "255"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color 2' '0' # Green dimension
{"led": {"control_item": "Color 2", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-set_led_control_item 'NUC_10' 'HDD LED' 'Software Indicator' 'Color 3' '0' # Blue dimension
{"led": {"control_item": "Color 3", "type": "HDD LED", "indicator_option": "Software Indicator", "control_item_value": "0"}, "nuc_wmi_spec_alias": "NUC_10"}

$ nuc_wmi-set_led_indicator_option 'NUC_10' 'HDD LED' 'Software Indicator'
{"led": {"type": "HDD LED", "indicator_option": "Software Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}
$ nuc_wmi-set_led_indicator_option 'NUC_10' 'Power Button LED' 'Power State Indicator'
{"led": {"type": "Power Button LED", "indicator_option": "Power State Indicator"}, "nuc_wmi_spec_alias": "NUC_10"}

# No idea what this WMI function does, I just implemented it according to spec. It doesnt work on NUC 10.
$ nuc_wmi-switch_led_type 'NUC_10' 'Single color LED'
$ nuc_wmi-switch_led_type 'NUC_10' 'Multi color LED'

$ nuc_wmi-wmi_interface_spec_compliance_version 'NUC_10'
{"version": {"semver": "1.32", "type": "wmi_interface_spec_compliance"}, "nuc_wmi_spec_alias": "NUC_10"}
```

## Known Issues

Unfortunately there can be a large set of differences across the devices and sometimes bugs in the BIOS
implementation make it out into the wild.

### NUC 7

* The `get_led` NUC WMI method is know to return out of bound values for `brightness`, `frequency`, and `color`.
  This usually happens on factory fresh refurbished devices and only on the first attempt to read values from
  device memory. Once you have used `set_led` to explicit set good values, then subsequent `get_led` calls should
  work fine. We recommend enabling OOB recovery in the NUC WMI spec file.

  When OOB recovery is enabled, brightness and color return `0` and frequency returns `1` if any of their
  values are outside of accepted spec range.

### NUC 10

* The NUC 10 BIOS released before December 2020 did not have support for the RGB Header on the NUC and also required
  different return types for `get_led_indicator_option` and `query_led_color_type` NUC WMI methods when compared
  to BIOS released later. This device therefore requires different NUC WMI spec configurations depending on your BIOS
  version.

  For NUC 10 BIOS released before December 2020, `get_led_indicator_option` and `query_led_color_type` have a
  return type of `index`, otherwise they have a return type of `bitmap`.

  An alternative way to check what your BIOS supports without needing to know the BIOS's release date is to run the
  `nuc_wmi-query_leds` CLI command and see if returns `RGB Header` as an option or not in the supported LED types.

* The NUC 10 BIOS does not return `Disable` indicator option for any LED when you run `query_led_indicator_options` even
  though `get_led_indicator_option` and `set_led_indicator_option` do support this indicator option.

### NUC 12

* The NUC 12 BIOS releases prior to WS9087 are in various states of functionality. In its orignal release form, the
  BIOS had invalid return types for methods compared to what was documented and subsequent releases had broken
  `get_led_control_item` and `set_led_control_item` implementations that could not be worked around by simply modifying the
  the WMI spec definition for return types. The broken implementations had different behavior for each of the indicator
  option modes. All current NUC 12 BIOS releases have severe performance degradation and are 20-100x slower for some
  WMI method calls. The performance issue is a BIOS side issue that we cannot resolve.

* The NUC 12 BIOS does not return `Disable` indicator option for any LED when you run `query_led_indicator_options` even
  though `get_led_indicator_option` and `set_led_indicator_option` do support this indicator option.
