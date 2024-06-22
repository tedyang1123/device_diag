#!/usr/bin/env python3
import click

from cmd.utility.cli_utility import DiagCommandGroup, cli_cmd_support_check
from cmd.utility.cmd_utility import cli_cmd_output
from common.rc_code import RcCode
from machine.device import DeviceSystem
from src.ui.ssd_ui import SsdUi


@click.group(cls=DiagCommandGroup)
@click.pass_context
def cli(ctx):
    """
    Command Line Utility For SSD Diagnostic
    """
    ctx.obj = DeviceSystem()


@cli.command('info', short_help='ssd info, display ssd information',
             cli_support=cli_cmd_support_check("ssd", "ssd_info"))
@click.pass_context
def ssd_info(ctx):
    """
    Display SSD information
    """
    rc, data = SsdUi(ctx.obj.device_board_list_get()).ssd_ui_info_get()
    if rc != RcCode.SUCCESS:
        click.echo("Get SSD information fail. Fail code {}".format(RcCode.covert_rc_to_string(rc)))
        return
    cli_cmd_output(data)
