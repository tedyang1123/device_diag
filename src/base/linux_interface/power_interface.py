from common.rc_code import RcCode


class PowerInterface:
    def power_init(self):
        return RcCode.SUCCESS, None

    power = "power{index}_input"
    def power_current_get(self, index=1):
        raise NotImplementedError

    power_min = "power{index}_min"
    def power_current_min_get(self, index=1):
        raise NotImplementedError

    power_max = "power{index}_max"
    def power_current_max_get(self, index=1):
        raise NotImplementedError

    power_lcrit = "power{index}_lcrit"
    def power_current_crit_min_get(self, index=1):
        raise NotImplementedError

    power_crit = "power{index}_crit"
    def power_current_crit_max_get(self, index=1):
        raise NotImplementedError
