import click
from wave_cli.services.backend_services import Backend


@click.command(name='delete', help='Delete devices. Use options to filter devices')
@click.pass_context
@click.option('-sn', '--serial-number', help='Device serial number')
@click.option('-id', '--device-id', help='Device id', default=None)
def delete(ctx, serial_number, device_id):
    if not serial_number and not device_id:
        serial_number = click.prompt(text='Enter serial number')
    backend = Backend(ctx)
    query_params = {
      "deviceId": device_id,
      "serialNumber": serial_number,
    }
    dev = backend.get_devices_list(query_params)
    if len(dev) == 0:
        click.secho('  DEVICE WAS NOT FOUND!', fg='yellow')
        exit(1)
    confirm = click.confirm(click.style('  Are you sure to delete the device of "{0}" ?'.format(dev[0]['store']), fg='yellow'), default=False)
    if confirm:
        backend.delete_device(query_params)
        click.secho('  Device with {0} is deleted'.format(
            'serial-number ' + serial_number if serial_number else 'id ' + device_id), fg='yellow'
        )
