import click
import sys
import os
import pyfiglet

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from wave_cli import PACKAGE_NAME, VERSION
from wave_cli.utils import read_config, save_config
from wave_cli.new_device_commands import new
from wave_cli.show_commands import show
from wave_cli.update_commands import update
from wave_cli.version_check import compare
from wave_cli.reset_command import reset
from wave_cli.reboot_commands import reboot
from wave_cli.delete_command import delete
from wave_cli.device_logs_commands import log
from wave_cli.services.backend_services import Backend


@click.group(name='main', add_help_option=False, help='Wavecount CLI for controlling and monitoring wavecount stuff.')
@click.pass_context
def main(ctx):
    compare()
    ctx.obj = read_config()
    if 'access_token' not in ctx.obj:
        ctx.forward(sync)
        exit()
    pass


@click.command('sync', help='Synchronize cache.')
@click.option('-T', '--access-token', type=click.STRING, help='Your access token')
@click.pass_context
def sync(ctx, access_token):
    if not access_token and 'access_token' not in ctx.obj:
        ctx.obj['access_token'] = click.prompt('Your Access Token', type=click.STRING)
    elif access_token:
        ctx.obj['access_token'] = access_token
    backend_service = Backend(ctx)
    result = backend_service.sync_cache()
    ctx.obj['customers'] = result
    save_config(ctx.obj)


@click.command('login', help='Authorize user.')
@click.option('-T', '--access-token', prompt='Your Access Token', type=click.STRING, help='Your access token')
@click.pass_context
def login(ctx, access_token):
    ctx.obj['access_token'] = access_token
    ctx.forward(sync)
    text_logo = 'wavecount cli'
    pyfiglet.print_figlet(text=text_logo, font='big', justify='center', colors='LIGHT_MAGENTA')


@click.command('version', help='Show {0} version.'.format(PACKAGE_NAME))
@click.pass_context
def version(ctx):
    message = 'using version: {0}'.format(VERSION)
    click.secho(message, fg='bright_black')


main.add_command(sync)
main.add_command(login)
main.add_command(show)
main.add_command(new)
main.add_command(update)
main.add_command(reboot)
main.add_command(delete)
main.add_command(reset)
main.add_command(version)
main.add_command(log)

if __name__ == '__main__':
    main()
