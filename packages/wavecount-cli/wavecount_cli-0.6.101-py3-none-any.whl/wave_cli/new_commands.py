import click

from wave_cli.utils import save_config
from wave_cli.services.backend_services import Backend


@click.group('new', add_help_option=False)
@click.pass_context
def new(ctx):
    """New command managements."""
    save_config(ctx.obj)
    pass


@click.command(name='device', help='Register a new device.')
@click.pass_context
def device(ctx):
    company_choices = ['new']
    backend_service = Backend(ctx)
    result = backend_service.sync_cache()
    ctx.obj['customers'] = result
    customers = ctx.obj['customers']
    company_choices.extend(customers)
    serial_number: str = click.prompt(text='Serial Number', type=click.STRING)
    backend_service = Backend(context=ctx)
    company: str = click.prompt(text='Company Name', show_choices=False, type=click.Choice(choices=company_choices, case_sensitive=True))
    if company == 'new':
        company: str = click.prompt(text='Enter New Company Name', type=click.STRING)
        customers[company] = {}
        store: str = click.prompt(text='New Store Name', type=click.STRING)
        store_number: str = click.prompt(text='Store Number', type=click.STRING)
        customers[company][store] = store_number
        device = backend_service.register_device(serial_number, company, store, store_number)
        save_config(ctx.obj)
    else:
        store_choices = ['new']
        store_choices.extend(customers[company].keys())
        store: str = click.prompt(text='Store Name', type=click.Choice(store_choices, case_sensitive=True), show_choices=False)
        if store == 'new':
            store: str = click.prompt(text='New Store Name', type=click.STRING)
            store_number: str = click.prompt(text='Store Number', type=click.STRING)
            customers[company][store] = store_number
            device = backend_service.register_device(serial_number, company, store, store_number)
            save_config(ctx.obj)
        else:
            store_number: str = customers[company][store]
            device = backend_service.register_device(serial_number, company, store, store_number)
    dev_id = device['deviceId']
    prim_key = device['primaryKey']
    comp = device['company']
    store = device['store']
    store_num = device['storeNumber']
    sn = device['serialNumber']
    click.secho(' device id:      {}'.format(dev_id), fg='green')
    click.secho(' primary key:    {}'.format(prim_key), fg='green')
    click.secho(' company:        {}'.format(comp), fg='green')
    click.secho(' store:          {}'.format(store), fg='green')
    click.secho(' store number:   {}'.format(store_num), fg='green')
    click.secho(' s/n:            {}'.format(sn), fg='green')
    click.secho()


new.add_command(device)
