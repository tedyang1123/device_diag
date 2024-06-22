from system_interface.system_call.os_tool import OsTool


class OsInterface:
    def __init__(self):
        self._os_tool_obj = OsTool()

    def os_interface_exec_cmd(self, cmd, shell=False):
        return self._os_tool_obj.os_tool_exec_cmd(cmd, shell)
