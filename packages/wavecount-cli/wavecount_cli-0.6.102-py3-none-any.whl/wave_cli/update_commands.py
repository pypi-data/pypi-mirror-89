from wave_cli import COMMAND_NAME
import click
import re
import inquirer as inq

from wave_cli.services.backend_services import Backend


@click.command(name='update', help='Update devices. Use options to filter devices')
@click.pass_context
@click.argument('args', nargs=1, default=None, required=False)
@click.option('-v', '--firmware-version', help='Firmware version', is_eager=True)
@click.option('-sn', '--serial-number', help='Device serial number', default=None, is_eager=True)
@click.option('-id', '--device-id', help='Device id', default=None, is_eager=True)
@click.option('-n', '--device-name', help='Device name', default=None, is_eager=True)
@click.option('-c', '--company', help='Company name', default=None, is_eager=True)
@click.option('-st', '--store', help='Store name', default=None, is_eager=True)
@click.option('-stn', '--store-number', help='Store number', default=None, is_eager=True)
@click.option('-cl', '--cluster', help='Cluster name', default=None, is_eager=True)
def update(ctx, args, firmware_version, serial_number, device_id, device_name, company, store, store_number, cluster):
    force_update = False
    if args == 'force':
        force_update = True
    answer = inq.prompt(
        raise_keyboard_interrupt=True,
        questions=[
            inq.Text(
                name='desired_version',
                message='Enter firmware version to update'
            )
        ]
    )
    desired_version = answer['desired_version']
    if not firmware_version and \
            not serial_number and \
            not device_id and \
            not device_name and \
            not company and \
            not store and \
            not store_number and \
            not cluster:
        confirmation = inq.confirm(message='Are you trying update all devices?')
        if not confirmation:
            click.secho(message='\nBye!')
            exit(1)
        answer = inq.prompt(
            raise_keyboard_interrupt=True,
            questions=[
                inq.Text(
                    name='re_desired_version',
                    message='So to confirm, type firmware version again [{0}]'.format(desired_version),
                )
            ]
        )
        re_desired_version = answer['re_desired_version']
        if desired_version != re_desired_version:
            click.secho('Not matched!', fg='red')
            exit(1)
    backend = Backend(ctx)
    data = {
      "firmwareVersion": firmware_version,
      "deviceId": device_id,
      "store": store,
      "storeNumber": store_number,
      "cluster": cluster,
      "company": company,
      "serialNumber": serial_number,
      "desiredVersion": desired_version,
      "deviceName": device_name,
      "forceUpdate": force_update
    }
    result = backend.update_devices(data)
    click.secho("")
    for key in result:
        row_length = 25
        splitted_key = re.findall('.[^A-Z]*', key)
        cap_splitted_key = [k.capitalize() for k in splitted_key]
        joined = ' '.join(cap_splitted_key)
        txt = "  {0}:".format(joined) + ' ' * (row_length - len(joined)) + "{0}".format(result[key])
        click.secho(txt, bold=True, fg='blue')
    click.secho()
    click.secho("Run `{0} show device` to tracking update states.".format(COMMAND_NAME))
    click.secho()
