import os
import struct

from common.rc_code import RcCode
from src.base.linux_interface.eeprom_interface import EepromInterface
from system_interface.driver_interface import DriverInterface
from system_interface.os_interface import OsInterface
from system_interface.smbus_interface import SmbusInterface
from system_interface.i2c_interface import I2cInterface


class At24c02Smbus(EepromInterface, SmbusInterface):
    def __init__(self, bus, addr):
        SmbusInterface.__init__(self, bus, addr)
        EepromInterface.__init__(self)

    def eeprom_read(self, offset: int) ->tuple:
        rc, val = self.smbus_interface_read_byte_data(offset)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, val
        else:
            return RcCode.FAILURE, 0

    def eeprom_write(self, offset: int, value: int) ->RcCode:
        rc = self.smbus_interface_write_byte_data(offset, value)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS
        else:
            return RcCode.FAILURE


class At24c02I2c(EepromInterface, I2cInterface):
    def __init__(self, bus, addr):
        I2cInterface.__init__(self, bus, addr)
        EepromInterface.__init__(self)

    def eeprom_read(self, offset: int) ->tuple:
        rc, val = self.i2c_interface_read_byte(offset)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, val
        else:
            return RcCode.FAILURE, 0

    def eeprom_write(self, offset: int, value: int) ->RcCode:
        rc = self.i2c_interface_write_byte(offset, value)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS
        else:
            return RcCode.FAILURE


class At24c02Driver(EepromInterface, DriverInterface):
    def __init__(self, bus, addr):
        self._bus = bus
        self._addr = addr
        EepromInterface.__init__(self)
        DriverInterface.__init__(self, "/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=bus, addr=addr))

    def eeprom_int(self):
        rc, msg = RcCode.SUCCESS, None
        if not os.path.isdir("/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=self._bus,addr=self._addr)):
            os_interface_obj = OsInterface()
            rc, msg = os_interface_obj.os_interface_exec_cmd(
                "echo 24c02 0x{addr:02x} > /sys/bus/i2c/devices/i2c={bus}".format(bus=self._bus,addr=self._addr))
        return rc. msg

    def eeprom_read(self, offset: int) ->tuple:
        rc, value = self.driver_bin_read("eeprom", offset, 1)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, struct.unpack("B", value)
        else:
            return RcCode.FAILURE, 0

    def eeprom_write(self, offset: int, value: int) ->RcCode:
        rc = self.driver_bin_write("eeprom", offset, 1, bytearray(struct.pack("B", value)))
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS
        else:
            return RcCode.FAILURE