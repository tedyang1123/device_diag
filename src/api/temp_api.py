from common.rc_code import RcCode


class TempApi:
    def __init__(self, temp_list):
        self._temp_list = temp_list

    def temp_api_get(self, index=-1):
        temp_info_dict = {}
        for i in range(0, len(self._temp_list)):
            if i != -1 and i != index:
                continue
            temp_info_dict["Temp{index}".format(index=i)] = {}
            temp_obj = self._temp_list[i]
            num_of_item = temp_obj.temp_num_of_item_get()
            for idx in range(1, num_of_item):
                try:
                    rc, label = temp_obj.temp_label_get(idx)
                except NotImplementedError:
                    label = "Temp_item_{idx}".format(idx=idx)
                rc, data = temp_obj.temp_core_temp_get()
                if rc == RcCode.SUCCESS:
                    temp_info_dict["Temp{index}".format(index=i)][label] = data
                else:
                    return rc, data
        return RcCode.SUCCESS, temp_info_dict
