import click


def cli_cmd_output(data_dict: dict, start_column=0):
    empty_dtr = "{empty:10}".format(empty="")
    for key, value in data_dict.items():
        for i in range(start_column):
            click.echo(empty_dtr, nl=False)
        if not isinstance(value, dict):
            click.echo("{key:<20}{value:<60}".format(key=key, value=value))
        else:
            click.echo(key)
            cli_cmd_output(value, start_column + 1)
