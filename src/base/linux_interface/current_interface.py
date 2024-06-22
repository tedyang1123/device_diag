from common.rc_code import RcCode


class CurrentInterface:
    def current_init(self):
        return RcCode.SUCCESS, None

    current = "curr{index}_input"
    def current_get(self, index=1):
        raise NotImplementedError

    current_min = "curr{index}_min"
    def current_min_get(self, index=1):
        raise NotImplementedError

    current_max = "curr{index}_max"
    def current_max_get(self, index=1):
        raise NotImplementedError

    current_lcrit = "curr{index}_lcrit"
    def current_crit_min_get(self, index=1):
        raise NotImplementedError

    current_crit = "curr{index}_crit"
    def current_crit_max_get(self, index=1):
        raise NotImplementedError
