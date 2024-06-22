from common.rc_code import RcCode
from src.lib.fru.data_converter import convert_str_to_minutes
from src.lib.fru.fru_area import InternalArea, CommonHeader, PadArea, make_internal_area, make_chassis_area, \
    make_board_area, \
    make_product_area, make_common_header, make_pad_area_data, ChassisArea, BoardArea, ProductArea, parse_common_header, \
    parse_internal_area, parse_chassis_area, parse_board_area, parse_product_area


class FruHandler:
    def __init__(self, fru_size):
        self._fru_size = fru_size
        self._fru_config = {}
        self._fru_data = {
            "common": b"",
            "internal": b"",
            "chassis": b"",
            "board": b"",
            "product": b"",
            "multiurecord": b"",
            "pad": b""
        }

    def init_fru_config_from_fru_data(self, fru_data):
        common = parse_common_header(fru_data)

        self._fru_config["common"] = {
            "format_version": common["format_version"]  & 0x0F,
        }

        internal_offset = common["internal_offset"] * 8
        chassis_offset = common["chassis_offset"] * 8
        board_offset = common["board_offset"] * 8
        product_offset = common["product_offset"] * 8

        if internal_offset:
            next_offset = chassis_offset or board_offset or product_offset
            rc, data = parse_internal_area(fru_data[internal_offset: next_offset or len(fru_data)])
            if rc != RcCode.SUCCESS:
                return rc, data
            self._fru_config["internal"] = data
        if chassis_offset:
            length = ord(fru_data[chassis_offset + 1: chassis_offset + 2]) * 8
            rc, data = parse_chassis_area(fru_data[chassis_offset: chassis_offset + length])
            if rc != RcCode.SUCCESS:
                return rc, data
            self._fru_config["chassis"] = data
        if board_offset:
            length = ord(fru_data[board_offset + 1: board_offset + 2]) * 8
            rc, data = parse_board_area(fru_data[board_offset: board_offset + length])
            if rc != RcCode.SUCCESS:
                return rc, data
            self._fru_config["board"] = data
        if product_offset:
            length = ord(fru_data[product_offset + 1: product_offset + 2]) * 8
            rc, data = parse_product_area(fru_data[product_offset: product_offset + length])
            if rc != RcCode.SUCCESS:
                return rc, data
            self._fru_config["product"] = data
        return RcCode.SUCCESS, self._fru_config

    def _calculate_fru_area_offset(self):
        pos = 1
        internal_offset = 0
        if len(self._fru_data["internal"]):
            internal_offset = pos
            pos += len(self._fru_data["internal"]) // 8
        chassis_offset = 0
        if len(self._fru_data["chassis"]):
            chassis_offset = pos
            pos += len(self._fru_data["chassis"]) // 8
        board_offset = 0
        if len(self._fru_data["board"]):
            board_offset = pos
            pos += len(self._fru_data["board"]) // 8
        product_offset = 0
        if len(self._fru_data["product"]):
            product_offset = pos
            pos += len(self._fru_data["product"]) // 8
        multirecord_offset = 0
        if len(self._fru_data["multiurecord"]):
            product_offset = pos
            pos += len(self._fru_data["multiurecord"]) // 8
        return internal_offset, chassis_offset, board_offset, product_offset, multirecord_offset

    def init_fru_data_from_config(self, fru_config):
        if "internal" in fru_config and "data" in fru_config["internal"]:
            rc, data = make_internal_area(fru_config["internal"])
            if rc != RcCode.SUCCESS:
                return rc, None
            self._fru_data["internal"] = data
        if "chassis" in fru_config:
            rc, data = make_chassis_area(fru_config["chassis"])
            if rc != RcCode.SUCCESS:
                return rc, None
            self._fru_data["chassis"] = data
        if "board" in fru_config:
            rc, data = make_board_area(fru_config["board"])
            if rc != RcCode.SUCCESS:
                return rc, None
            self._fru_data["board"] = data
        if "product" in fru_config:
            rc, data = make_product_area(fru_config["product"])
            if rc != RcCode.SUCCESS:
                return rc, None
            self._fru_data["product"] = data
        if "multiurecord" in fru_config:
            self._fru_data["multiurecord"] = b""

        internal_offset, chassis_offset, board_offset, product_offset, multirecord_offset = \
            self._calculate_fru_area_offset()

        # Header
        rc, data = make_common_header(
            {
                "format_version": fru_config["common"]["format_version"],
                "internal_offset": internal_offset,
                "chassis_offset": chassis_offset,
                "board_offset": board_offset,
                "product_offset": product_offset,
                "multirecord_offset": multirecord_offset
            }
        )
        if rc != RcCode.SUCCESS:
            return rc, None
        self._fru_data["common"] = data

        total_len = len(self._fru_data["common"]) + len(self._fru_data["internal"]) + \
                    len(self._fru_data["chassis"]) + len(self._fru_data["board"]) + \
                    len(self._fru_data["product"])
        difference = self._fru_size - total_len
        if difference < 0:
            return RcCode.INVALID_VALUE, "Too much content, does not fit"
        pad = PadArea(self._fru_data["pad"])
        rc, data = pad.modify_pad_area_data_field(difference)
        if rc != RcCode.SUCCESS:
            return rc, None
        self._fru_data["pad"] = data
        return RcCode.SUCCESS, self._fru_data

    def sync_fru_data(self):
        internal_offset, chassis_offset, board_offset, product_offset, multirecord_offset = \
            self._calculate_fru_area_offset()

        common_header = CommonHeader(self._fru_data["common"])
        rc, data = \
            common_header.modify_command_header_offset_field(internal_offset, chassis_offset, board_offset,
                                                             product_offset, multirecord_offset)
        if rc != RcCode.SUCCESS:
            return rc, None
        self._fru_data["common"] = data
        total_len = len(self._fru_data["common"]) + len(self._fru_data["internal"]) + \
                    len(self._fru_data["chassis"]) + len(self._fru_data["board"]) + \
                    len(self._fru_data["product"])
        difference = self._fru_size - total_len
        if difference < 0:
            return RcCode.INVALID_VALUE, "Too much content, does not fit"
        pad = PadArea(self._fru_data["pad"])
        rc, data = pad.modify_pad_area_data_field(difference)
        if rc != RcCode.SUCCESS:
            return rc, None
        self._fru_data["pad"] = data
        return RcCode.SUCCESS, None

    ###########################################################################################
    # Common Header API
    ###########################################################################################

    ###########################################################################################
    # Internal Area API
    ###########################################################################################

    def add_internal_area_internal_use_data(self, data):
        internal_area = InternalArea(self._fru_data["internal"])
        rc, bin_data = internal_area.add_internal_area_data_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["internal"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def delete_internal_area_internal_user_data(self, data):
        internal_area = InternalArea(self._fru_data["internal"])
        rc, bin_data = \
            internal_area.delete_internal_area_data_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["internal"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    ###########################################################################################
    # Chassis Area API
    ###########################################################################################

    def modify_chassis_area_type(self, data):
        chassis_area = ChassisArea(self._fru_data["chassis"])
        rc, bin_data = \
            chassis_area.modify_chassis_area_type_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["chassis"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_chassis_area_part_number(self, data):
        chassis_area = ChassisArea(self._fru_data["chassis"])
        rc, bin_data = \
            chassis_area.modify_chassis_area_pn_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["chassis"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_chassis_area_serial_number(self, data):
        chassis_area = ChassisArea(self._fru_data["chassis"])
        rc, bin_data = \
            chassis_area.modify_chassis_area_sn_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["chassis"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    ###########################################################################################
    # Board Area API
    ###########################################################################################

    def modify_board_area_language_code(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, bin_data = \
            board_area.modify_board_area_language_code_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_board_area_mfg_date_time(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, date = convert_str_to_minutes(data)
        if rc != RcCode.SUCCESS:
            return rc, data
        rc, bin_data = \
            board_area.modify_board_area_mfg_date_time_field(date)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_board_area_manufacturer(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, bin_data = \
            board_area.modify_board_area_manufacturer_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_board_area_product_name(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, bin_data = \
            board_area.modify_board_area_product_name_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_board_area_serial_number(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, bin_data = \
            board_area.modify_board_area_serial_number_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_board_area_part_number(self, data):
        board_area = BoardArea(self._fru_data["board"])
        rc, bin_data = \
            board_area.modify_board_area_part_number_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["board"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    ###########################################################################################
    # Product Area API
    ###########################################################################################

    def modify_product_area_mfg_date_time(self, data):
        product_area = ProductArea(self._fru_data["product"])
        rc, bin_data = \
            product_area.modify_product_area_mfg_date_time_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["product"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_product_area_manufacturer(self, data):
        product_area = ProductArea(self._fru_data["product"])
        rc, bin_data = \
            product_area.modify_product_area_manufacturer_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["product"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_product_area_product_name(self, data):
        product_area = ProductArea(self._fru_data["product"])
        rc, bin_data = \
            product_area.modify_product_area_product_name_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["product"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_product_area_serial_number(self, data):
        product_area = ProductArea(self._fru_data["product"])
        rc, bin_data = \
            product_area.modify_product_area_serial_number_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["product"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data

    def modify_product_area_part_number(self, data):
        product_area = ProductArea(self._fru_data["product"])
        rc, bin_data = \
            product_area.modify_product_area_part_number_field(data)
        if rc != RcCode.SUCCESS:
            return rc, bin_data
        self._fru_data["product"] = bin_data
        rc, msg = self.sync_fru_data()
        if rc != RcCode.SUCCESS:
            return rc, msg
        return RcCode.SUCCESS, self._fru_data
