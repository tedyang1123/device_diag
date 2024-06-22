from src.core.cpu_core import CpuCore
from src.core.dimm_core import DimmCore
from src.core.eeprom_core import EepromCore
from src.core.os_core import OsCore
from src.core.ssd_core import SsdCore
from src.core.temp_core import TempCore
from common.rc_code import RcCode


class BoardBase:
    def __init__(self, board_config):
        self._config = board_config
        self._cpu_core_list = []
        if "cpu" in board_config:
            for index in range(board_config["cpu"]):
                self._cpu_core_list.append(CpuCore())
        self._dimm_core_list = []
        if "dimm" in board_config:
            for dimm in board_config["dimm"]:
                self._dimm_core_list.append(DimmCore(dimm))
        self._eeprom_core_list = []
        if "eeprom" in board_config:
            for eeprom in board_config["eeprom"]:
                self._eeprom_core_list.append(EepromCore(eeprom))
        self._sata_ssd_core_list = []
        if "ssd" in board_config:
            for ssd in board_config["ssd"]:
                self._dimm_core_list.append(SsdCore(ssd))
        self._nvme_ssd_core_list = []
        if "nvme_ssd" in board_config:
            for nvme_ssd in board_config["nvme_ssd"]:
                self._dimm_core_list.append(DimmCore(nvme_ssd))
        self._mgmt_port_core_list = []
        if "mgmt_port" in board_config:
            for mgmt_port in board_config["mgmt_port"]:
                self._dimm_core_list.append(DimmCore(mgmt_port))
        self._power_core_list = []
        if "power" in board_config:
            for power in board_config["power"]:
                self._dimm_core_list.append(DimmCore(power))
        self._psu_list = []
        if "psu" in board_config:
            for psu in board_config["psu"]:
                self._dimm_core_list.append(DimmCore(psu))
        self._temp_core_list = []
        if "temperature" in board_config:
            for temp in board_config["temperature"]:
                self._temp_core_list.append(TempCore(temp))
        self._sfp_core_list = []
        if "sfp" in board_config:
            for sfp in board_config["sfp"]:
                self._temp_core_list.append(TempCore(sfp))
        self._os_core_instance = OsCore()

    ####################################################################################################
    # CPU
    ####################################################################################################

    def get_num_of_cpu(self) -> int:
        return len(self._cpu_core_list)

    def get_cpu_list(self) -> list:
        return self._cpu_core_list

    ####################################################################################################
    # DIMM
    ####################################################################################################

    def get_num_of_dimm(self) -> int:
        return len(self._dimm_core_list)

    ####################################################################################################
    # SATA SSD
    ####################################################################################################

    def get_num_of_sata_ssd(self) -> int:
        return len(self._sata_ssd_core_list)

    ####################################################################################################
    # SATA SSD
    ####################################################################################################

    def get_num_of_nvme_ssd(self) -> int:
        return len(self._nvme_ssd_core_list)

    ####################################################################################################
    # MGMT Port
    ####################################################################################################

    def get_num_of_power(self) -> int:
        return len(self._power_core_list)

    ####################################################################################################
    # MGMT Port
    ####################################################################################################

    def get_num_of_mgmt_port(self) -> int:
        return len(self._mgmt_port_core_list)

    ####################################################################################################
    # Temperature
    ####################################################################################################

    def get_num_of_temperatures(self) -> int:
        return len(self._temp_core_list)

    ####################################################################################################
    # SFP
    ####################################################################################################

    def get_num_of_sfp(self) -> int:
        return len(self._sfp_core_list)

    ####################################################################################################
    # API
    ####################################################################################################
    def board_init(self) -> tuple:
        for dimm_api in self._cpu_core_list:
            rc, msg = dimm_api.cpu_core_init()
            if rc != RcCode.SUCCESS:
                return rc, msg
        for dimm_api in self._dimm_core_list:
            rc, msg = dimm_api.dimm_core_init()
            if rc != RcCode.SUCCESS:
                return rc, msg

        for temp_api in self._temp_core_list:
            rc, msg = temp_api.temp_core_init()
            if rc != RcCode.SUCCESS:
                return rc, msg
        return RcCode.SUCCESS, None
