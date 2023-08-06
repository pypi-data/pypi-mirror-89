"""
pykitcommander - Python Kit Commander
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pykitcommander manages interaction with Microchip development kits based on
PKOB nano on-board debugger

In many situations interaction with peripheral hardware components on a
development kit is done via a "bridge" application running on the MCU on that
kit.  To achieve this, the bridge firmware must be programmed onto that MCU,
and then communications over a given channel and protocol can logically link
the host computer to the peripheral components.

pykitcommander manages all aspects of this interaction.

Supported kits are:
    * AVR-IOT (all variants)
    * PIC-IOT (all variants)

Dependencies
~~~~~~~~~~~~
This package uses pyedbglib for USB communications.
For more information see: https://pypi.org/project/pyedbglib/

Usage example 1
~~~~~~~~~~~~~~~
Short example usage in AVR-IoT and PIC-IoT kits:

Request protocol (and auto-detected port) via IoT helper function
Then use KitSerialConnection() to manage port open/close
    >>> from pykitcommander.kitprotocols import get_iot_provision_protocol
    >>> protocol, port = get_iot_provision_protocol()
    >>> from pykitcommander.firmwareinterface import KitSerialConnection
    >>> with KitSerialConnection(protocol, port):
            ecc_serial_number = protocol.read_ecc_serialnumber()

Usage example 2
~~~~~~~~~~~~~~~
Long example usage in AVR-IoT and PIC-IoT kits:

Discover kit information about the connected kit
    >>> from pykitcommander.kitmanager import KitProgrammer
    >>> programmer = KitProgrammer()
    >>> print (programmer.kit_info)

List all firmware options available for a kit
Then locate the 'iotprovision' bundled firmware
And program it into the MCU
    >>> from pykitcommander.kitmanager import KitApplicationFirmwareProvider
    >>> applications = KitApplicationFirmwareProvider(kitname=programmer.kit_info['kit_name'])
    >>> print (applications.kit_firmware)
    >>> application = applications.locate_firmware(firmware_identifier="iotprovision")
    >>> print(application['bundled_firmware'])
    >>> programmer.program_application(application['bundled_firmware'])

Now instantiate a protocol and communicate with the MCU
    >>> protocol = application['protocol_driver']()
    >>> protocol.open(port)
    >>> ecc_serial_number = protocol.read_ecc_serialnumber()
    >>> protocol.close()

"""
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
