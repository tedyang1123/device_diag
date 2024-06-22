from common.rc_code import RcCode
from src.lib.fru.share_lib import parse_common_header, make_common_header, parse_internal_area, make_internal_area, \
    parse_chassis_area, make_chassis_area, parse_board_area, make_board_area, parse_product_area, make_product_area, \
    make_pad_area_data


class CommonHeader:
    def __init__(self, data):
        self._command_header_data = data

    def modify_command_header_format_version_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_common_header(self._command_header_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["format_version"] = field_data
        rc, self._command_header_data = make_common_header(dict_data)
        return rc, self._command_header_data

    def modify_command_header_offset_field(self, internal_field_data, chassis_field_dat, board_field_dataa,
                                           product_field_data, multirecord_field_data, dict_data=None):
        if dict_data is None:
            dict_data = parse_common_header(self._command_header_data)
        dict_data["internal_offset"] = internal_field_data
        dict_data["chassis_offset"] = chassis_field_dat
        dict_data["board_offset"] = board_field_dataa
        dict_data["product_offset"] = product_field_data
        dict_data["multirecord_offset"] = multirecord_field_data
        rc, self._command_header_data = make_common_header(dict_data)
        return rc, self._command_header_data


class InternalArea:
    def __init__(self, data):
        self._internal_fru_data = data

    def add_internal_area_data_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_internal_area(self._internal_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["data"] = field_data
        rc, self._internal_fru_data = make_internal_area(dict_data)
        return rc, self._internal_fru_data

    def delete_internal_area_data_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_internal_area(self._internal_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "data" in dict_data:
            locate_idx = -1
            for i in range(len(dict_data["data"])):
                if dict_data["data"][i] == field_data:
                    locate_idx = i
                    break
            if locate_idx != -1:
                del dict_data["data"][locate_idx]
        rc, self._internal_fru_data = make_internal_area(dict_data)
        return rc, self._internal_fru_data


class ChassisArea:
    def __init__(self, data):
        self._chassis_fru_data = data

    def modify_chassis_area_type_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_chassis_area(self._chassis_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["type"] = field_data
        rc, self._chassis_fru_data = make_chassis_area(dict_data)
        return rc, self._chassis_fru_data

    def modify_chassis_area_pn_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_chassis_area(self._chassis_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["part_number"] = field_data
        rc, self._chassis_fru_data = make_chassis_area(dict_data)
        return rc, self._chassis_fru_data

    def modify_chassis_area_sn_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_chassis_area(self._chassis_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["serial_number"] = field_data
        rc, self._chassis_fru_data = make_chassis_area(dict_data)
        return rc, self._chassis_fru_data

    def add_chassis_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_chassis_area(self._chassis_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" not in dict_data:
            dict_data["custom_fields"] = []
        found = False
        for record in dict_data["custom_fields"]:
            if record == field_data:
                found = True
                break
        if not found:
            dict_data["custom_fields"].append(field_data)
        rc, self._chassis_fru_data = make_chassis_area(dict_data)
        return rc, self._chassis_fru_data

    def delete_chassis_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_chassis_area(self._chassis_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" in dict_data:
            locate_idx = -1
            for i in range(len(dict_data["custom_fields"])):
                if dict_data["custom_fields"][i] == field_data:
                    locate_idx = i
                    break
            if locate_idx != -1:
                del dict_data["custom_fields"][locate_idx]
        rc, self._chassis_fru_data = make_chassis_area(dict_data)
        return rc, self._chassis_fru_data


class BoardArea:
    def __init__(self, data):
        self._board_fru_data = data

    def modify_board_area_language_code_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["language_code"] = field_data
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def modify_board_area_mfg_date_time_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["mfg_date_time"] = field_data
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def modify_board_area_manufacturer_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["manufacturer"] = field_data
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def modify_board_area_product_name_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["product_name"] = field_data
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def modify_board_area_serial_number_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["serial_number"] = field_data
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def modify_board_area_part_number_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["part_number"] = field_data
        self._board_fru_data = make_board_area(dict_data)
        return self._board_fru_data

    def add_board_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" not in dict_data:
            dict_data["custom_fields"] = []
        found = False
        for record in dict_data["custom_fields"]:
            if record == field_data:
                found = True
                break
        if not found:
            dict_data["custom_fields"].append(field_data)
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data

    def delete_board_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_board_area(self._board_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" in dict_data:
            locate_idx = -1
            for i in range(len(dict_data["custom_fields"])):
                if dict_data["custom_fields"][i] == field_data:
                    locate_idx = i
                    break
            if locate_idx != -1:
                del dict_data["custom_fields"][locate_idx]
        rc, self._board_fru_data = make_board_area(dict_data)
        return rc, self._board_fru_data


class ProductArea:
    def __init__(self, data):
        self._product_fru_data = data

    def modify_product_area_language_code_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["language_code"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_mfg_date_time_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["mfg_date_time"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_manufacturer_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["manufacturer"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_product_name_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["product_name"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_part_number_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["part_number"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_product_version_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["product_version"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def modify_product_area_serial_number_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        dict_data["serial_number"] = field_data
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def add_product_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" not in dict_data:
            dict_data["custom_fields"] = []
        found = False
        for record in dict_data["custom_fields"]:
            if record == field_data:
                found = True
                break
        if not found:
            dict_data["custom_fields"].append(field_data)
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data

    def delete_product_area_custom_field(self, field_data, dict_data=None):
        if dict_data is None:
            rc, dict_data = parse_product_area(self._product_fru_data)
            if rc != RcCode.SUCCESS:
                return rc, None
        if "custom_fields" in dict_data:
            locate_idx = -1
            for i in range(len(dict_data["custom_fields"])):
                if dict_data["custom_fields"][i] == field_data:
                    locate_idx = i
                    break
            if locate_idx != -1:
                del dict_data["custom_fields"][locate_idx]
        rc, self._product_fru_data = make_product_area(dict_data)
        return rc, self._product_fru_data


class PadArea:
    def __init__(self, data):
        self._pad_data = data

    def modify_pad_area_data_field(self, pad_size):
        rc, self._pad_data = make_pad_area_data(pad_size)
        return rc, self._pad_data
