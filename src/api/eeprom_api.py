from common.rc_code import RcCode


class EepromApi:
    def __init__(self, eeprom_list):
        self._eeprom_list= eeprom_list

    def eeprom_api_read(self, index=-1):
        eeprom_info_dict = {}
        for i in range(0, len(self._eeprom_list)):
            if i != -1 and i != index:
                continue
            eeprom_obj = self._eeprom_list[i]
            rc, data = eeprom_obj.eeprom_core_read()
            if rc == RcCode.SUCCESS:
                eeprom_info_dict["Eeprom{index}".format(index=i)] = data
            else:
                return rc, data
        return RcCode.SUCCESS, eeprom_info_dict

    def eeprom_api_write(self, index, value: int):
        for i in range(0, len(self._eeprom_list)):
            if i != index:
                continue
            eeprom_obj = self._eeprom_list[i]
            return eeprom_obj.eeprom_core_write(value)
        return RcCode.FAILURE

    def eeprom_api_dump(self):
        eeprom__dump_info_dict = {}
        for i in range(0, len(self._eeprom_list)):
            eeprom_obj = self._eeprom_list[i]
            rc, data = eeprom_obj.eeprom_core_dump()
            if rc == RcCode.SUCCESS:
                eeprom__dump_info_dict["Eeprom{index}".format(index=i)] = data
            else:
                return rc, data
        return RcCode.SUCCESS, eeprom__dump_info_dict
