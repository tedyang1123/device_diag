import sys
from common.rc_code import RcCode


class TempCore:
    def __init__(self, **args):
        self._obj = None
        chip_name = args["chip_name"]
        if chip_name == "i2c":
            self._obj = getattr(
                sys.modules[__name__],
                chip_name.capitalize() + args["access_type"].capitalize())(args["i2c_bus"], args["i2c_addr"])
        elif chip_name == "smart":
            self._obj = getattr(
                sys.modules[__name__],
                chip_name.capitalize() + args["access_type"].capitalize())(args["host_node"])
        self._num_of_item = 1 if "num_of_item" not in args else args["num_of_item"]

    def temp_core_init(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_int()

    def temp_core_temp_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_get(index)

    def temp_core_temp_max_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_max_get(index)

    def temp_core_temp_max_set(self, temp, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_max_set(temp, index)

    def temp_core_temp_max_crit_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_max_crit_get(index)

    def temp_core_temp_min_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_min_get(index)

    def temp_core_temp_min_set(self, temp, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_min_set(temp, index)

    def temp_core_temp_min_crit_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_min_crit_get(index)

    def temp_core_temp_max_hyst_get(self, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_max_hyst_get(index)

    def temp_core_temp_max_hyst_set(self, temp, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_max_hyst_set(temp, index)

    def temp_core_label_get(self, temp, index=0):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.temp_label_get(temp, index)

    def temp_num_of_item_get(self):
        return self._num_of_item