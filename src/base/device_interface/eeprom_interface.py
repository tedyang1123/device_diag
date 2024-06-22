from common.rc_code import RcCode


class EepromInterface:
    def eeprom_init(self):
        return RcCode.SUCCESS, None

    def eeprom_read(self, offset: int, index=0):
        raise NotImplementedError

    def eeprom_write(self, offset: int, value: int, index=0):
        raise NotImplementedError

