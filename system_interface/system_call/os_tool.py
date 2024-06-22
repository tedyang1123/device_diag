import subprocess
from common.rc_code import RcCode


class OsTool:
    def __init__(self):
        pass

    def os_tool_exec_cmd(self, cmd, shel=False):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shel)
        except subprocess.CalledProcessError:
            return RcCode.FAILURE, None
        rc = RcCode.SUCCESS if result.returncode == 0 else RcCode.FAILURE
        msg = result.stderr if rc == RcCode.SUCCESS else result.stderr
        return rc, msg
