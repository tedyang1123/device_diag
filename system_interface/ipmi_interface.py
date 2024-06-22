from common.rc_code import RcCode
from system_interface.system_call.ipmi_access import IpmiAccess


class IpmiI2cInterface:
    def __init__(self, bus: int, addr: int):
        self._ipmi_obj = IpmiAccess(bus, addr)

    def ipmi_i2c_read_byte(self, register: int) -> tuple:
        return self._ipmi_obj.ipmi_access_read_byte(register)

    def ipmi_i2c_write_byte(self, register: int, value: int) -> RcCode:
        return self._ipmi_obj.ipmi_access_read_byte(register, value)

    def ipmi_i2c_read_word(self, register: int) -> tuple:
        return self._ipmi_obj.ipmi_access_read_word(register)

    def ipmi_i2c_write_word(self, register: int, value: int) -> RcCode:
        return self._ipmi_obj.ipmi_access_write_word(register, value)

    def ipmi_i2c_read_block(self, register: int) -> tuple:
        return self._ipmi_obj.ipmi_access_read_block(register)

    def ipmi_i2c_write_block(self, register: int, value: list) -> RcCode:
        return self._ipmi_obj.ipmi_access_write_block(register, value)


class IpmiOemCmdInterface:
    def __init__(self):
        self._ipmi_obj = IpmiAccess()

    def ipmi_oem_cmd_exec(self, net_fun: int, cmd: int, data_format: dict):
        pass
    # TBD


class IpmiCmdInterface:
    def __init__(self):
        self._ipmi_obj = IpmiAccess()

    def ipmi_cmd_exec_sensor_red(self, sensor: str) -> tuple:
        return self._ipmi_obj.ipmi_access_sensor_read(sensor)
