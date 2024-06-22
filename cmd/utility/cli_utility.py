import click
import json
import os

from common.rc_code import RcCode

CONFIG_PATH =  "/home/tedyang/new_diag/machine/config/cli_control/"

def cli_cmd_support_check(func_group, func_name):
    cli_control_file = ""
    if func_group == "cpu":
        cli_control_file = "cli_cpu_ctl.json"
    if func_group == "dimm":
        cli_control_file = "cli_dimm_ctl.json"
    if func_group == "ssd":
        cli_control_file = "cli_ssd_ctl.json"
    cmd_list = json.load(open(os.path.join(CONFIG_PATH, cli_control_file), encoding='UTF-8'))
    if cmd_list[func_name] != "y":
        return RcCode.NOT_SUPPORT, "Command is not supported."
    return RcCode.SUCCESS, ""


class DiagCommandGroup(click.Group):
    def __init__(self, *args, **kwargs):
        self.command_class = DiagCommand
        super().__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        kwargs.setdefault('cls', self.command_class)
        return super().command(*args, **kwargs)


class DiagCommand(click.Command):
    def __init__(self, *args, **kwargs):
        self.is_supported_cli = kwargs.pop('cli_support', None)
        super().__init__(*args, **kwargs)
        if self.is_supported_cli is not None and self.is_supported_cli == "n":
            self.hidden = True

    def invoke(self, ctx):
        if self.hidden:
            click.echo("This command is currently unsupported and cannot be invoked.")
            return
        super().invoke(ctx)
