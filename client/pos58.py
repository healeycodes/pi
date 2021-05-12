import os
import usb.core
import usb.util
import textwrap

"""Demo program to print to the POS58 USB thermal receipt printer. This is
labeled under different companies, but is made by Zijiang. See
http://zijiang.com

MIT License — Copyright (c) 2019 Vince Patron
"""

# In Linux, you must:
#
# 1) Add your user to the Linux group "lp" (line printer), otherwise you will
#    get a user permissions error when trying to print.
#
# 2) Add a udev rule to allow all users to use this USB device, otherwise you
#    will get a permissions error also. Example:
#
#    In /etc/udev/rules.d create a file ending in .rules, such as
#    33-receipt-printer.rules with the contents:
#
#   # Set permissions to let anyone use the thermal receipt printer
#   SUBSYSTEM=="usb", ATTR{idVendor}=="0416", ATTR{idProduct}=="5011", MODE="666"


def output(data):
    # find our device
    # 0416:5011 is POS58 USB thermal receipt printer
    ID_VENDOR = os.getenv("ID_VENDOR", 0x0416)
    ID_PRODUCT = os.getenv("ID_VENDOR", 0x5011)
    dev = usb.core.find(idVendor=ID_VENDOR, idProduct=ID_PRODUCT)

    # was it found?
    if dev is None:
        raise ValueError("Device not found")

    # disconnect it from kernel
    needs_reattach = False
    if dev.is_kernel_driver_active(0):
        needs_reattach = True
        dev.detach_kernel_driver(0)

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
        == usb.util.ENDPOINT_OUT,
    )

    assert ep is not None

    # print!
    lines = textwrap.wrap(data, width=30)
    for line in lines:
        ep.write(line + "\n")
    ep.write("\n\n")

    # reattach if it was attached originally
    dev.reset()
    if needs_reattach:
        dev.attach_kernel_driver(0)
        print("Reattached USB device to kernel driver")
