import time

from common.rc_code import RcCode
from system_interface.os_interface import OsInterface


class IpmiAccess:
    def __init__(self, bus=None, i2c_addr=None):
        self._bus = bus
        self._i2c_addr = i2c_addr << 1
        self._ipmi_i2c_read_cmd = "ipmitool raw 0x30 0x25 {bus} {addr} {size} {offset}"
        self._ipmi_i2c_write_cmd = "ipmitool raw 0x30 0x25 {bus} {addr} 0 {offset} {value}"
        self._os_boj = OsInterface()

    def _ipmi_raw_cmd_read(self,command):
        int_list = []
        rc, data = self._os_boj.os_interface_exec_cmd(command)
        if rc == RcCode.SUCCESS:
            line_list = data.split("\n")
            for line in line_list:
                line = line.rstrip()
                if line != "":
                    hex_list = line.strip().split(" ")
                    for hex_num in hex_list:
                        int_list.append(int(hex_num, 16))
            return rc, int_list
        return RcCode.FAILURE, None

    def _ipmi_raw_cmd_write(self,command):
        return self._os_boj.os_interface_exec_cmd(command)

    def ipmi_access_read_byte(self, register: int):
        cmd = self._ipmi_i2c_read_cmd.format(bus=self._bus, addr=self._i2c_addr, offset=register, size=1)
        rc, data = self._ipmi_raw_cmd_read(cmd)
        if rc != RcCode.SUCCESS:
            return rc, None
        return rc, data[0]

    def ipmi_access_write_byte(self, register: int, value: int):
        cmd = self._ipmi_i2c_write_cmd.format(bus=self._bus, addr=self._i2c_addr, size=0, offset=register, value=value)
        return self._ipmi_raw_cmd_write(cmd)

    def ipmi_access_read_word(self, register: int):
        cmd = self._ipmi_i2c_read_cmd.format(bus=self._bus, addr=self._i2c_addr, offset=register, size=1)
        rc, data = self._ipmi_raw_cmd_read(cmd)
        if rc != RcCode.SUCCESS:
            return rc, None
        return rc, (data[1] << 8) + data[0] if len(data) == 2 else data[0]

    def ipmi_access_write_word(self, register: int, value: int):
        int_list = [(value & 0xFF00) >> 8, value & 0xFF]
        cmd = self._ipmi_i2c_write_cmd.format(bus=self._bus, addr=self._i2c_addr, size=0, offset=register, value=int_list)
        return self._ipmi_raw_cmd_write(cmd)

    def ipmi_access_read_block(self, register: int):
        cmd = self._ipmi_i2c_read_cmd.format(bus=self._bus, addr=self._i2c_addr, offset=register, size=32)
        rc, data = self._ipmi_raw_cmd_read(cmd)
        if rc != RcCode.SUCCESS:
            return rc, None
        value = []
        for i in data:
            value.append(bytes(data[i]))
        return rc, value

    def ipmi_access_write_block(self, register: int, value: list):
        int_list = []
        for i in value:
            int_list.append(int.from_bytes(value[i], "big"))
        cmd = self._ipmi_i2c_write_cmd.format(bus=self._bus, addr=self._i2c_addr, size=0, offset=register, value=int_list)
        return self._ipmi_raw_cmd_write(cmd)

    def ipmi_access_process_raw_cmd(self, cmd, data=None):
        rc, result = self._os_boj.os_interface_exec_cmd(cmd)
        time.sleep(0.1)
        val = None
        if rc == RcCode.SUCCESS:
            if data and "type" in data:
                result = result.replace("\r", "").replace("\n", " ")
                if data["type"] == "value":
                    val = 0
                    str_list = result.strip().split(" ")
                    for i in reversed(str_list):
                        val = val << 8
                        val = val + int(i, 16)
                    if "scale" in data:
                        val = val * data["scale"]
                elif data["type"] == "ascii":
                    str_data = result.replace(" ", "")
                    val = "{:s}".format(bytes.fromhex(str_data).decode("ascii"))
                elif data["type"] == "list":
                    val = []
                    str_list = result.strip().split(" ")
                    for i in str_list:
                        val.append(int(i, 16))
        else:
            return RcCode.FAILURE, None
        return rc, val

    def ipmi_access_sensor_read(self, sensor):
        cmd = "ipmitool sensor reading {sensor}".format(sensor=sensor)
        rc, result = self._os_boj.os_interface_exec_cmd(cmd)
        time.sleep(0.1)
        val = None
        if rc == RcCode.SUCCESS:
            str_list = result.strip().split("|")
            if len(str_list) < 0:
                return RcCode.INVALID_VALUE, None
            if str_list[0].strip() == sensor:
                val = float(str_list[1].strip())
            else:
                return RcCode.DATA_NOT_FOUND, None
        return rc, val
