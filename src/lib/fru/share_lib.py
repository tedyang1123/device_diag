import struct

from common.rc_code import RcCode


def extract_values(blob, offset, names):
    data = {
        "custom_fields": [],
    }

    for name in names:
        type_length = ord(blob[offset: offset + 1])
        if type_length == 0xC1:
            return RcCode.SUCCESS, data
        length = type_length & 0x3F
        data[name] = blob[offset + 1: offset + length + 1].decode("ascii")
        offset += length + 1

    while True:
        type_length = ord(blob[offset: offset + 1])
        if type_length == 0xC1:
            return RcCode.SUCCESS, data
        length = type_length & 0x3F
        data["custom_fields"].append(
            blob[offset + 1: offset + length + 1].decode("ascii")
        )
        offset += length + 1


def validate_checksum(binary_data: bytes, length: int):
    checksum = int.from_bytes(binary_data[length - 1: length], "big")
    data_sum = sum(
        struct.unpack("{}B".format(length - 1), binary_data[: length - 1])
    )
    if 0xFF & (data_sum + checksum) != 0:
        return RcCode.FAILURE
    return RcCode.SUCCESS


def get_default_common_section():
    return {
        "format_version": 1,
        "size": 0,
    }


def get_default_chassis_section():
    return {
        "format_version": 1,
        "type": 0,
        "part_number": "",
        "serial_number": "",
        "custom_fields": [],
    }


def get_default_board_section():
    return {
        "format_version": 1,
        "language_code": 0,
        "mfg_date_time": 0,
        "manufacturer": "",
        "product_name": "",
        "serial_number": "",
        "part_number": "",
        "fru_file_id": "",
        "custom_fields": [],
    }


def get_default_product_section():
    return {
        "format_version": 1,
        "language_code": 0,
        "manufacturer": "",
        "product_name": "",
        "part_number": "",
        "product_version": "",
        "serial_number": "",
        "asset_tag": "",
        "fru_file_id": "",
        "custom_fields": [],
    }


def get_chassis_section_names():
    return (
        "part_number",
        "serial_number",
    )


def get_board_section_names():
    return (
        "manufacturer",
        "product_name",
        "serial_number",
        "part_number",
        "fru_file_id",
    )


def get_product_section_names():
    return (
        "manufacturer",
        "product_name",
        "part_number",
        "product_version",
        "serial_number",
        "asset_tag",
        "fru_file_id",
    )


def parse_common_header(common_header_data):
    return {
        "format_version": ord(common_header_data[0:1]),
        "internal_offset": ord(common_header_data[1:2]),
        "chassis_offset": ord(common_header_data[2:3]),
        "board_offset": ord(common_header_data[3:4]),
        "product_offset": ord(common_header_data[4:5]),
        "multirecord_offset": 0
    }


def make_common_header(common_header_data):
    out = struct.pack("BBBBBBB",
                      common_header_data["format_version"],
                      common_header_data["internal_offset"],
                      common_header_data["chassis_offset"],
                      common_header_data["board_offset"],
                      common_header_data["product_offset"],
                      common_header_data["multirecord_offset"],
                      0x00)
    out += struct.pack("B", (0 - sum(bytearray(out))) & 0xFF)
    return RcCode.SUCCESS, out


def parse_internal_area(internal_fru_data):
    return RcCode.SUCCESS, {
        "format_version": internal_fru_data[0] & 0x0F,
        "data": internal_fru_data[1: len(internal_fru_data)]
    }


def make_internal_area(internal_fru_info):
    return RcCode.SUCCESS, struct.pack("B{data_size}s".format(data_size=len(internal_fru_info["data"])),
                                       internal_fru_info.get("format_version", 1),
                                       internal_fru_info["data"])


def parse_chassis_area(chassis_fru_data):
    length = ord(chassis_fru_data[1: 2]) * 8
    validate_checksum(chassis_fru_data, length)

    chassis_info = get_default_chassis_section()
    chassis_info.update(
        {
            "format_version": ord(chassis_fru_data[0: 1]) & 0x0F,
            "type": ord(chassis_fru_data[2: 3]),
        }
    )
    names = get_chassis_section_names()
    rc, data = extract_values(chassis_fru_data, 3, names)
    if rc != RcCode.SUCCESS:
        return RcCode.FAILURE, None
    chassis_info.update(data)
    return RcCode.SUCCESS, chassis_info


