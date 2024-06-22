from common.rc_code import RcCode


class PwmInterface:
    def pwm_init(self):
        return RcCode.SUCCESS, None

    pwm = "pwm{index}"
    def pwm_get(self, index=1):
        raise NotImplementedError

    def pwm_set(self, percentage: int, index=1):
        raise NotImplementedError

    pwm_enable = "pwm{index}_enable"
    def pwm_enable_get(self, index=1):
        raise NotImplementedError

    def pwm_enable_set(self, state: bool, index=1):
        raise NotImplementedError
