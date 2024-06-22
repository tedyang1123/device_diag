import sys

from common.rc_code import RcCode


class EepromCore:
    def __init__(self, **args):
        self._obj = None
        chip_name = args["chip_name"]
        if chip_name == "i2c":
            self._obj = getattr(
                sys.modules[__name__],
                chip_name.capitalize() + args["access_type"].capitalize())(args["i2c_bus"], args["i2c_addr"])

    def eeprom_core_read(self, offset: int):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.eeprom_read(offset)

    def eeprom_core_write(self, offset: int, value: int):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        return self._obj.eeprom_write(offset, value)

    def eeprom_core_dump(self):
        if self._obj is None:
            return RcCode.NOT_SUPPORT, None
        byte_data = bytearray()
        rc = RcCode.SUCCESS
        offset = 0
        while rc == RcCode.SUCCESS:
            rc, data = self._obj.eeprom_read(offset)
            byte_data.appned(data)
        return RcCode.SUCCESS, byte_data

