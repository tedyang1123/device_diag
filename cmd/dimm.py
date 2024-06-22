#!/usr/bin/env python3
import click

from cmd.utility.cli_utility import DiagCommandGroup, cli_cmd_support_check
from cmd.utility.cmd_utility import cli_cmd_output
from common.rc_code import RcCode
from machine.device import DeviceSystem
from src.ui.dimm_ui import DimmUi


@click.group(cls=DiagCommandGroup)
@click.pass_context
def cli(ctx):
    """
    Command Line Utility For DIMM Diagnostic
    """
    ctx.obj = DeviceSystem()


@cli.command('info', short_help='dimm info, display DIMM information',
             cli_support=cli_cmd_support_check("dimm", "dimm"))
@click.pass_context
def dimm_info(ctx):
    """
    Display CPU information
    """
    rc, data = DimmUi(ctx.obj.device_board_list_get()).dimm_ui_info_get()
    if rc != RcCode.SUCCESS:
        click.echo("Get DIMM information fail. Fail code {}".format(RcCode.covert_rc_to_string(rc)))
        return
    cli_cmd_output(data)


@cli.command('util', short_help='cpu util, display cpu utilization',
             cli_support=cli_cmd_support_check("dimm", "dimm_util"))
@click.pass_context
def dimm_util(ctx):
    """
    Display CPU Utilization
    """
    rc, data = DimmUi(ctx.obj.device_board_list_get()).dimm_ui_util_get()
    if rc != RcCode.SUCCESS:
        click.echo("Get DIMM utilization fail. Fail code {}".format(RcCode.covert_rc_to_string(rc)))
        return
    cli_cmd_output(data)


if __name__ == "__main__":
    cli()