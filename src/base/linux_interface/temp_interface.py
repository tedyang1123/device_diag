from common.rc_code import RcCode


class TempInterface:
    def temp_int(self):
        return RcCode.SUCCESS, None

    temp = "temp{index}_input"
    def temp_get(self, index=1):
        raise NotImplementedError

    temp_max = "temp{index}_max"
    def temp_max_get(self, index=1):
        raise NotImplementedError

    def temp_max_set(self, temp, index=1):
        raise NotImplementedError

    temp_crit = "temp{index}_crit"
    def temp_max_crit_get(self, index=1):
        raise NotImplementedError

    temp_min = "temp{index}_min"
    def temp_min_get(self, index=1):
        raise NotImplementedError

    def temp_min_set(self, temp, index=1):
        raise NotImplementedError

    temp_lcrit = "temp{index}_lcrit"
    def temp_min_crit_get(self, index=1):
        raise NotImplementedError

    temp_max_hyst = "temp{index}_max_hyst"
    def temp_max_hyst_get(self, index=1):
        raise NotImplementedError

    def temp_max_hyst_set(self, temp, index=1):
        raise NotImplementedError

    temp_label = "temp{index}_label"
    def temp_label_get(self, index=1):
        raise NotImplementedError
