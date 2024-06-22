import datetime

from common.rc_code import RcCode
from src.lib.fru.share_lib import get_default_common_section, get_default_board_section, get_default_chassis_section, \
    get_default_product_section

min_date = datetime.datetime(1996, 1, 1, 0, 0)  # 0x000000
max_date = datetime.datetime(2027, 11, 24, 20, 15)  # 0xffffff


def convert_str_to_minutes(stamp):
    try:
        date = datetime.datetime.strptime(stamp, "%Y-%m-%d %H:%M")
    except ValueError:
        return RcCode.FAILURE, "The date {} must follow the format \"YYYY-MM-DD HH:MM\"".format(stamp)
    if date < min_date:
        return RcCode.FAILURE, "The date/time {} must be at least 1996-01-01 00:00".format(stamp)
    if date > max_date:
        return RcCode.FAILURE, "The date/time {} must be at most 2027-11-24 20:15".format(stamp)
    return RcCode.SUCCESS, int((date - min_date).total_seconds()) // 60


def convert_minutes_to_str(minutes):
    if minutes < 0:
        return RcCode.FAILURE, "*minutes* must be >= 0 (got {})".format(minutes)
    if minutes > 0xFFFFFF:
        return RcCode.FAILURE, "*minutes* must be <= 0xffffff (got 0x{:x})".format
    date = min_date + datetime.timedelta(minutes=minutes)
    return RcCode.SUCCESS, date.strftime("%Y-%m-%d %H:%M")


def repr_(value):
    if isinstance(value, bool):
        return RcCode.SUCCESS, str(bool(value)).lower()
    elif isinstance(value, int):
        return RcCode.SUCCESS, value
    elif isinstance(value, str):
        value = value.replace("\\", "\\\\")
        value = value.replace('"', '\\"')
        return RcCode.SUCCESS, "{}".format(value)
    elif isinstance(value, list):
        result = []
        for v in value:
            rc, val = repr_(v)
            if rc != RcCode.SUCCESS:
                return rc, val
            result.append("{},".format(v))
        output = " ".join(result).rstrip(",")
        return RcCode.SUCCESS, "[{}]".format(output)
    return RcCode.FAILURE, "Unable to represent {} (type={}) in the TOML format".format(repr(value), type(value))


def repr_internal(value: bytes):
    if not value:
        return RcCode.SUCCESS, ""
    return RcCode.SUCCESS, str(value, encoding='utf-8')


def pre_process_fru_config(fru_config):
    integers = (
        ("common", "format_version"),
        ("board", "language_code"),
        ("chassis", "type"),
        ("product", "language_code"),
    )
    dates = (("board", "mfg_date_time"),)

    # Standardize integer values.
    for section, key in integers:
        if not isinstance(fru_config.get(section, {}).get(key, 0), int):
            try:
                fru_config[section][key] = int(fru_config[section][key], 16)
            except ValueError:
                return RcCode.FAILURE, 'Section [{}] key "{}" must be a number'.format(section, key)

    # Standardize date/time values.
    for section, key in dates:
        if section in fru_config and key in fru_config[section]:
            if not fru_config[section][key]:
                fru_config[section][key] = "1996-01-01 00:00"
            if not isinstance(fru_config[section][key], str):
                return RcCode.FAILURE, 'Section [{}] key "{}" must be a string'.format(section, key)
            rc, date = convert_str_to_minutes(fru_config[section][key])
            if rc != RcCode.SUCCESS:
                return rc, date
            fru_config[section][key] = date

    # Normalize the internal info area data.
    if fru_config.get("internal", {}).get("data"):
        msg = 'Section [internal] key "data" must be a list of numbers or a string'
        try:
            fru_config["internal"]["data"] = bytes(fru_config["internal"]["data"])
        except TypeError:
            try:
                fru_config["internal"]["data"] = fru_config["internal"]["data"].encode("utf8")
            except AttributeError:
                return RcCode.FAILURE, msg
    if "file" in fru_config.get("internal", {}):
        del fru_config["internal"]["file"]
    return RcCode.SUCCESS, fru_config


def post_process_fru_config(data):
    if data is None:
        data = {}
    info = {
        "common": get_default_common_section(),
        "board": get_default_board_section(),
        "chassis": get_default_chassis_section(),
        "product": get_default_product_section(),
    }
    for section in ("common", "board", "chassis", "product"):
        info[section].update(data.get(section, {}))

    # Common
    rc, result = repr_(data.get("common", {}).get("format_version", 1))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["common"]["format_version"] = result

    # Internal
    rc, result = repr_(data.get("internal", {}).get("format_version", 1))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["internal"]["format_version"] = result
    rc, result = repr_internal(data.get("internal", {}).get("data", b""))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["internal"]["data"] = result

    # chassis
    rc, result = repr_(data.get("chassis", {}).get("format_version", 1))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["chassis"]["format_version"] = result
    result = "0x{:02x}".format(data["chassis"]["type"])
    data["chassis"]["type"] = result
    rc, result = repr_(info["chassis"]["format_version"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["chassis"]["format_version"] = result
    rc, result = repr_(info["chassis"]["part_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["chassis"]["part_number"] = result
    rc, result = repr_(info["chassis"]["serial_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["chassis"]["serial_number"] = result
    data["chassis"]["custom_fields"] = info["chassis"]["custom_fields"]

    # board
    rc, result = repr_(data.get("board", {}).get("format_version", 1))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["format_version"] = result
    rc, result = repr_(info["board"]["language_code"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["language_code"] = result
    rc, result = convert_minutes_to_str(info["board"]["mfg_date_time"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["mfg_date_time"] = result
    rc, result = repr_(info["board"]["manufacturer"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["manufacturer"] = result
    rc, result = repr_(info["board"]["product_name"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["product_name"] = result
    rc, result = repr_(info["board"]["serial_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["serial_number"] = result
    rc, result = repr_(info["board"]["part_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["part_number"] = result
    rc, result = repr_(info["board"]["fru_file_id"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["board"]["fru_file_id"] = result
    data["board"]["custom_fields"] = info["board"]["custom_fields"]

    # product
    rc, result = repr_(data.get("product", {}).get("format_version", 1))
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["format_version"] = result
    rc, result = repr_(info["product"]["language_code"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["language_code"] = result
    rc, result = repr_(info["product"]["manufacturer"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["manufacturer"] = result
    rc, result = repr_(info["product"]["product_name"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["product_name"] = result
    rc, result = repr_(info["product"]["part_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["part_number"] = result
    rc, result = repr_(info["product"]["product_version"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["product_version"] = result
    rc, result = repr_(info["product"]["serial_number"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["serial_number"] = result
    rc, result = repr_(info["product"]["asset_tag"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["asset_tag"] = result
    rc, result = repr_(info["product"]["fru_file_id"])
    if rc != RcCode.SUCCESS:
        return rc, result
    data["product"]["fru_file_id"] = result
    data["product"]["custom_fields"] = info["product"]["custom_fields"]

    return RcCode.SUCCESS, data
