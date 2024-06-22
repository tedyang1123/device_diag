from common.rc_code import RcCode


class DimmUi:
    def __init__(self, board_list):
        self._board_list = board_list

    def dimm_ui_info_get(self):
        info_dict = {}
        for board_key, board_value in self._board_list.items():
            try:
                rc, data = board_value.dimm_api_info_get()
            except AttributeError:
                continue
            if rc != RcCode.SUCCESS:
                return rc, None
            if data:
                info_dict[board_key] = data
        return RcCode.SUCCESS, info_dict

    def dimm_ui_util_get(self):
        return RcCode.NOT_SUPPORT, "Command does not support"