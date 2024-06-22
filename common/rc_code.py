from enum import IntEnum, auto


class RcCode(IntEnum):
    SUCCESS = 0
    FAILURE = auto()
    ERROR = auto()
    NOT_SUPPORT = auto()
    REQUEST_DENIED = auto()
    FILE_NOT_FOUND = auto()
    FILE_NOT_READ = auto()
    FILE_NOT_WRITE = auto()
    FILE_NOT_CREATE = auto()
    FILE_ACCESS_FAIL = auto()
    SIGNATURE_VERIFICATION_FAIL = auto()
    CHECKSUM_VERIFICATION_FAIL = auto()
    INVALID_VALUE = auto()
    INVALID_TYPE = auto()
    NOT_FOUND = auto()

    @classmethod
    def covert_rc_to_string(cls, rc):
        if rc == cls.SUCCESS:
            return "SUCCESS"
        elif rc == cls.FAILURE:
            return "FAILURE"
        elif rc == cls.ERROR:
            return "ERROR"
        elif rc == cls.NOT_SUPPORT:
            return "NOT_SUPPORT"
        elif rc == cls.REQUEST_DENIED:
            return "REQUEST_DENIED"
        elif rc == cls.FILE_NOT_FOUND:
            return "FILE_NOT_FOUND"
        elif rc == cls.FILE_NOT_READ:
            return "FILE_NOT_READ"
        elif rc == cls.FILE_NOT_WRITE:
            return "FILE_NOT_WRITE"
        elif rc == cls.FILE_NOT_CREATE:
            return "FILE_NOT_CREATE"
        elif rc == cls.FILE_ACCESS_FAIL:
            return "FILE_ACCESS_FAIL"
        elif rc == cls.SIGNATURE_VERIFICATION_FAIL:
            return "SIGNATURE_VERIFICATION_FAIL"
        elif rc == cls.CHECKSUM_VERIFICATION_FAIL:
            return "SIGNATURE_VERIFICATION_FAIL"
        elif rc == cls.INVALID_VALUE:
            return "INVALID_VALUE"
        elif rc == cls.INVALID_TYPE:
            return "INVALID_TYPE"
        elif rc == cls.NOT_FOUND:
            return "NOT_FOUND"
        else:
            return None


