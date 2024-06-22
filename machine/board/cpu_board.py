from src.api.cpu_api import CpuApi
from src.api.dimm_api import DimmApi
from src.api.eeprom_api import EepromApi
from src.api.os_api import OsApi
from src.api.temp_api import TempApi
from src.base.board_base import BoardBase


class CpuBoard(BoardBase, CpuApi, DimmApi, TempApi, OsApi, EepromApi):
    def __init__(self, board_config):
        BoardBase.__init__(self, board_config)
        CpuApi.__init__(self, self._cpu_core_list)
        DimmApi.__init__(self, self._dimm_core_list)
        TempApi.__init__(self, self._temp_core_list)
        OsApi.__init__(self, self._os_core_instance)
        EepromApi.__init__(self, self._eeprom_core_list)