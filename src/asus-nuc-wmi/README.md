# ASUS NUC WMI kernel driver

## Building the kernel module

The `asus_nuc_wmi` and  kernel module supports building and installing "from source" directly or using `dkms`.

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
