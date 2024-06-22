import sys

from dmidecode import DMIDecode
from common.rc_code import RcCode


class DimmCore:
    def __init__(self, **args):
        self._obj = None
        chip_name = args["chip_name"]
        if chip_name == "i2c":
            self._obj = getattr(
                sys.modules[__name__],
                chip_name.capitalize() + args["access_type"].capitalize())(args["i2c_bus"], args["i2c_addr"])
        self.dmi = DMIDecode()

    def dimm_core_init(self):
        return RcCode.SUCCESS, None

    def dimm_core_info_get(self):
        info_dict = {}
        dimm_info = self.dmi.get("Memory Device")[2]
        if dimm_info:
            info_dict["Locator"] = dimm_info['Locator']
            info_dict["Type"] = dimm_info['Type']
            info_dict["Speed"] = dimm_info['Speed']
            info_dict["Size"] = dimm_info['Size']
            info_dict["Part Number"] = dimm_info['Part Number']
            return RcCode.SUCCESS, info_dict
        else:
            return RcCode.FAILURE, None