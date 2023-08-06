"""
Helper functions for setting up simple applications
"""
from logging import getLogger
from pyedbglib.serialport.serialportmap import SerialPortMap

from .kitmanager import KitApplicationFirmwareProvider
from .kitmanager import KitProgrammer

def get_iot_provision_protocol(skip_programming=False, serialnumber=None):
    """
    Helper function for retrieving the provisioning protocol
    :param skip_programming: saves time if already programmed
    :param serialnumnber: selects specific kit by its USB serial number
    """
    return get_protocol("iotprovision", skip_programming, serialnumber)

def get_protocol(protocol_name, skip_programming=False, serialnumber=None):
    """
    Helper function for retrieving a protocol
    :param protocol_name: name of the protocol to find
    :param skip_programming: saves time if already programmed
    :param serialnumnber: selects specific kit by its USB serial number
    """
    logger = getLogger(__name__)
    programmer = KitProgrammer(serialnumber=serialnumber)

    # Look up available applications for this kit
    applications = KitApplicationFirmwareProvider(kitname=programmer.kit_info['kit_name'])
    # Request iotprovision application
    application = applications.locate_firmware(firmware_identifier=protocol_name)
    # Create the protocol object for this application
    protocol = application['protocol_driver']()

    # Make an educated port guess for the client
    serialnumber = programmer.kit_info['serialnumber']
    portmapper = SerialPortMap()
    port = portmapper.find_serial_port(serialnumber)

    if skip_programming:
        programmer.reset_target()       # Make sure firmware is in known state
    else:
        programmer.program_application(application['bundled_firmware'])

    # Return protocol object and port
    logger.info("Created protocol for '%s' on '%s'", protocol_name, programmer.kit_info['kit_name'])
    return protocol, port
