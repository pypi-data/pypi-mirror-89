import click

from wave_cli.utils import save_config
from wave_cli.services.backend_services import Backend


@click.group('registry', help='Registry commands management.')
def registry():
    pass


@click.command(name='new', help='Register a new device.')
@click.pass_context
def new(ctx):
    company_choices = ['new']
    customers = ctx.obj['customers']
    company_choices.extend(customers)
    backend_service = Backend(context=ctx)
    company: str = click.prompt(text='Company Name', show_choices=False, type=click.Choice(choices=company_choices, case_sensitive=True))
    if company == 'new':
        company: str = click.prompt(text='Enter New Company Name', type=click.STRING)
        customers[company] = {}
        store: str = click.prompt(text='Enter New Store Name', type=click.STRING)
        store_number: str = click.prompt(text='Store Number', type=click.STRING)
        customers[company][store] = store_number
        device = backend_service.register_device(company, store, store_number)
        save_config(ctx.obj)
    else:
        store_choices = ['new']
        store_choices.extend(customers[company].keys())
        store: str = click.prompt(text='Store Name', type=click.Choice(store_choices, case_sensitive=True), show_choices=False)
        if store == 'new':
            store: str = click.prompt(text='Enter New Store Name', type=click.STRING)
            store_number: str = click.prompt(text='Store Number', type=click.STRING)
            customers[company][store] = store_number
            device = backend_service.register_device(company, store, store_number)
            save_config(ctx.obj)
        else:
            store_number: str = customers[company][store]
            device = backend_service.register_device(company, store, store_number)
    click.secho(' device id:      {}'.format(device['deviceId']), fg='green')
    click.secho(' primary key:    {}'.format(device['primaryKey']), fg='green')
    click.secho(' company:        {}'.format(company), fg='green')
    click.secho(' store:          {}'.format(store), fg='green')
    click.secho(' store number:   {}'.format(store_number), fg='green')
    click.secho()


registry.add_command(new)
