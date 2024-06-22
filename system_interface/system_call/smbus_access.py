from smbus2 import SMBus
from common.rc_code import RcCode


class SmbusAccess:
    def __init__(self, bus, i2c_addr):
        self._bus = bus
        self._i2c_addr = i2c_addr

    def smbus_read_byte_data(self, register: int, force: bool = False):
        """
        Read a single byte from a designated register.
        :param register: (int) – Start register
        :param force (Boolean) – Force to access I2C src
        :return: (tuple) Return code and (int) Read byte value
        """
        try:
            with SMBus(self._bus) as bus:
                rtn_val = bus.read_byte_data(self._i2c_addr, register, force)
        except IOError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, rtn_val

    def smbus_write_byte_data(self, register: int, value: int, force: bool = False):
        """
        Write a block of byte data to a given register.
        :param register: (int) – Start register
        :param value: (int) – Byte value to transmit
        :param force (Boolean) – Force to access I2C src
        :return: Return code
        """
        try:
            with SMBus(self._bus) as bus:
                bus.write_byte_data(self._i2c_addr, register, value, force)
        except IOError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def smbus_read_word_data(self, register: int, force: bool = False):
        """
        Read a single word (2 bytes) from a given register.
        :param register: (int) – Start register
        :param force (Boolean) – Force to access I2C src
        :return: (tuple) Return code and (int) 2-byte word
        """
        try:
            with SMBus(self._bus) as bus:
                rtn_val = bus.read_word_data(self._i2c_addr, register, force)
        except IOError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, rtn_val

    def smbus_write_word_data(self, register: int, value: int, force: bool = False):
        """
        Write a block of byte data to a given register.
        :param register: (int) – Start register
        :param value: (int) – Word value to transmit
        :param force (Boolean) – Force to access I2C src
        :return: Return code
        """
        try:
            with SMBus(self._bus) as bus:
                bus.write_word_data(self._i2c_addr, register, value, force)
        except IOError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def smbus_read_block_data(self, register: int, force: bool = False):
        """
        Read a block of up to 32-bytes from a given register.
        :param register: (int) – Start register
        :param force (Boolean) – Force to access I2C src
        :return: (tuple) Return code and (list) List of bytes
        """
        try:
            with SMBus(self._bus) as bus:
                rtn_val = bus.read_block_data(self._i2c_addr, register, force)
        except IOError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, rtn_val

    def smbus_write_block_data(self, register: int, value: list, force: bool = False):
        """
        Write a byte to a given register.
        :param register: (int) – Start register
        :param value: (list) – List of bytes
        :param force (Boolean) – Force to access I2C src
        :return: Return code
        """
        try:
            with SMBus(self._bus) as bus:
                bus.write_block_data(self._i2c_addr,
                                     register,
                                     [value[i] for i in range(len(value) if len(value) > 32 else 32)],
                                     force)
        except IOError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def smbus_read_i2c_block_data(self, register: int, length: int, force: bool = False):
        """
        Read a block of byte data from a given register.
        :param register: (int) – Start register
        :param length: (int) – Desired block length
        :param force (Boolean) – Force to access I2C src
        :return: (tuple) Return code and (list) List of bytes
        """
        try:
            with SMBus(self._bus) as bus:
                rtn_val = bus.read_i2c_block_data(self._i2c_addr, register, length, force)
        except IOError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, rtn_val

    def smbus_write_i2c_block_data(self, register: int, data: list, force: bool = False):
        """
        Write a block of byte data to a given register.
        :param register: (int) – Start register
        :param data: (list) – The list stores the data
        :param force (Boolean) – Force to access I2C src
        :return: Return code
        """
        try:
            with SMBus(self._bus) as bus:
                bus.write_i2c_block_data(self._i2c_addr,
                                     register,
                                     [x for x in data],
                                     force)
        except IOError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def smbus_read_sequence(self, register: int, input_len: int, force: bool = False):
        """
        Read a sequence of byte data from a given register.
        :param register: (int) – Start register
        :param input_len: (int) - The length of the data user wants to read
        :param force (Boolean) – Force to access I2C src
        :return: Return code
        """
        output_list = []
        try:
            with SMBus(self._bus) as bus:
                for i in range(0, input_len):
                    rtn_val = bus.read_byte_data(self._i2c_addr, register + i, force)
                    output_list.append(rtn_val)
        except IOError as e:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, output_list
