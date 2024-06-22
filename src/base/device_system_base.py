class DeviceSystemBase:
    def __init__(self):
        self._board_list = {}
        self._main_board = None
        self._cpu_board = None
        self._fan_board = None