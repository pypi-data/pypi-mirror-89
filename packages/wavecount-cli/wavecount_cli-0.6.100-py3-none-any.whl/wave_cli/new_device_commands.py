import click
import inquirer as inq
from inquirer import themes

from wave_cli.utils import save_config
from wave_cli.services.backend_services import Backend
from wave_cli.services.validate_services import int_validate, serial_number_validate, string_validate


@click.command(name='new', help='Register a new device.')
@click.pass_context
def new(ctx):
    company_choices = ['new']
    backend_service = Backend(ctx)
    result = backend_service.sync_cache()
    ctx.obj['customers'] = result
    customers = ctx.obj['customers']
    company_choices.extend(customers)
    answer = inq.prompt(
        questions=[
            inq.Text(
                name='serial_number',
                message='Enter serial number',
                validate=serial_number_validate
            )
        ],
        raise_keyboard_interrupt=True,
        theme=themes.GreenPassion()
    )
    serial_number: str = answer['serial_number']
    backend_service = Backend(context=ctx)
    answer = inq.prompt(
        theme=themes.GreenPassion(),
        raise_keyboard_interrupt=True,
        questions=[
            inq.List(
                name='company',
                message='Enter company name',
                choices=company_choices,
                default='new',
            )
        ],
    )
    company: str = answer['company']
    if company == 'new':
        answers = inq.prompt(
            theme=themes.GreenPassion(),
            raise_keyboard_interrupt=True,
            questions=[
                inq.Text(
                    name='company',
                    message='Enter new company name',
                    validate=string_validate,
                ),
                inq.Text(
                    name='store',
                    message='Enter new store name',
                    validate=string_validate,
                ),
                inq.Text(
                    name='store_number',
                    message='Enter store number',
                    validate=int_validate,
                ),
            ],
        )
        company: str = answers['company']
        customers[company] = {}
        store: str = answers['store']
        store_number: str = answers['store_number']
        customers[company][store] = store_number
        save_config(ctx.obj)
    else:
        store_choices = ['new']
        store_choices.extend(sorted(customers[company].keys()))
        answer = inq.prompt(
            theme=themes.GreenPassion(),
            raise_keyboard_interrupt=True,
            questions=[
                inq.List(
                    name='store',
                    message='Enter store name',
                    choices=store_choices,
                    default='new'
                )
            ],
        )
        store: str = answer['store']
        if store == 'new':
            answer = inq.prompt(
                theme=themes.GreenPassion(),
                raise_keyboard_interrupt=True,
                questions=[
                    inq.Text(
                        name='store',
                        message='Enter new store name',
                        validate=string_validate,
                    ),
                    inq.Text(
                        name='store_number',
                        message='Enter store number',
                        validate=int_validate,
                    ),
                ],
            )
            customers[company] = {}
            store: str = answer['store']
            store_number: str = answer['store_number']
            customers[company][store] = store_number
            save_config(ctx.obj)
        else:
            store_number: str = customers[company][store]
    data = {
        'store': store,
        'company': company,
        'storeNumber': store_number,
        'serialNumber': serial_number,
    }
    device = backend_service.register_device(data)
    dev_id = device['deviceId']
    prim_key = device['primaryKey']
    comp = device['company']
    store = device['store']
    store_num = device['storeNumber']
    sn = device['serialNumber']
    click.secho(' serial number:  {}'.format(sn), fg='green')
    click.secho(' device id:      {}'.format(dev_id), fg='green')
    click.secho(' primary key:    {}'.format(prim_key), fg='green')
    click.secho(' company:        {}'.format(comp), fg='green')
    click.secho(' store:          {}'.format(store), fg='green')
    click.secho(' store number:   {}'.format(store_num), fg='green')
    click.secho()
