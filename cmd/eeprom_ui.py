from common.rc_code import RcCode


class EepromUi:
    def __init__(self, board_list):
        self._board_list = board_list

    def eeprom_ui_info_get(self):
        info_dict = {}
        for board_key, board_value in self._board_list.items():
            try:
                rc, data = board_value.temp_api_get()
            except AttributeError:
                continue
            if rc != RcCode.SUCCESS:
                return rc, None
            if data:
                info_dict[board_key] = data
        return RcCode.SUCCESS, info_dict

    def eeprom_ui_data_reset(self):
        pass

    def eeprom_ui_data_sn_reset(self):
        pass

    def eeprom_ui_data_pn_resent(self):
        pass