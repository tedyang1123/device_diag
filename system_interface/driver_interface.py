from common.rc_code import RcCode
from system_interface.system_call.driver_access import DriverAccess


class DriverInterface:
    def __init__(self, root_fs_path):
        self._driver_obj = DriverAccess(root_fs_path)

    def driver_read(self, file_name: str) -> tuple:
        return self._driver_obj.driver_access_read(file_name)

    def driver_write(self, file_name: str, data: str) -> RcCode:
        return self._driver_obj.driver_access_write(file_name, data)

    def driver_bin_read(self, file_name: str, offset: int, data_len: int) -> tuple:
        return self._driver_obj.driver_access_binary_read(file_name, offset, data_len)

    def driver_bin_write(self, file_name: str, offset: int, data_len: int, data: bytearray) -> RcCode:
        return self._driver_obj.driver_access_binary_write(file_name, offset, data_len, data)
