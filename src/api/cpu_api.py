from common.rc_code import RcCode


class CpuApi:
    def __init__(self, cpu_list):
        self._cpu_list = cpu_list

    def cpu_api_info_get(self, index=-1):
        cpu_info_dict = {}
        for i in range(0, len(self._cpu_list)):
            if index != -1 and i != index:
                continue
            cpu_pbj = self._cpu_list[i]
            rc, data = cpu_pbj.cpu_core_info_get()
            if rc == RcCode.SUCCESS:
                cpu_info_dict["Cpu{index}".format(index=i)] = data
            else:
                return rc, data
        return RcCode.SUCCESS, cpu_info_dict

    def cpu_api_utilization_get(self, index=-1):
        cpu_utilization_dict = {}
        for i in range(0, len(self._cpu_list)):
            if index != -1 and i != index:
                continue
            cpu_pbj = self._cpu_list[i]
            rc, data = cpu_pbj.cpu_core_utilization_get()
            if rc == RcCode.SUCCESS:
                core_index = 0
                for core in data:
                    cpu_utilization_dict["Cpu{cpu_index}_core{cpu_core}".format(cpu_index=i,
                                                                                cpu_core= core_index)] = core
                    core_index = core_index + 1
            else:
                return rc, data

        return RcCode.SUCCESS, cpu_utilization_dict