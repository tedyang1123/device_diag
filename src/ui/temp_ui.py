from common.rc_code import RcCode


class TempUi:
    def __init__(self, board_list):
        self._board_list = board_list

    def temp_ui_info_get(self):
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