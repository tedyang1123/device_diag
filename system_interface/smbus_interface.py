from system_interface.system_call.smbus_access import SmbusAccess


class SmbusInterface:
    def __init__(self, bus: int, addr: int):
        self._bus = bus
        self._addr = addr
        self._smbus_obj = SmbusAccess(bus, addr)

    def smbus_interface_read_byte_data(self, register: int, force: bool = False):
        return self._smbus_obj.smbus_read_byte_data(register, force)

    def smbus_interface_write_byte_data(self, register: int, value: int, force: bool = False):
        return self._smbus_obj.smbus_write_byte_data(register, value, force)

    def smbus_interface_read_word_data(self, register: int, force=False):
        return self._smbus_obj.smbus_read_word_data(register, force)

    def smbus_interface_write_word_data(self, register: int, value: int, force: bool = False):
        return self._smbus_obj.smbus_write_word_data(register, value, force)

    def smbus_interface_read_block_data(self, register: int, force=False):
        return self._smbus_obj.smbus_read_block_data(register, force)

    def smbus_interface_write_block_data(self, register: int, value: list, force: bool = False):
        return self._smbus_obj.smbus_write_block_data(register, value, force)

    def smbus_interface_read_i2c_block_data(self, register: int, length: int, force: bool = False):
        return self._smbus_obj.smbus_read_i2c_block_data(register, length, force)

    def smbus_interface_write_i2c_block_data(self, register: int, value: list, force: bool = False):
        return self._smbus_obj.smbus_write_i2c_block_data(register, value, force)

    def smbus_interface_read_sequence(self, register: int, input_len: int, force: bool = False):
        return self._smbus_obj.smbus_read_sequence(register, input_len, force)
