from src.api.temp_api import TempApi
from src.base.board_base import BoardBase


class FanBoard(BoardBase, TempApi):
    def __init__(self, board_config):
        BoardBase.__init__(self, board_config)
        TempApi.__init__(self, self._temp_core_list)