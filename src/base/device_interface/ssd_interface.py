from common.rc_code import RcCode


class SsdInterface:
    def ssd_init(self):
        return RcCode.SUCCESS, None

    def ssd_vendor_get(self):
        raise NotImplementedError

    def ssd_capacity_get(self):
        raise NotImplementedError

    def ssd_size_get(self):
        raise NotImplementedError

    def ssd_sector_size_get(self):
        raise NotImplementedError

    def ssd_dev_reference_get(self):
        raise NotImplementedError
