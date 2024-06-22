from common.rc_code import RcCode


class MgmtPortApi:
    def __init__(self, mgmt_port_list):
        self._mgmt_port_list = mgmt_port_list

    def mgmt_port_api_mac_read(self, index=-1):
        mgmt_port_info_dict = {}
        for i in range(0, len(self._mgmt_port_list)):
            if i != -1 and i != index:
                continue
            mgmt_port_pbj = self._mgmt_port_list[i]
            rc, data = mgmt_port_pbj.mgmt_core_api_mac_addr_read()
            if rc == RcCode.SUCCESS:
                mgmt_port_info_dict["MgmtPort{index}".format(index=i)] = data
            else:
                return rc, data
        return RcCode.SUCCESS, mgmt_port_info_dict

    def mgmt_port_api_mac_write(self, index, mac_addr):
        for i in range(0, len(self._mgmt_port_list)):
            if i != index:
                continue
            mgmt_port_pbj = self._mgmt_port_list[i]
            return mgmt_port_pbj.mgmt_port_core_mac_addr_write(mac_addr)
        return RcCode.FAILURE