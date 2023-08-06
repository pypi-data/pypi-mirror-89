from .x1000_base import SenseX1000Base
from .x1000_scpi import SenseX1000ScpiDevice


class SenseX1000(SenseX1000Base):
    @classmethod
    def open_device(cls, resource):
        # Use as a factory function
        # As of this time, only scpi is supported
        return SenseX1000ScpiDevice(resource)

    @classmethod
    def find_devices(cls):
        # As of this time we only search for Scpi devices
        # TODO: Implement resource class for devices with resource type
        scpi_devices = SenseX1000ScpiDevice.find_devices()
        return scpi_devices