def make_chassis_area(chassis_fru_info):
    chassis = get_default_chassis_section()
    chassis.update(chassis_fru_info)

    out = struct.pack("B", chassis["type"])

    fields = get_chassis_section_names()
    for key in fields:
        if chassis[key]:
            value = chassis[key].encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
        else:
            out += struct.pack("B", 0)
    if isinstance(chassis["custom_fields"], (list, tuple)):
        for record in chassis["custom_fields"]:
            value = record.encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
    out += struct.pack("B", 0xC1)

    while len(out) % 8 != 5:
        out += struct.pack("B", 0)

    out = struct.pack("BB", chassis["format_version"], (len(out) + 3) // 8,) + out

    out += struct.pack("B", (0 - sum(bytearray(out))) & 0xFF)

    return RcCode.SUCCESS, out


def parse_board_area(board_fru_data):
    length = ord(board_fru_data[1: 2]) * 8
    validate_checksum(board_fru_data, length)

    board_info = get_default_board_section()
    board_info.update(
        {
            "format_version": ord(board_fru_data[: 1]) & 0x0F,
            "language_code": ord(board_fru_data[2: 3]),
            "mfg_date_time": sum(
                [
                    ord(board_fru_data[3: 4]),
                    ord(board_fru_data[4: 5]) << 8,
                    ord(board_fru_data[5: 6]) << 16,
                ]
            ),
        }
    )
    names = get_board_section_names()
    rc, data = extract_values(board_fru_data, 6, names)
    if rc != RcCode.SUCCESS:
        return RcCode.FAILURE, None
    board_info.update(data)
    return RcCode.SUCCESS, board_info


def make_board_area(board_fru_info):
    board = get_default_board_section()
    board.update(board_fru_info)

    out = struct.pack("B", board["language_code"])

    date = board["mfg_date_time"]
    out += struct.pack("BBB", (date & 0xFF), (date & 0xFF00) >> 8, (date & 0xFF0000) >> 16)

    fields = get_board_section_names()
    for key in fields:
        if board[key]:
            value = board[key].encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
        else:
            out += struct.pack("B", 0)
    if isinstance(board["custom_fields"], (list, tuple)):
        for record in board["custom_fields"]:
            value = record.encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
    out += struct.pack("B", 0xC1)

    while len(out) % 8 != 5:
        out += struct.pack("B", 0)

    out = struct.pack("BB", board["format_version"], (len(out) + 3) // 8) + out

    out += struct.pack("B", (0 - sum(bytearray(out))) & 0xFF)

    return RcCode.SUCCESS, out


def parse_product_area(product_fru_data):
    length = ord(product_fru_data[1: 2]) * 8

    validate_checksum(product_fru_data, length)

    product_info = get_default_product_section()
    product_info.update(
        {
            "format_version": ord(product_fru_data[: 1]) & 0x0F,
            "language_code": ord(product_fru_data[2: 3]),
        }
    )
    names = get_product_section_names()
    rc, data = extract_values(product_fru_data, 3, names)
    if rc != RcCode.SUCCESS:
        return RcCode.FAILURE, None
    product_info.update(data)
    return RcCode.SUCCESS, product_info


def make_product_area(product_fru_info):
    product = get_default_product_section()
    product.update(product_fru_info)

    out = struct.pack("B", product["language_code"])

    fields = get_product_section_names()
    for key in fields:
        if product[key]:
            value = product[key].encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
        else:
            out += struct.pack("B", 0)
    if isinstance(product["custom_fields"], (list, tuple)):
        for record in product["custom_fields"]:
            value = record.encode("ascii")
            out += struct.pack("B%ds" % len(value), len(value) | 0xC0, value)
    out += struct.pack("B", 0xC1)

    while len(out) % 8 != 5:
        out += struct.pack("B", 0)

    out = struct.pack("BB", product["format_version"], (len(out) + 3) // 8) + out

    out += struct.pack("B", (0 - sum(bytearray(out))) & 0xFF)

    return RcCode.SUCCESS, out


def make_pad_area_data(pad_size):
    return RcCode.SUCCESS, struct.pack("B" * pad_size, *[0] * pad_size)
