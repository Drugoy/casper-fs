CONFIG_MODULE_SIG=n
PWD := $(shell pwd)
CC := gcc
KERNEL_PATH ?= /lib/modules/$(shell uname -r)/build
ccflags-y	+= -Wall -Wdeclaration-after-statement -Wno-unused-variable -Wno-unused-function

obj-m += CASPER_BINARY_NAME.o
CASPER_BINARY_NAME-objs := main.o hooked.o 

all:
	make -C $(KERNEL_PATH) M=$(PWD) modules

clean:
	make -C $(KERNEL_PATH) M=$(PWD) clean
