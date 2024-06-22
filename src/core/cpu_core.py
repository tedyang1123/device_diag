import psutil

from dmidecode import DMIDecode
from common.rc_code import RcCode


class CpuCore:
    def __init__(self):
        pass

    def cpu_core_init(self):
        return RcCode.SUCCESS, None

    def cpu_core_info_get(self):
        dmi = DMIDecode()
        cpu_version = dmi.cpu_type()
        if cpu_version is not None:
            return RcCode.SUCCESS, cpu_version
        else:
            return RcCode.FAILURE, None

    def cpu_core_utilization_get(self):
        cpu_util = psutil.cpu_percent(1, percpu=True)
        if cpu_util != 0:
            return RcCode.SUCCESS, cpu_util
        else:
            return RcCode.FAILURE, None
