# ASUS kernel driver and Python userland CLI tools

## Low-level vs high-level interface

### High-level Python Userland CLI

See [Python asus_nuc_wmi userland](asus_nuc_wmi) documentation for ASUS NUC WMI CLI commands. We recommend using this interface over
using the low lowel control file directly for ease of use.

### Low-level Control File Usage (Kernel device)

```
# 257 bytes written in, 256 bytes read out
echo xx xx xx xx xx .. > /proc/acpi/asus_nuc_wmi
```
where the `xx` are a 4-byte hex number followed by 256 1-byte hex numbers:

* first byte: the 4-byte Method ID of the WMI call
* bytes 2 to 256: the 256 bytes of arguments passed into the WMI call (unused values can be set to 0)

This will invoke the specified method with the provided arguments,
and save the return results.

And then:

```
cat /proc/acpi/asus_nuc_wmi
```
will emit 256 1-byte hex numbers, which are the bytes returned by the last
invocation of the WMI system call.

### Low-level Control File bytes and their values

The following ASUS documents describe the available Method IDs and
parameters here in [reference](reference).

### Low-level Control File Errors

Errors will appear as warnings in `dmesg` or `journalctl -k`. WMI call
error codes are part of the return value of the WMI call, and shown
through `cat /proc/acpi/asus_nuc_wmi`.

Once the device has been read, a subsequent read without first writing valid bytes
will return the value 256 1-byte values of `ff` (something not used by the WMI call).

## Examples

### NUC14RVK-B

```
# Set 'Software Indicator' 'Normally OFF, ON when active' Amber Strobing 0.1Hz 50 Black Solid 1.0Hz 0
echo 101 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 > /proc/acpi/asus_nuc_wmi
```

Note: With the NUC 14, you must start bytes 1 to 257 with output of a query led group attribute call and then
overlay the updated values for bytes 1, 8, 28-33, and 37-40 in order to make a call to update led group attribute.

When calling query led group attribute, see the reference doc for how to interpret the returned values for bytes
0, 7, 27-32, 36-39.

When calling update led group attribute, see the reference doc for allowed input values for bytes
0, 7, 27-32, 36-39 (note that because the first byte on writing to control file is the method id,
you must add 1 to these byte positions when constructing the input array of 257 bytes).

## Permissions

You can change the owner, group and permissions of `/proc/acpi/asus_nuc_wmi` by
passing parameters to the kernel module. Use:

* `asus_nuc_wmi_uid` to set the owner (default is 0, root)
* `asus_nuc_wmi_gid` to set the owning group (default is 0, root)
* `asus_nuc_wmi_perms` to set the file permissions (default is r+w for
  group and user and r for others)
