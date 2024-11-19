# Intel and ASUS NUC WMI kernel driver and Python userland CLI tools

This is a simple kernel module that serves as an RPC interface for internal WMI functions
on Intel/ASUS NUCs through a control file leveraging the Linux kernel /proc tree with
optional high-level userspace tools written in Python.

The current `2.0` version of the kernel driver is backwards incompatible with the original `1.0`
version which only supported Intel NUC 6 and 7. Reference the
[old documentation](https://github.com/milesp20/intel_nuc_led/tree/6a3850eadff554053ca7d95e830a624b28c53670)
for `1.0` usage.

Please be aware that while this repo was originally intended to control the Intel NUC LED, the driver has
now been renamed to be generic and not specific to the LED now that its a low level interface to the WMI
functions since some NUC models also support controlling the HDMI and USB bus via other WMI functions. We
currently do not implement CLI helper methods for those and only support the NUC LED WMI functions in the
current userland.

Pull requests appreciated as well reports if you could (or could not) get it
running on other NUCs with software-controllable LEDs, and other distros.

## Known Issues

* Currently, 5.x kernels in Ubuntu 20.04 and 22.04 have a kernel level bug with using Python to read from
  the control file in a buffered I/O manner that reads to EOF/EOL from the control file. To work around this issue,
  you must read a fixed number of bytes from the control file. This bug is irrelevant of the NUC LED kernel driver.

  As of `nuc_wmi` CLI `3.0.1`, we work around this issue by reading/writing to the control file using unbuffered
  I/O and fixed length reading from the control file.
* Performance of the Intel/ASUS NUC WMI methods is severely degraded in NUC 12s and is about 20-100x slower for some
  WMI methods than previously on the Intel NUC 10. This is a BIOS issue that we cant work around due to a delayed
  response.

## Requirements

Requirements:

* Intel NUC 6 through 12, ASUS NUC 12, or ASUS NUC 14
* ACPI/WMI support in kernel

## LED Header Breakout Boards

Example Intel NUC LED header breakout boards for internal LED headers are available in
[contrib/intel_nuc_wmi/led_header_boards](contrib/intel_nuc_wmi/led_header_boards).

## Choosing the right kernel driver and Python userland for your NUC device

As of the NUC 12, Intel sold the NUC device line to ASUS and they now manufacture and support the NUC device generations
moving forward. NUC 12 models were initially manufactured by Intel and shifted manufacturing to ASUS. Devices after the NUC 12
are all fully manufactured and supported by ASUS.

Kernel driver:

* [nuc_wmi](src/intel-nuc-wmi): Supports all NUC generations up the the NUC 12 (including the ASUS manufactured NUC 12).
* [asus_nuc_wmi](src/asus-nuc-wmi): Supports NUC generations after the NUC 12, currently only tested with ASUS NUC 14.

Python userland:

* [nuc_wmi](contrib/intel_nuc_wmi): Supports all NUC generations up the the NUC 12 (including the ASUS manufactured NUC 12).
* [asus_nuc_wmi](contrib/asus_nuc_wmi): Supports NUC generations after the NUC 12, currently only tested with ASUS NUC 14.

## Building the kernel module

The `asus_nuc_wmi` and `nuc_wmi` kernel modules support building and installing "from source" directly or using `dkms`.

For the `asus_nuc_wmi` kernel module change directories to `src/asus-nuc-wmi` or for `nuc_wmi` kernel module change
directories to `src/intel-nuc-wmi` and run follow the steps below to install build dependencies and then build and
install from source or dkms.

### Installing Build Dependencies

Ubuntu:

```
apt-get install build-essential linux-headers-$(uname -r)

# DKMS dependencies
apt-get install debhelper dkms fakeroot
```

Redhat:

```
yum groupinstall "Development Tools"
yum install kernel-devel-$(uname -r)

# Install appropriate EPEL for DKMS if needed by your RHEL variant
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

yum install dkms
```

### Building and Installing "from source"

```
make clean
make install
```

### Building and Installing Using DKMS

You can override the `KVERSION` or `KDIR` environment variables to customize the build as needed.

Build and install without system packaging:

```
make dkms-install
```

Uninstall without system packaging:

```
make dkms-uninstall
```

Build and install using system packaging:

```
# Ubuntu
make dkms-deb

# RHEL
make dkms-rpm

# Install generated DEB/RPM from the folder specified in the output using system package manager
```
