from common.rc_code import RcCode
from src.base.linux_interface.fan_interface import FanInterface
from src.base.linux_interface.power_interface import PowerInterface
from src.base.linux_interface.temp_interface import TempInterface
from system_interface.os_interface import OsInterface


class lmSensor(FanInterface, PowerInterface, TempInterface):
    def __init__(self):
        self._os_interface_obj = OsInterface()

    def temp_get(self, sensors_name):
        rc, value = self._os_interface_obj.os_interface_exec_cmd("sensors | grep Package | awk '{print $4}'")
        if rc == RcCode.SUCCESS:
            return rc, float(value.replace("+", "").replace("°C", "").rstrip())
        return rc, 0