#!/usr/bin/env python3
import click

from cmd.utility.cli_utility import DiagCommandGroup, cli_cmd_support_check
from cmd.utility.cmd_utility import cli_cmd_output
from common.rc_code import RcCode
from machine.device import DeviceSystem
from src.ui.cpu_ui import CpuUi


@click.group(cls=DiagCommandGroup)
@click.pass_context
def cli(ctx):
    """
    Command Line Utility For CPU Diagnostic
    """
    ctx.obj = DeviceSystem()


@cli.command('info', short_help='cpu info, display cpu information',
             cli_support=cli_cmd_support_check("cpu", "cpu_info"))
@click.pass_context
def cpu_info(ctx):
    """
    Display CPU information
    """
    rc, data = CpuUi(ctx.obj.device_board_list_get()).cpu_ui_info_get()
    if rc != RcCode.SUCCESS:
        click.echo("Get CPU information fail. Fail code {}".format(RcCode.covert_rc_to_string(rc)))
        return
    cli_cmd_output(data)


@cli.command('util', short_help='cpu util, display cpu utilization',
             cli_support=cli_cmd_support_check("cpu", "cpu_util"))
@click.pass_context
def cpu_util(ctx):
    """
    Display CPU Utilization
    """
    rc, data = CpuUi(ctx.obj.device_board_list_get()).cpu_ui_util_get()
    if rc != RcCode.SUCCESS:
        click.echo("Get CPU utilization fail. Fail code {}".format(RcCode.covert_rc_to_string(rc)))
        return
    cli_cmd_output(data)


if __name__ == "__main__":
    cli()