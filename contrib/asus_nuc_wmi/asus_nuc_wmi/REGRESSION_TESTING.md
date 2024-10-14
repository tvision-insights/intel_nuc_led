# ASUS NUC WMI Function regression test plan

The tests should be run in the order specified here. The tests include argument values that span the beginning
and end of the enum range for each input value type to ensure we no longer have any more issues with processing
of the WMI return values.

Note: When running HDD Activity tests, you can use
`dd if=/dev/random of=/tmp/empty_raw_file bs=1M count=1000 status=progress; rm -f /tmp/empty_raw_file`
to trigger blinking from writing on SSDs.

## asus_nuc_wmi-query_led_group_attribute

### NUC 14

```
$ asus_nuc_wmi-query_led_group_attribute
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}
```

## asus_nuc_wmi-update_led_group_attribute

### NUC 14

```
$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Red' 'Solid' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Red' 'Solid' '0.1Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "0.1Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Red' 'Solid' '1.0Hz' '0' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "0", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Black' 'Solid' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Black", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally ON, OFF when active' 'White' 'Solid' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "White", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Disable' 'Normally OFF, ON when active' 'Red' 'Solid' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Disable", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Solid", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}

$ asus_nuc_wmi-update_led_group_attribute 'Software Indicator' 'Normally OFF, ON when active' 'Red' 'Strobing' '1.0Hz' '100' 'Amber' 'Breathing' '0.9Hz' '99'
{"led": {"type": "Power Button LED", "indicator_option": "Software Indicator", "hdd_activity_behavior": "Normally OFF, ON when active", "color": "Red", "blinking_behavior": "Strobing", "blinking_frequency": "1.0Hz", "brightness": "100", "sleep_state_color": "Amber", "sleep_state_blinking_behavior": "Breathing", "sleep_state_blinking_frequency": "0.9Hz", "sleep_state_brightness": "99"}}
```
