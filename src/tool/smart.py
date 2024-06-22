from common.rc_code import RcCode
from pySMART import Device

from src.base.linux_interface.ssd_interface import SsdInterface
from src.base.linux_interface.temp_interface import TempInterface


class Smart(TempInterface, SsdInterface):
    def __init__(self, host_node):
        TempInterface.__init__(self)
        SsdInterface.__init__(self)
        self._host_node = host_node

    def ssd_vendor_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.device()

    def ssd_capacity_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.capacity()

    def ssd_size_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.size()

    def ssd_sector_size_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.sector_size()

    def ssd_dev_reference_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.dev_reference()

    def temp_get(self):
        try:
            device = Device(self._host_node)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, device.temperature()
