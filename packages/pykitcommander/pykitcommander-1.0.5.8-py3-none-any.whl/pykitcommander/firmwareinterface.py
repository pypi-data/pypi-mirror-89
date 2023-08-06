"""
Collection of firmware Serial-port-based communication interfaces

All implementations should inherit from ApplicationFirmwareInterface
This base class implements serial open and close, and can be used via
the KitSerialConnection context manager, for example:

    with KitSerialConnection(protocol, self.kitlink.port):
        # Read WINC fw version
        print("Querying current WINC firmware version")
        version_info = protocol.get_winc_fw_version()

This ensures port closure after use.

"""

from time import sleep
from logging import getLogger
from codecs import decode
from hexdump import hexdump
from pyedbglib.serialport.serialcdc import SerialCDC
from .kitcommandererrors import PortError, KitCommunicationError



class KitSerialConnection:
    """
    Context manager for serial connections
    Makes sure clients are always disconnecting when they are done

    :param protocol: ApplicationFirmwareInterface object
    :param port: port to connect to
    """

    def __init__(self, protocol, port):
        self.protocol = protocol
        self.port = port
    def __enter__(self):
        """ Enter: open port on protocol """
        self.protocol.open(self.port)
        return self.protocol.get_comport_handle()
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit: close port """
        self.protocol.close()

class ApplicationFirmwareInterface:
    """
    Base class for firmware interfaces
    Supports open, close, and get_comport_handle

    :param baud: baud rate
    :param dump: protocol verbose logging
    :param stopbits: number of stopbits to use
    """
    def __init__(self, baud, dump=False, stopbits=1):
        self.baud = baud
        self.dump = dump
        self.com = None
        self.stopbits = stopbits

    def open(self, port):
        """
        Open serial port using values set during constuction
        """
        self.com = SerialCDC(port, self.baud, timeout=10, stopbits=self.stopbits)

    def close(self):
        """
        Close serial port
        """
        self.com.close()
        self.com = None

    def get_comport_handle(self):
        """
        Get serial port handle
        :return: handle to serial port in use by this protocol
        """
        return self.com


class WincUpgradeFirmwareInterface(ApplicationFirmwareInterface):
    """
    Interface to WINC upgrade firmware
    """
    DEFAULT_BAUD = 115200
    def __init__(self, baud=DEFAULT_BAUD, dump=False):
        super().__init__(baud, dump=dump, stopbits=2)
        self.logger = getLogger(__name__)


class ProvisioningFirmwareInterface(ApplicationFirmwareInterface):
    """
    Interface to provisioning firmware

    Implementation of the provisioning firmware communication protocol.
    Commands and responses are 0-terminated strings as described below.

    Command syntax: <cmd>:[<arg>[,<arg>...]]

                    <arg> is hex-encoded blob

    Response: <hex> | "OK" | "ERROR:"<xxxx>
            <hex> is hex-encoded blob, <xxxx> 16-bit hex error code

    """

    # Time in seconds for WINC erase/write operations to complete
    # FIXME: Should be handled in FW?
    WINC_SETTLE_TIME = 1

    DEFAULT_BAUD = 115200

    def __init__(self, baud=DEFAULT_BAUD, dump=False):
        super().__init__(baud, dump=dump)
        self.logger = getLogger(__name__)

    def read_ecc_serialnumber(self):
        """
        Reads the ECC serialnumber
        :return: ECC serialnumber as string
        """
        self.logger.info("Read ecc serialnumber")
        return self.fw_request("<serNum")

    def read_ecc_slot(self, slot_number, num_bytes):
        """
        Read contents of a slot on the ECC
        :param slot_number: ECC slot to read from
        :param num_bytes: number of bytes to read
        :return: contents of slot
        """
        self.logger.info("Read %d bytes from ecc slot %d", num_bytes, slot_number)
        return self.fw_request("<readSlot:{0:d},{1:d}".format(slot_number, num_bytes))

    def read_signer_certificate(self):
        """
        Reads the signer certificate
        :return: signer certificate as string
        """
        self.logger.info("Request signer certificate")
        return self.fw_request("<signCert")

    def write_signer_certificate(self, signer_cert):
        """
        Writes the signer certificate
        :param signer_cert: signer certificate
        """
        self.logger.info("Write Signer Certificate")
        return self.fw_request(">caCert", [signer_cert])

    def read_device_certificate(self):
        """
        Reads the device certificate
        :return: device certificate as string
        """
        self.logger.info("Read device certificate")
        return self.fw_request("<devCert")

    def write_device_certificate(self, device_cert):
        """
        Writes the device certificate
        :param device_cert: device certificate
        """
        self.logger.info("Write Device Certificate")
        return self.fw_request(">devCert", [device_cert])

    def transfer_certificates(self, template):
        """
        Transfers certificate to the WINC
        :param device_cert: certificate template
        """
        self.logger.info("Transfer certificates to WINC")
        result = self.fw_request("xferCerts", [template])
        sleep(self.WINC_SETTLE_TIME)
        return result

    def write_thing_name(self, thing_name):
        """
        Write thing name to the WINC
        :param thing_name: thing name
        """
        self.logger.info("Write thing name to WINC")
        result = self.fw_request(">thingName", [thing_name])
        sleep(self.WINC_SETTLE_TIME)
        return result

    def write_endpoint_name(self, endpoint_name):
        """
        Write endpoint name to the WINC
        :param endpoint_name: endpoint name
        """
        self.logger.info("Write AWS endpoint in WINC")
        result = self.fw_request(">endPoint", [endpoint_name])
        sleep(self.WINC_SETTLE_TIME)
        return result

    def lock_ecc_slots_10_to_12(self):
        """
        Lock ECC slots 10 to 12
        """
        self.logger.info("Locking ECC slots 10-12")
        return self.fw_request("lock")

    def erase_tls_certificate_sector(self):
        """
        Erase TLS certificate sector in WINC
        """
        self.logger.info("Erase WINC TLS certificate sector")
        result = self.fw_request("wincErs")
        sleep(self.WINC_SETTLE_TIME)
        return result

    def read_public_key(self):
        """
        Reads the public key
        :return: public key as string
        """
        self.logger.info("Read device public key")
        return self.fw_request("<devKey")

    def sign_digest(self, digest):
        """
        Send a digest for signing by the ECC
        :param digest: digest to sign
        :return: signature of signed digest
        """
        self.logger.info("Sign digest")
        return self.fw_request("<devSign", [digest.hex()])


    def get_winc_fw_version(self):
        """
        Alias for read_
        """
        return self.read_winc_fw_version()


    def read_winc_fw_version(self):
        """
        Reads the FW version of the WINC module using provisioning FW
        :return: firmware version as string
        """
        self.logger.debug("Read WINC module FW version")
        response = self.fw_request("<wincFWVer")
        result = decode(response, "hex")
        self.logger.debug(result)
        return result

    def fw_request(self, cmd, args=None):
        """
        Send a request to the kit provisioning FW, receive response.

        Due to pyserial lacks explicit mechanism for detecting timeout,
        (like raising exception), a protocol workaround had to be found
        (non-empty positive response from FW)
        :param cmd: command to send to target
        :type cmd: str
        :param args: arguments to be added to the command being sent to target
        :type args: str
        :return: response from target
        :rtype: str
        :raises:
            PortError: If port has not been opened
            KitCommunicationError: If an unexpected response was received from target
        """
        if self.com is None:
            raise PortError("Port not open.")
        args = args or []
        buffer = ("{}:{}\0").format(cmd, ",".join(args)).encode()
        self.logger.debug("%s: length %d", cmd, len(buffer))
        self.com.write(buffer)
        response = self.com.read_until(b'\x00')[:-1].decode("utf-8")
        if response.startswith("OK"):  # Positive response without data
            return ""
        if response.startswith("ERROR"):
            raise KitCommunicationError("Target communication failed.  Firmware command '{}' returned: '{}'".format(cmd, response))
        if response:                 # Positive response with data
            if self.dump:
                hexdump(bytes.fromhex(response))
            return response

        raise KitCommunicationError("Target communication failed.  Timeout waiting for response from FW (cmd = '{}')".format(cmd))

class DemoFirmwareInterface(ApplicationFirmwareInterface):
    """
    Interface to demo firmware
    """
    DEFAULT_BAUD = 9600
    def __init__(self, baud=DEFAULT_BAUD, dump=False):
        super().__init__(baud, dump=dump)
        self.logger = getLogger(__name__)

    def open(self, port):
        """
        Open port, then send an initial empty command and discard the response (list of available commands).
        This reduces the risk of communication glitches on initial real command sent to demo FW.
        """
        super().open(port)
        _ = self.demo_fw_command("")

    # pylint: disable=dangerous-default-value
    def demo_fw_command(self, cmd, args=[]):
        """
        Send a request to demo FW CLI, return response.
        """
        if self.com is None:
            raise PortError("Port not open.")
        #TODO: refactor
        end_of_transmission = b'\\04'  # end of transmission from target
        buffer = ("{} {}\n").format(cmd, ",".join(args)).encode()
        sleep(0.1)     # Mystery delay between requests seems to avoid mixed-up responses
        # Experimental: Try to send a single character at a time to solve instability
        for c in buffer:
            buf = [c]
            self.com.write(buf)
            self.com.flush()
        response = self.com.read_until(end_of_transmission)[:-1].decode("utf-8", errors="ignore")
        return response
