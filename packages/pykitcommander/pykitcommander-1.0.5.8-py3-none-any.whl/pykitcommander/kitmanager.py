"""
Kit state management functions
"""

import os
from logging import getLogger
from time import sleep
from .programmer import PymcuprogProgrammer
from .firmwareinterface import ProvisioningFirmwareInterface
from .firmwareinterface import WincUpgradeFirmwareInterface
from .firmwareinterface import DemoFirmwareInterface
from .kitcommandererrors import KitConnectionError

# InstallDir gives access to bundled FW hexfiles
INSTALLDIR = os.path.abspath(os.path.dirname(__file__))

# Firmware bundled/pointers
AVRIOT_PROVISION_FW = {
    'description' : "provisioning firmware for AVR-IOT running on ATmega4808",
    'bundled_firmware' : "fw/avr/atmega4808-iot-provision.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : ProvisioningFirmwareInterface,
    'protocol_baud' : ProvisioningFirmwareInterface.DEFAULT_BAUD
}

PICIOT_PROVISION_FW = {
    'description' : "provisioning firmware for PIC-IOT running on PIC24FJ128GA205",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-iot-provision.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : ProvisioningFirmwareInterface,
    'protocol_baud' : ProvisioningFirmwareInterface.DEFAULT_BAUD
}


AVRIOT_AWS_DEMO_FW = {
    'description' : "",
    'bundled_firmware' : "fw/avr/atmega4808-aws-iot-demo.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : DemoFirmwareInterface,
}

AVRIOT_GOOGLE_DEMO_FW = {
    'description' : "",
    'bundled_firmware' : "fw/avr/atmega4808-google-iot-demo.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : DemoFirmwareInterface,
}


PICIOT_AWS_DEMO_FW = {
    'description' : "",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-aws-iot-demo.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : DemoFirmwareInterface,
}

PICIOT_GOOGLE_DEMO_FW = {
    'description' : "",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-google-iot-demo.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : DemoFirmwareInterface,
}


AVRIOT_WINCUPGRADE_FW = {
    'description' : "",
    'bundled_firmware' : "fw/avr/atmega4808-iot-winc-upgrade.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : WincUpgradeFirmwareInterface,
    'protocol_baud' : WincUpgradeFirmwareInterface.DEFAULT_BAUD
}

PICIOT_WINCUPGRADE_FW = {
    'description' : "",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-iot-winc-upgrade.hex",
    'artifactory_firmware' : None,
    'github_firmware' : None,
    'protocol_driver' : WincUpgradeFirmwareInterface,
    'protocol_baud' : WincUpgradeFirmwareInterface.DEFAULT_BAUD
}

AVRIOT_FW_FUNCTIONS = {
    'iotprovision' : AVRIOT_PROVISION_FW,
    'iotprovision-aws' : AVRIOT_PROVISION_FW,
    'iotprovision-google' : AVRIOT_PROVISION_FW,
    'iotprovision-azure' : AVRIOT_PROVISION_FW,
    'wincupgrade' : AVRIOT_WINCUPGRADE_FW,
    'demo-aws' : AVRIOT_AWS_DEMO_FW,
    'demo-google' : AVRIOT_GOOGLE_DEMO_FW,
}


PICIOT_FW_FUNCTIONS = {
    'iotprovision' : PICIOT_PROVISION_FW,
    'iotprovision-aws' : PICIOT_PROVISION_FW,
    'iotprovision-google' : PICIOT_PROVISION_FW,
    'iotprovision-azure' : PICIOT_PROVISION_FW,
    'wincupgrade' : PICIOT_WINCUPGRADE_FW,
    'demo-aws' : PICIOT_AWS_DEMO_FW,
    'demo-google' : PICIOT_GOOGLE_DEMO_FW,
}

AVR_IOT_KIT = {
    'kit_names' : ['avr-iot wg', 'avr-iot wa'],
    'firmware' : AVRIOT_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'avr',
    'device' : 'atmega4808',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog'
}

