from common.rc_code import RcCode


class OsApi:
    def __init__(self, os_instance):
        self._os_instance = os_instance

    def os_api_linux_version_get(self):
        os_info_dict = {}
        os_pbj = self._os_instance
        rc, data = os_pbj.os_core_linux_version_get()
        if rc == RcCode.SUCCESS:
            os_info_dict["LinuxVersion"] = data
        else:
            return rc, data
        return RcCode.SUCCESS, os_info_dict