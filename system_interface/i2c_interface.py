from common.rc_code import RcCode
from system_interface.system_call.i2c_access import I2cAccess


class I2cInterface:
    def __init__(self, bus: int, addr: int):
        self._i2c_obj = I2cAccess(bus, addr)

    def i2c_interface_read_byte(self, register: int, force: bool = False) -> tuple:
        return self._i2c_obj.i2c_access_read_byte(register, force)

    def i2c_interface_write_byte(self, register: int, data, force: bool = False) -> RcCode:
        return self._i2c_obj.i2c_access_write_byte(register, data, force)

    def i2c_interface_read_word(self, register: int, force: bool = False) -> tuple:
        return self._i2c_obj.i2c_access_read_word(register, force)

    def i2c_interface_write_word(self, register: int, data, force: bool = False) -> RcCode:
        return self._i2c_obj.i2c_access_write_word(register, data, force)

    def i2c_interface_read_block(self, register: int, force: bool = False) -> tuple:
        return self._i2c_obj.i2c_access_read_block(register, force)

    def i2c_interface_write_block(self, register: int, data, force: bool = False) -> RcCode:
        return self._i2c_obj.i2c_access_write_block(register, data, force)
