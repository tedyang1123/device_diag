import os

from common.rc_code import RcCode
from src.base.linux_interface.temp_interface import TempInterface
from system_interface.driver_interface import DriverInterface
from system_interface.i2c_interface import I2cInterface
from system_interface.os_interface import OsInterface
from system_interface.smbus_interface import SmbusInterface


def jc42_temp_from_reg(reg_value):
    msb = (reg_value & 0xFF) << 8
    lsb = (reg_value & 0xFF00) >> 8
    dimm = msb | lsb
    dimm = (dimm & 0x1FFF) >> 2
    temp = dimm * 0.25
    return temp


class Jc42Smbus(SmbusInterface, TempInterface):
    def __init__(self, bus, addr):
        SmbusInterface.__init__(self, bus, addr)
        TempInterface.__init__(self)

    def temp_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_read_byte_data(0x5)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_min_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_read_byte_data(0x3)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_max_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_read_byte_data(0x2)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_max_crit_get(self, index=1) -> tuple:
        rc, val = self.smbus_interface_read_byte_data(0x4)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0


class Jc42I2c(I2cInterface, TempInterface):
    def __init__(self, bus, addr):
        I2cInterface.__init__(self, bus, addr)
        TempInterface.__init__(self)

    def temp_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_read_byte(0x5)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_min_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_read_byte(0x3)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_max_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_read_byte(0x2)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0

    def temp_max_crit_get(self, index=1) -> tuple:
        rc, val = self.i2c_interface_read_byte(0x4)
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, jc42_temp_from_reg(val)
        else:
            return RcCode.FAILURE, 0


class Jc42Driver(DriverInterface, TempInterface):
    def __init__(self, bus, addr):
        self._bus = bus
        self._addr = addr
        DriverInterface.__init__(self, "/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=bus, addr=addr))
        TempInterface.__init__(self)

    def temp_int(self):
        rc, msg = RcCode.SUCCESS, None
        if not os.path.isdir("/sys/bus/i2c/devices/i2c={bus}/{bus}-00{addr}".format(bus=self._bus,addr=self._addr)):
            os_interface_obj = OsInterface()
            rc, msg = os_interface_obj.os_interface_exec_cmd(
                "echo jc42 0x{addr:02x} > /sys/bus/i2c/devices/i2c={bus}".format(bus=self._bus,addr=self._addr))
        return rc. msg

    def temp_get(self, index=1) -> tuple:
        return self.driver_read(self.temp.format(index))

    def temp_min_get(self, index=1) -> tuple:
        return self.driver_read(self.temp_min.format(index))

    def temp_max_get(self, index=1) -> tuple:
        return self.driver_read(self.temp_max.format(index))

    def temp_max_crit_get(self, index=1) -> tuple:
        return self.driver_read(self.temp_crit.format(index))

    def temp_label_get(self, index=1):
        return self.driver_read(self.temp_label.format(index))
