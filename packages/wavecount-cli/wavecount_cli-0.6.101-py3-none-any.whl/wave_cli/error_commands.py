import click
import datetime

from wave_cli.services.backend_services import Backend


@click.group(name='error', help='Device internal error managements.')
def error():
    pass


@click.command(name='show', help='Show avtive errors.')
@click.pass_context
def show(ctx):
    backend_service = Backend(ctx)
    ef_list = backend_service.get_error_flags()
    row_len = 114
    block_len = round(row_len / 6)
    sep = '│'
    t_dId = ' Device Id'
    t_com = ' Company'
    t_sto = ' Store'
    t_stn = ' Store Number'
    t_err = ' Error'
    t_dte = ' Date'
    click.secho('┌' + '─' * (row_len - 5) + '┐', fg='blue')
    click.secho(sep + t_dId + ' ' * (block_len - len(t_dId) - 4) +
                sep + t_com + ' ' * (block_len - len(t_com) - 4) +
                sep + t_sto + ' ' * (block_len - len(t_sto) - 4) +
                sep + t_stn + ' ' * (block_len - len(t_stn) - 4) +
                sep + t_err + ' ' * (block_len - len(t_err) + 6) +
                sep + t_dte + ' ' * (block_len - len(t_dte)) +
                sep, fg='blue')
    click.secho('╞' + '═' * (row_len - 5) + '╡', fg='blue')
    prev_dId = ''
    for ef in ef_list:
        for f in ef['errorFlags']:
            if len(ef['deviceId']) < len(t_dId + ' ' * (block_len - len(t_dId) - 4)):
                dId = ' {0}'.format(ef['deviceId'])
            else:
                dId = ' {0}..'.format(ef['deviceId'][0:(len(t_dId + ' ' * (block_len - len(t_dId) - 4)) - 3)])
            if len(ef['company']) < len(t_com + ' ' * (block_len - len(t_com) - 4)):
                com = ' {0}'.format(ef['company'])
            else:
                com = ' {0}..'.format(ef['company'][0:(len(t_com + ' ' * (block_len - len(t_com) - 4)) - 3)])
            if len(ef['store']) < len(t_sto + ' ' * (block_len - len(t_sto) - 4)):
                sto = ' {0}'.format(ef['store'])
            else:
                sto = ' {0}..'.format(ef['store'][0:(len(t_sto + ' ' * (block_len - len(t_sto) - 4)) - 3)])
            if len(ef['storeNumber']) < len(t_stn + ' ' * (block_len - len(t_stn) - 4)):
                stn = ' {0}'.format(ef['storeNumber'])
            else:
                stn = ' {0}..'.format(ef['storeNumber'][0:(len(t_stn + ' ' * (block_len - len(t_stn) - 4)) - 3)])
            if len(f) < len(t_err + ' ' * (block_len - len(t_err) + 6)):
                err = ' {0}'.format(f)
            else:
                err = ' {0}..'.format(f[0:(len(t_err + ' ' * (block_len - len(t_err) + 6))) - 3])
            localeDate = datetime.datetime.fromtimestamp(ef['errorFlags'][f]).strftime('%Y-%m-%d %H:%M')
            if len(localeDate) < len(t_dte + ' ' * (block_len - len(t_dte) + 4)):
                dte = ' {0}'.format(localeDate)
            else:
                dte = ' {0}..'.format(ef['errorFlags'][f][0:(len(t_dte + ' ' * (block_len - len(t_dte) + 5)) - 3)])
            if prev_dId != ef['deviceId']:
                click.secho(sep + dId + ' ' * (block_len - len(dId) - 4) +
                            sep + com + ' ' * (block_len - len(com) - 4) +
                            sep + sto + ' ' * (block_len - len(sto) - 4) +
                            sep + stn + ' ' * (block_len - len(stn) - 4) +
                            '├' + err + ' ' * (block_len - len(err) + 6) +
                            sep + dte + ' ' * (block_len - len(dte)) +
                            sep, fg='blue')
            else:
                if len(f) <= len(t_err + ' ' * (block_len - len(t_err) + 6)):
                    err = ' {0}'.format(f)
                else:
                    err = ' {0}..'.format(f[0:len(t_err + ' ' * (block_len - len(t_err) + 5))])
                click.secho(sep + ' ' * (3 * block_len + 6) +
                            '├' + err + ' ' * (block_len - len(err) + 6) +
                            sep + dte + ' ' * (block_len - len(dte)) +
                            sep, fg='blue')
            prev_dId = ef['deviceId']
        click.secho('├' + '─' * (row_len - 5) + '┤', fg='blue')
    click.echo()


error.add_command(show)
