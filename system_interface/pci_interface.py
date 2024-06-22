from pypcie import Device

from common.rc_code import RcCode


class PciInterface:
    def __init__(self, device_id, bar_num):
        self._device_id = device_id
        self._bar_num = bar_num

    def pic_interface_byte_read(self, offset:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            val = bar.read(offset)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, val & 0xFF

    def pic_interface_byte_write(self, offset:int, value:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            val = bar.read(offset)
            bar.write(offset, (val & 0xFFFFFF00) | (value & 0xFF))
        except ValueError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def pic_interface_word_read(self, offset:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            val = bar.read(offset)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, val & 0xFFFF

    def pic_interface_half_write(self, offset:int, value:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            val = bar.read(offset)
            bar.write(offset, (val & 0xFFFF0000) | (value & 0xFFFF))
        except ValueError:
            return RcCode.FAILURE
        return RcCode.SUCCESS

    def pic_interface_half_read(self, offset:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            val = bar.read(offset)
        except ValueError:
            return RcCode.FAILURE, None
        return RcCode.SUCCESS, val & 0xFFFF

    def pic_interface_word_write(self, offset:int, value:int):
        try:
            device = Device(self._device_id)
            bar = device.bar[self._bar_num]
            bar.write(offset, value)
        except ValueError:
            return RcCode.FAILURE
        return RcCode.SUCCESS
