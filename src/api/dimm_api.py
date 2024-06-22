from common.rc_code import RcCode


class DimmApi:
    def __init__(self, dimm_list):
        self._dimm_list = dimm_list

    def dimm_api_info_get(self, index=-1):
        dimm_info_dict = {}
        for i in range(0, len(self._dimm_list)):
            if i != -1 and i != index:
                continue
            dimm_pbj = self._dimm_list[i]
            rc, data = dimm_pbj.dimm_core_info_get()
            if rc == RcCode.SUCCESS:
                dimm_info_dict["Dimm{index}".format(index=i)] = data
            else:
                return rc, data
        return RcCode.SUCCESS, dimm_info_dict