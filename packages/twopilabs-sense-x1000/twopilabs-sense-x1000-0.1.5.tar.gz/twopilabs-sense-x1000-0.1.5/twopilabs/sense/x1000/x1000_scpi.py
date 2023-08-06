from twopilabs.utils.scpi import ScpiDevice
from .scpi_core import ScpiCore
from .scpi_system import ScpiSystem
from .scpi_control import ScpiControl
from .scpi_sense import ScpiSense
from .scpi_calc import ScpiCalc
from .scpi_trigger import ScpiTrigger
from .scpi_initiate import ScpiInitiate
from .x1000_base import SenseX1000Base

class SenseX1000ScpiDevice(ScpiDevice):
    def __init__(self, resource: str):
        ScpiDevice.__init__(self, resource)
        self.core       = ScpiCore(self)
        self.system     = ScpiSystem(self)
        self.control    = ScpiControl(self)
        self.sense      = ScpiSense(self)
        self.calc       = ScpiCalc(self)
        self.trigger    = ScpiTrigger(self)
        self.initiate   = ScpiInitiate(self)

    @classmethod
    def find_devices(cls):
        from twopilabs.utils.scpi import ScpiSerialTransport
        regexp = "({0:04x}:{1:04x})|({0:04X}:{1:04X})".format(
            SenseX1000Base.USB_VID, SenseX1000Base.USB_PID)
        return ScpiSerialTransport.find_devices(regexp=regexp)
