import os

from common.rc_code import RcCode
from src.base.linux_interface.temp_interface import TempInterface
from system_interface.driver_interface import DriverInterface


class CoreTemp(TempInterface, DriverInterface):
    def __init__(self):
        TempInterface.__init__(self)
        DriverInterface.__init__(self, "/sys/class/hwmon/hwmon0/")

    def temp_int(self):
        if not os.path.isdir("/sys/class/hwmon/hwmon0/"):
            return RcCode.FAILURE, "CoreTemp Driver is not load in the system."
        return RcCode.SUCCESS, None

    def temp_get(self, index=1) -> tuple:
        return self.driver_read("temp1_input")

    def temp_max_get(self, index=1) -> tuple:
        return self.driver_read(self.temp_max.format(index))

    def temp_label_get(self, index=1):
        return self.driver_read(self.temp_label.format(index))
