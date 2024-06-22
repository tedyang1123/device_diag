from common.rc_code import RcCode
from system_interface.os_interface import OsInterface


class OsCore:
    def __init__(self):
        self._obj = OsInterface()

    def os_core_init(self):
        return RcCode.SUCCESS, None

    def os_core_linux_version_get(self):
        rc, linux_version = self._obj.os_interface_exec_cmd("uname -a")
        if rc == RcCode.SUCCESS:
            return RcCode.SUCCESS, {"linux_version": linux_version.strip()}
        else:
            return RcCode.FAILURE, None