obj-m := nuc_wmi.o

DKMS_MODULE := intel-nuc-wmi
DKMS_MODULE_VERSION := 2.2
KDIR ?= /lib/modules/$(KVERSION)/build
KVERSION ?= $(shell uname -r)
PWD := $(shell pwd)

.PHONY: clean all dkms-add dkms-build dkms-deb dkms-install dkms-rpm dkms-uninstall install install_build_deps install_build_deps_rhel

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

dkms-add:
	dkms add --force $(PWD)

dkms-build: dkms-add
	dkms build -m $(DKMS_MODULE) -v $(DKMS_MODULE_VERSION) -k $(KVERSION)

dkms-deb: dkms-add
	dkms mkdeb $(DKMS_MODULE)/$(DKMS_MODULE_VERSION) --source-only

dkms-install: dkms-build
	dkms install -m $(DKMS_MODULE) -v $(DKMS_MODULE_VERSION) -k $(KVERSION)
	@depmod -a $(KVERSION)

dkms-rpm: dkms-add
	dkms mkrpm $(DKMS_MODULE)/$(DKMS_MODULE_VERSION) --source-only

dkms-status:
	dkms status $(DKMS_MODULE)/$(DKMS_MODULE_VERSION) -k $(KVERSION)

dkms-uninstall:
	dkms remove -m $(DKMS_MODULE) -v $(DKMS_MODULE_VERSION) --all
	rm -rf /usr/src/$(DKMS_MODULE)-$(DKMS_MODULE_VERSION)/

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	@depmod -a $(KVERSION)

install_build_deps:
	apt-get install -y build-essential debhelper dkms fakeroot

install_build_deps_rhel:
	yim groupinstall -y "Development Tools"
	yum install -y dkms kernel-devel-$(KVERSION)
