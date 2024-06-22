from common.rc_code import RcCode


class VoltageInterface:
    def voltage_init(self):
        return RcCode.SUCCESS, None

    voltage = "in{index}_input"
    def voltage_get(self, index=0):
        raise NotImplementedError

    voltage_min = "in{index}_min"
    def voltage_min_get(self, index=0):
        raise NotImplementedError

    voltage_max = "in{index}_max"
    def voltage_max_get(self, index=0):
        raise NotImplementedError

    voltage_lcrit = "in{index}_lcrit"
    def voltage_crit_min_get(self, index=0):
        raise NotImplementedError

    voltage_crit = "in{index}_crit"
    def voltage_crit_max_get(self, index=0):
        raise NotImplementedError

    voltage_label = "in{index}_label"
    def voltage_label_get(self, index=0):
        raise NotImplementedError
