import click
import inquirer as inq
from inquirer import themes
from datetime import date, timedelta

from wave_cli.services.backend_services import Backend
from wave_cli.services.validate_services import date_validate, serial_number_validate


@click.command(name='log', help='Get device log. Use options')
@click.pass_context
@click.argument('args', nargs=1, default=None, required=False)
@click.option('-sn', '--serial-number', help='Device serial-number', default=None, is_eager=True)
@click.option('-id', '--device-id', help='Device id', default=None, is_eager=True)
@click.option('-fd', '--from-date', help='From date', default=None, is_eager=True)
@click.option('-td', '--to-date', help='To date', default=None, is_eager=True)
def log(ctx, args, serial_number, device_id, from_date, to_date):
    force_get_log = False
    if args == 'force':
        force_get_log = True
    questions = []
    if not serial_number and not device_id:
        questions.append(
            inq.Text(
                name='serial_number',
                message='Enter device "serial-number"',
                validate=serial_number_validate,
            )
        )
    if not from_date:
        questions.append(
            inq.Text(
                name='from_date',
                message='Enter "start-date". format <YYYY-MM-DD>',
                default=str(date.today() - timedelta(days=1)),
                validate=date_validate
            )
        )
    if not to_date:
        questions.append(
            inq.Text(
                name='to_date',
                message='Enter "end-date". format <YYYY-MM-DD>',
                default=str(date.today()),
                validate=date_validate
            )
        )
    questions.append(
        inq.Checkbox(
            name='targets',
            message='Select targets',
            choices=[('Azure', 'azure'), ('Frames', 'frames'), ('Panel', 'panel'), ('Sensor', 'sensor')],
            default=['azure', 'frames', 'panel', 'sensor']
        )
    )
    answers = inq.prompt(
        questions=questions,
        raise_keyboard_interrupt=True,
        theme=themes.GreenPassion()
    )
    backend = Backend(ctx)
    body = {
      'forceGetLog': force_get_log,
      'deviceId': device_id,
      'serialNumber': serial_number if serial_number or device_id else answers['serial_number'],
      'from': from_date if from_date else answers['from_date'],
      'to': to_date if to_date else answers['to_date'],
      'targets': answers['targets'],
    }
    blob_data = backend.request_device_logs(body)
    blob_name = blob_data['blobName']
    file_dir = backend.download_device_logs(blob_name)
    click.secho('  Saved at {}'.format(file_dir), fg='green')
