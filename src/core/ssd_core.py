import sys

from common.rc_code import RcCode


class SsdCore:
    def __init__(self, **args):
        self._obj = None
        self._obj = getattr(sys.modules[__name__], args["access_type"].capitalize())(args["host_node"])

    def ssd_core_init(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_init()

    def ssd_core_vendor_get(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_vendor_get()

    def ssd_capacity_get(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_capacity_get()

    def ssd_size_get(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_size_get()

    def ssd_sector_size_get(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_sector_size_get()

    def ssd_dev_reference_get(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.ssd_dev_reference_get()