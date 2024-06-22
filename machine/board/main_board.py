from src.api.fru_api import FruApi
from src.api.temp_api import TempApi
from src.base.board_base import BoardBase


class MainBoard(BoardBase, FruApi, TempApi):
    def __init__(self, board_config):
        BoardBase.__init__(self, board_config)
        FruApi.__init__(self, self._eeprom_core_list)
        TempApi.__init__(self, self._temp_core_list)