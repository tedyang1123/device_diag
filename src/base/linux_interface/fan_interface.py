from common.rc_code import RcCode


class FanInterface:
    def fan_init(self):
        return RcCode.SUCCESS, None

    fan_speed = "fan{index}_input"
    def fan_speed_get(self, index=1):
        raise NotImplementedError

    fam_min = "fan{index}_min"
    def fan_speed_min_get(self, index=1):
        raise NotImplementedError

    fam_max = "fan{index}_max"
    def fan_speed_max_get(self, index=1):
        raise NotImplementedError

    fan_target = "fan{index}_target"
    def fan_target_speed_get(self, index=1):
        raise NotImplementedError

    fan_label = "fan{index}_label"
    def fan_label_get(self, index=1):
        raise NotImplementedError
