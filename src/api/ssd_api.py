from common.rc_code import RcCode


class SsdApi:
    def __init__(self, ssd_list):
        self._ssd_list = ssd_list

    def ssd_api_info_get(self, index=-1):
        ssd_info_dict = {}
        for i in range(0, len(self._ssd_list)):
            if i != -1 and i != index:
                continue
            ssd_obj = self._ssd_list[i]
            ssd_dict = {}
            rc, data = ssd_obj.ssd_core_vendor_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["vendor"] = data
            else:
                return rc, data
            rc, data = ssd_obj.ssd_capacity_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["capacity"] = data
            else:
                return rc, data
            rc, data = ssd_obj.ssd_capacity_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["capacity"] = data
            else:
                return rc, data
            rc, data = ssd_obj.ssd_size_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["size"] = data
            else:
                return rc, data
            rc, data = ssd_obj.ssd_sector_size_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["sector_size"] = data
            else:
                return rc, data
            rc, data = ssd_obj.ssd_dev_reference_get()
            if rc == RcCode.SUCCESS:
                ssd_dict["dev_reference"] = data
            else:
                return rc, data
            ssd_info_dict["Temp{index}".format(index=i)] = ssd_dict
        return RcCode.SUCCESS, ssd_info_dict
