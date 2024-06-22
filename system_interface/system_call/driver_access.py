import os

from common.rc_code import RcCode


class DriverAccess:
    def __init__(self, root_fs_path:str):
        self.root_fs_path = root_fs_path

    def driver_access_read(self, file_name: str) -> tuple:
        target_file = os.path.join(self.root_fs_path, file_name)
        if not os.path.isfile(target_file):
            return RcCode.FILE_NOT_FOUND, None
        try:
            with open(target_file, "r") as f:
                data = f.read()
        except OSError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, data

    def driver_access_write(self, file_name: str, data: str) -> RcCode:
        target_file = os.path.join(self.root_fs_path, file_name)
        if not os.path.isfile(target_file):
            return RcCode.FILE_NOT_FOUND
        try:
            with open(target_file, "r+") as f:
                f.write(data)
        except OSError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def driver_access_binary_read(self, file_name: str, offset: int, data_len: int) -> tuple:
        target_file = os.path.join(self.root_fs_path, file_name)
        if not os.path.isfile(target_file):
            return RcCode.FILE_NOT_FOUND, None
        try:
            with open(target_file, "rb") as f:
                f.seek(offset)
                data = f.read(data_len)
        except OSError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, data

    def driver_access_binary_write(self, file_name:str, offset: int, data_len: int, data: bytes) -> RcCode:
        target_file = os.path.join(self.root_fs_path, file_name)
        if not os.path.isfile(target_file):
            return RcCode.FILE_NOT_FOUND
        try:
            with open(target_file, "r+b", buffering=0) as f:
                f.seek(offset)
                f.write(data[0:data_len])
        except OSError:
            return RcCode.FAILURE
        return RcCode.SUCCESS
