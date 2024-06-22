from common.rc_code import RcCode
from system_interface.os_interface import OsInterface


class MgmtPortCore:
    def __init__(self, vendor, chip_name):
        self._vendor = vendor
        self._chip_name = chip_name

    def mgmt_port_core_init(self):
        return RcCode.SUCCESS, None

    def mgmt_core_api_mac_addr_read(self):
        if self._vendor == "intel":
            os_obj = OsInterface()
            rc, value = os_obj.os_interface_exec_cmd(
                "eeupdate64e | grep {chip_name} | awk '{{print $1}}'".format(chip_name=self._chip_name))
            if rc != RcCode.SUCCESS:
                return RcCode.ERROR

            if len(value) <= 0:
                return RcCode.NOT_FOUND

            rc, value = os_obj.os_interface_exec_cmd(
                "eeupdate64e /nic={nic_id} /mac_dump | grep \"LAN MAC Address\"".format(nic_id=int(value)))
            if rc != RcCode.SUCCESS:
                return RcCode.FAILURE

            mac_info = value.strip().split(" ")[6][:-1]
            addr_list = []
            for idx, info in enumerate(list(mac_info)):
                if idx % 2 == 0 and idx != 0:
                    addr_list.append(":")
                addr_list.append(info)
            return RcCode.SUCCESS, ''.join(addr_list)
        else:
            return RcCode.NOT_SUPPORT

    def mgmt_port_core_mac_addr_write(self, mac_addr: str):
        if mac_addr is None or type(mac_addr) == str:
            return RcCode.INVALID_TYPE
        if self._vendor == "intel":
            os_obj = OsInterface()
            rc, value = os_obj.os_interface_exec_cmd(
                "eeupdate64e | grep {chip_name} | awk '{{print $1}}'".format(chip_name=self._chip_name))
            if rc != RcCode.SUCCESS:
                return RcCode.ERROR

            if len(value) <= 0:
                return RcCode.NOT_FOUND

            rc, value = os_obj.os_interface_exec_cmd(
                "eeupdate64e /nic={nic_id} /mac={mac_str}".format(nic_id=int(value), mac_str="".join(f'{x:02x}' for x in mac_addr)))
            if rc != RcCode.SUCCESS:
                return RcCode.FAILURE
            return RcCode.SUCCESS
        else:
            return RcCode.NOT_SUPPORT

