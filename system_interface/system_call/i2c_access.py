from common.rc_code import RcCode
from system_interface.system_call.os_tool import OsTool


class I2cAccess:
    def __init__(self, bus, i2c_addr):
        self._bus = bus
        self._i2c_addr = i2c_addr
        self._os_tool = OsTool()

    def i2c_access_read_byte(self, register, force=False) -> tuple:
        force_cmd = "-f " if force else ""
        cmd = ("i2cget -y " + force_cmd +
               str(self._bus) + " " + str(self._i2c_addr) + " " + str(register))
        rc, data = self._os_tool.os_tool_exec_cmd(cmd)
        if rc == RcCode.SUCCESS:
            return rc, int(data, 16)
        else:
            return rc, None

    def i2c_access_write_byte(self, register, data, force=False) -> RcCode:
        force_cmd = "-f " if force else ""
        cmd = ("i2cset -y " + force_cmd +
               str(self._bus) + " " + str(self._i2c_addr) + " " + str(register) + " " + str(data))
        rc, _ = self._os_tool.os_tool_exec_cmd(cmd)
        return rc

    def i2c_access_read_word(self, register, force=False) -> tuple:
        force_cmd = "-f " if force else ""
        cmd = ("i2cget -y " + force_cmd +
               str(self._bus) + " " + str(self._i2c_addr) + " " + str(register)) + " w"
        rc, data = self._os_tool.os_tool_exec_cmd(cmd)
        if rc == RcCode.SUCCESS:
            return rc, int(data, 16)
        else:
            return rc, None

    def i2c_access_write_word(self, register, data, force=False) -> RcCode:
        force_cmd = "-f " if force else ""
        cmd = ("i2cset -y " + force_cmd +
               str(self._bus) + " " + str(self._i2c_addr) + " " + str(register) + " " + str(data)) + " w"
        rc, _ = self._os_tool.os_tool_exec_cmd(cmd)
        return rc

    def i2c_access_read_block(self, register, force=False) -> tuple:
        force_cmd = "-f " if force else ""
        cmd = "i2cdump -y " + force_cmd + str(self._bus) + " " + str(self._i2c_addr) + " s " + str(register)
        rc, data = self._os_tool.os_tool_exec_cmd(cmd)
        output_list = []
        line_list = self._os_tool.os_tool_exec_cmd(cmd)
        line_len = len(line_list)
        if line_len > 1:
            for line_no in range(1, line_len):
                val_list = line_list[line_no].split(' ')
                for i in range(1, len(val_list)):
                    if val_list[i] == '':
                        break
                    else:
                        output_list.append(val_list[i])
        return rc, output_list

    def i2c_access_write_block(self, register, data, force=False) -> RcCode:
        force_cmd = "-f " if force else ""
        cmd = "i2cset -y " + force_cmd + str(self._bus) + " " + str(self._i2c_addr) + " " + str(register) + " "
        for _, data in enumerate(data):
            cmd += str(data)
            cmd += " "
        cmd += "i"
        rc, _ = self._os_tool.os_tool_exec_cmd(cmd)
        return rc
