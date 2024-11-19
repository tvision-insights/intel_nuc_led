# Intel kernel driver and Python userland CLI tools

## Low-level vs high-level interface

### High-level Python Userland CLI

See [Python nuc_wmi userland](nuc_wmi) documentation for NUC WMI CLI commands. We recommend using this interface over
using the low lowel control file directly for ease of use.

### Low-level Control File Usage (Kernel device)

```
echo xx xx xx xx xx > /proc/acpi/nuc_wmi
```
where the `xx` are a 4-byte hex number followed by 4 1-byte hex numbers:

* first byte: the 4-byte Method ID of the WMI call
* bytes 2-5: the four bytes of arguments passed into the WMI call

This will invoke the specified method with the provided arguments,
and save the return results.

And then:

```
cat /proc/acpi/nuc_wmi
```
will emit 4 1-byte hex numbers, which are the bytes returned by the last
invocation of the WMI system call.

### Low-level Control File bytes and their values

The following Intel documents describe the available Method IDs and
parameters:

* for the NUC6CAY, or NUC7i[x]BN:
  [Use WMI Explorer* to Program the Ring LED and Button LED](https://www.intel.com/content/www/us/en/support/articles/000023426/intel-nuc/intel-nuc-kits.html).

* for the NUC10i3FNH:
  [WMI Interface for Intel NUC Products / WMI Specification / Frost Canyon / July2020 Revision 1.0](https://www.intel.com/content/dam/support/us/en/documents/intel-nuc/WMI-Spec-Intel-NUC-NUC10ixFNx.pdf)

There are copies of these documents here in [reference](reference).

Note that the WMI functions have changed significantly. E.g. the Method IDs
for the older models are 1 and 2, while the they are 3 to 9 for the newer
model.

### Low-level Control File Errors

Errors will appear as warnings in `dmesg` or `journalctl -k`. WMI call
error codes are part of the return value of the WMI call, and shown
through `cat /proc/acpi/nuc_wmi`.

Once the device has been read, a subsequent read without first writing valid bytes
will return the value `ff ff ff ff` (something not used by the WMI call).

## Examples

### NUC6CAY

Make sure you have enabled LED software control in the BIOS, as there
is no WMI call to change that setting on this device.

To set the Ring LED to brightness 80, blink at medium speed, and green:

```
echo 02 02 50 05 06 > /proc/acpi/nuc_wmi
```

where:
* `02`: method ID: "Set LED function"
* `02`: Ring LED command mode
* `50`: 80% brightness (in hex)
* `05`: 0.5 Hz
* `06`: green

### NUC10i3FNH

Make sure you have enabled LED software control in the BIOS, or have
previously executed the WMI call to turn on software control.

To set the Power Button LED to brightness 80, blink at medium speed, and color amber:

```
echo 06 00 04 00 50 > /proc/acpi/nuc_wmi # brightness
echo 06 00 04 01 02 > /proc/acpi/nuc_wmi # blinking behavior
echo 06 00 04 02 05 > /proc/acpi/nuc_wmi # blinking frequency
echo 06 00 04 03 01 > /proc/acpi/nuc_wmi # color
```

where:

* brightness:

  * `06`: method ID: "Set the value to the control item of the indicator option and the LED type"
  * `00`: power button LED
  * `04`: software indicator
  * `00`: brightness control item
  * `50`: brightness value (in hex)

* blinking behavior (same, then):

  * `01`: blinking behavior control item
  * `02`: pulsing

* blinking frequency (same, then):

  * `02`: blinking behavior control item
  * `05`: 5 times 0.1Hz = 0.5Hz

* color (same, then):

  * `03`: color control item
  * `01`: amber color

## Permissions

You can change the owner, group and permissions of `/proc/acpi/nuc_wmi` by
passing parameters to the kernel module. Use:

* `nuc_wmi_uid` to set the owner (default is 0, root)
* `nuc_wmi_gid` to set the owning group (default is 0, root)
* `nuc_wmi_perms` to set the file permissions (default is r+w for
  group and user and r for others)
