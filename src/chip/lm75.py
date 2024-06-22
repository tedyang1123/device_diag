import os

from common.rc_code import RcCode
from src.base.linux_interface.temp_interface import TempInterface
from system_interface.driver_interface import DriverInterface
from system_interface.i2c_interface import I2cInterface
from system_interface.ipmi_interface import IpmiI2cInterface
from system_interface.os_interface import OsInterface
from system_interface.smbus_interface import SmbusInterface


def _temp_reg_to_mc(reg_val: int, resolution: int):
    """
    Translate temperature value
    """
    return ((reg_val >> (16 - resolution)) * 1000) >> (resolution - 8)


class Tmp75Smbus(TempInterface, SmbusInterface):
    def __init__(self, bus, addr):
        TempInterface.__init__(self)
        SmbusInterface.__init__(self, bus, addr)

    def temp_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_read_word_data(0x0)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0

    def temp_max_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_write_word_data(0x3)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0


class Tmp75I2c(TempInterface, I2cInterface):
    def __init__(self, bus, addr):
        TempInterface.__init__(self)
        I2cInterface.__init__(self, bus, addr)

    def temp_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_read_word(0x0)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0

    def temp_max_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_write_word(0x3)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0


class Tmp75Ipmi(TempInterface, IpmiI2cInterface):
    def __init__(self, bus, addr):
        TempInterface.__init__(self)
        IpmiI2cInterface.__init__(self, bus, addr)

    def temp_get(self, index=1) -> tuple:
        rc, val = self.ipmi_i2c_read_word(0x0)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0

    def temp_max_get(self, index=1) -> tuple:
        rc, val = self.ipmi_i2c_write_word(0x3)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, _temp_reg_to_mc(val, 12)
        else:
            return RcCode.FAILURE, 0


class Tmp75Driver(TempInterface, DriverInterface):
    def __init__(self, bus, addr):
        self._bus = bus
        self._addr = addr
        TempInterface.__init__(self)
        DriverInterface.__init__(self, "/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=bus, addr=addr))

    def temp_int(self):
        rc, msg = RcCode.SUCCESS, None
        if not os.path.isdir("/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=self._bus,addr=self._addr)):
            os_interface_obj = OsInterface()
            rc, msg = os_interface_obj.os_interface_exec_cmd(
                "echo temp75 0x{addr:02x} > /sys/bus/i2c/devices/i2c={bus}".format(bus=self._bus,addr=self._addr))
        return rc. msg

    def temp_get(self, index=1) -> tuple:
        return self.driver_read(self.temp.format(index))

    def temp_max_get(self, index=1) -> tuple:
        return self.driver_read(self.temp_max.format(index))

    def temp_label_get(self, index=1):
        return self.driver_read(self.temp_label.format(index))