PIC_IOT_KIT = {
    'kit_names' : ['pic-iot wg', 'pic-iot wa'],
    'firmware' : PICIOT_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'pic',
    'device' : 'pic24fj128ga705',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog'
}


SUPPORTED_KITS = [AVR_IOT_KIT, PIC_IOT_KIT]

# FIXME: Startup time should probably be specified per application,
# or better, readiness should be signaled by application (eg "READY" message)
FW_STARTUP_TIME = 1.5    # Startup time for FW after programming/target reset

class KitApplicationFirmwareProvider():
    """
    Finds applications based on required functionality, device/board and 'cloud provider'
    TODO: Could well be a simple function instead of a class
    Looks in:
    - bundled folders
    - Artefactory (internal) (todo)
    - GitHub (todo)

    """
    def __init__(self, kitname, hexfile_path=INSTALLDIR):
        self.logger = getLogger(__name__)
        self.hexfile_path = hexfile_path
        supported_kits = []
        target_kit_name = kitname.lower()
        self.logger.info("Looking for kit matching '%s'", target_kit_name)
        for supported_kit in SUPPORTED_KITS:
            if  target_kit_name in supported_kit['kit_names']:
                supported_kits.append(supported_kit)

        if len(supported_kits) > 1:
            raise KitConnectionError(msg="Too many compatible kits defined", value=supported_kits)

        self.kit_firmware = supported_kits[0]

    def locate_firmware(self, firmware_identifier):
        """
        Looks up and returns firmware for a given identifier
        :param firmware_identifier: unique ID of firmware
        """
        if firmware_identifier in self.kit_firmware['firmware'].keys():
            self.kit_firmware['firmware'][firmware_identifier]['bundled_firmware'] = os.path.normpath(os.path.join(self.hexfile_path, self.kit_firmware['firmware'][firmware_identifier]['bundled_firmware']))
            self.logger.info("Locating firmware for '%s'", firmware_identifier)
            return self.kit_firmware['firmware'][firmware_identifier]
        self.logger.error("Unable to locate firmware for '%s'", firmware_identifier)
        return ''


class KitProgrammer():
    """
    Programming applications onto kits
    """
    def __init__(self, serialnumber=None):
        self.last_used = None
        self.logger = getLogger(__name__)
        self.logger.info("Connecting to kit...")
        self.programmer = PymcuprogProgrammer(serialnumber=serialnumber, dfp_path=os.path.join(INSTALLDIR, "picpack"))
        kits = self.programmer.get_usable_kits()
        if len(kits) == 0:
            raise KitConnectionError(msg="Kit not found", value=kits)
        if len(kits) > 1:
            raise KitConnectionError(msg="Too many kits available (specific USB serial number required)", value=kits)

        # Only one at this point.
        kit = kits[0]
        serialnumber = kit['serial']
        kitname = self.programmer.read_kit_info('KITNAME').strip("\0")
        self.logger.info("Connected to kit '%s' (%s)", kitname, serialnumber)

        # Store kit info
        self.kit_info = {
            'serialnumber': serialnumber,
            'install_dir' : INSTALLDIR,
            'device_name' : kit['device_name'].lower(),
            'programmer_name' : kit['product'],
            'programmer_id' : kit['product'].split(' ')[0].lower(),
            'kit_name' : kitname
        }

    def program_application(self, hexfile, strategy='cached'):
        """
        Programs an application into the kit
        :param hexfile: hex file to program
        :param strategy: use caching, or other special mode
        """
        if strategy == "cached":
            if self.last_used == hexfile:
                self.logger.info("Skipping programming as application is cached")
                return
        self.programmer.program_hexfile(filename=hexfile)
        sleep(FW_STARTUP_TIME)

    def reset_target(self):
        """
        Resets the target
        """
        self.programmer.reset_target()
        sleep(FW_STARTUP_TIME)

    def erase(self):
        """
        Erases the target
        """
        self.programmer.erase_target_device()
        self.last_used = None

    def reboot(self):
        """
        Reboots the debugger
        """
        self.programmer.reboot()
        # TODO - is it usable after this?

    def get_kit_info(self):
        """
        Retrieves kit info dict
        """
        return self.kit_info
