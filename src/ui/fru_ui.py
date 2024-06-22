from common.rc_code import RcCode


class FruUi:
    def __init__(self, board_list):
        self._board_list = board_list

    def fru_ui_init(self):
        pass

    def fru_ui_info_get(self):
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

    def fru_ui_internal_user_data_add(self):
        pass

    def fru_ui_internal_user_data_del(self):
        pass

    def fru_ui_chassis_pn_update(self):
        pass

    def fru_ui_chassis_sn_update(self):
        pass

    def fru_ui_board_mfg_data_update(self):
        pass

    def fru_ui_board_manufacturer_update(self):
        pass

    def fru_ui_board_name_update(self):
        pass

    def fru_ui_board_sn_update(self):
        pass

    def fru_ui_board_pn_update(self):
        pass

    def fru_ui_product_mfg_data_update(self):
        pass

    def fru_ui_product_manufacturer_update(self):
        pass

    def fru_ui_product_name_update(self):
        pass

    def fru_ui_product_sn_update(self):
        pass

    def fru_ui_product_pn_update(self):
        pass