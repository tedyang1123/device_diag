import os

from common.common import load_data_from_json
from common.rc_code import RcCode
from machine.board.cpu_board import CpuBoard
from machine.board.fan_board import FanBoard
from machine.board.main_board import MainBoard
from src.base.device_system_base import DeviceSystemBase


class DeviceSystem(DeviceSystemBase):
    def __init__(self):
        DeviceSystemBase.__init__(self)
        config_path = "/home/tedyang/new_diag/machine/config/"
        main_board_config_file = os.path.join(config_path, "main_board_config.json")
        if os.path.isfile(main_board_config_file):
            rc, main_board_config = load_data_from_json(main_board_config_file)
            if rc == RcCode.SUCCESS:
                self._main_board = MainBoard(main_board_config)
                self._board_list["Main_Board"] = self._main_board
        cpu_board_config_file = os.path.join(config_path, "cpu_board_config.json")
        if os.path.isfile(cpu_board_config_file):
            rc, cpu_board_config = load_data_from_json(cpu_board_config_file)
            if rc == RcCode.SUCCESS:
                self._cpu_board = CpuBoard(cpu_board_config)
                self._board_list["Cpu_Board"] = self._cpu_board
        fan_board_config_file = os.path.join(config_path, "fan_board_config.json")
        if os.path.isfile(fan_board_config_file):
            rc, fan_board_config = load_data_from_json(fan_board_config_file)
            if rc == RcCode.SUCCESS:
                self._fan_board = FanBoard(fan_board_config)
                self._board_list["Fan_Board"] = self._fan_board

    def device_init(self) -> tuple:
        if self._main_board is not None:
            rc, msg = self._main_board.board_init()
            if rc != RcCode.SUCCESS:
                return rc, msg
        if self._cpu_board is not None:
            rc, msg = self._cpu_board.board_init()
            if rc != RcCode.SUCCESS:
                return rc, msg
        if self._cpu_board is not None:
            rc, msg = self._fan_board.board_init()
            if rc != RcCode.SUCCESS:
                return rc, msg
        return RcCode.SUCCESS, None

    def device_board_list_get(self):
        return self._board_list
