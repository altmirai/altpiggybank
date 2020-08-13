import json

import click
import requests

import src.click_help as help
from src.bitcoin_addresses import P2PKH
from src.controllers import (create_address, create_fee, create_signed_tx,
                             create_unsigned_tx)
from src.files import (create_csv_file, create_json_file,
                       create_unsigned_tx_files, read_json_file,
                       read_signature_files)
from src.views import (addr_view, fee_estimate_view, show_address_view,
                       signed_tx_view, unsigned_tx_view)
import src.errors as errors


class Config(object):

    def __init__(self):
        self.path = '.'
        pass


pass_config = click.make_pass_decorator(Config, ensure=True)


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
                          ' NOTE: This argument is mutually exclusive with %s' %
                          self.not_required_if
                          ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        not_required_true = ctx.params.get(self.not_required_if)

        if not_required_true:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                        self.name, self.not_required_if))
            else:
                self.prompt = None
                self.required = False

        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


class VerifySigNumbers(click.Option):
    def __init__(self, *args, **kwargs):
        super(VerifySigNumbers, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        tx_json_file = opts.get('tx_json_file')
        data = read_json_file(tx_json_file)
        n_tx_inputs = data.get('n_tx_inputs')
        signature_files = opts.get('signature_files')
        n_sigs = 0 if signature_files is None else len(signature_files)

        if n_sigs != n_tx_inputs:
            raise click.UsageError(
                f'{tx_json_file} requires {n_tx_inputs} signatures, {n_sigs} provided', ctx)

        return super(VerifySigNumbers, self).handle_parse_result(ctx, opts, args)


@click.group()
def main():
    ''' AltPiggyBank is an open-sourced command line tool that is designed to be deployed in an AWS EC2 instance and enables cloudHSM to be used for secure Bitcoin safekeeping. See www.altmirai.com for more information.'''

    pass


@ main.command()
@click.argument('pem_file', type=click.File('rb'), required=True)
@click.option('-v', 'vkhandle', required=True, prompt="Public key(VK) handle", help=help.v)
@click.option('-s', 'skhandle', required=True, prompt='Private key(SK) handle', help=help.s)
@pass_config
@click.pass_context
def addr(context, config, **kwargs):
    try:
        pem_file_name = kwargs['pem_file'].name
        file = open(f"{config.path}/{pem_file_name}", 'rb')
        pem = file.read()
        file.close()

        resp = create_address(pem=pem)['data']

        create_json_file(
            file_name=f"addr{kwargs['vkhandle']}",
            vkhandle=kwargs['vkhandle'],
            skhandle=kwargs['skhandle'],
            pem=pem
        )

        create_csv_file(
            vkhandle=kwargs['vkhandle'],
            skhandle=kwargs['skhandle'],
            address=resp['address'],
            confirmed_balance=resp['confirmed_balance']
        )

        addr_view(
            vkhandle=kwargs['vkhandle'],
            skhandle=kwargs['skhandle'],
            address=resp['address'],
            confirmed_balance=resp['confirmed_balance']
        )
    except Exception as error:
        errors.addr(error, context, config, **kwargs)


@main.command()
@click.argument('addr_json_file', type=click.File('r'), required=True)
@pass_config
@click.pass_context
def refresh(context, config, **kwargs):
    try:
        addr_file_name = kwargs['addr_json_file'].name
        data = read_json_file(addr_file_name)
        assert data.get(
            'pem') is not None, 'Incorrect file, please provide a JSON formatted addr file created by piggy addr'
        resp = create_address(pem=data['pem'])['data']

        create_csv_file(
            vkhandle=data['vkhandle'],
            skhandle=data['skhandle'],
            address=resp['address'],
            confirmed_balance=resp['confirmed_balance']
        )

        show_address_view(
            vkhandle=data['vkhandle'],
            skhandle=data['skhandle'],
            address=resp['address'],
            confirmed_balance=resp['confirmed_balance']
        )
    except Exception as error:
        errors.refresh(error, context, config, **kwargs)


@main.command()
@click.argument('addr_json_file', type=click.File('r'), required=True)
@click.option('-p', 'partial', is_flag=True, help=help.p)
@click.option('-a', 'all', is_flag=True, required=True, prompt="Send recipient all the BTC in address",
              cls=NotRequiredIf, not_required_if='partial', help=help.a)
@pass_config
@click.pass_context
def fee(context, config, **kwargs):
    try:
        addr_file_name = kwargs['addr_json_file'].name
        data = read_json_file(addr_file_name)
        assert data.get(
            'pem') is not None, 'Incorrect file, please provide a JSON formatted addr file created by piggy addr'

        resp = create_address(
            pem=data['pem']
        )['data']

        fee_data = create_fee(
            all=kwargs['all'],
            address=resp['address']
        )

        fee_estimate_view(
            estimates=fee_data['estimates'],
            n_inputs=fee_data['n_inputs'],
            n_outputs=fee_data['n_outputs'],
            address=resp['address']
        )
    except Exception as error:
        errors.fee(error, context, config, **kwargs)



@main.command()
@click.argument('addr_json_file', type=click.File('r'), required=True)
@click.option('-a', 'all', is_flag=True, required=True, prompt="Send recipient all the BTC in address", cls=NotRequiredIf, not_required_if='partial', help=help.a)
@ click.option('-p', 'partial', is_flag=True, help=help.p)
@click.option('-f', 'fee', type=click.INT, required=True, prompt="Mining Fee", help=help.f)
@click.option('-r', 'recipient', required=True, prompt="Recipient address", help=help.r)
@click.option('-q', 'quantity', type=click.INT, required=True, prompt='Quatity of BTC transfered',
              cls=NotRequiredIf, not_required_if='all', help=help.q)
@click.option('-c', 'change_address', required=True, prompt='Change address',
              cls=NotRequiredIf, not_required_if='all', help=help.c)
@pass_config
@click.pass_context
def tx(context, config, **kwargs):
    try:
        addr_file_name = kwargs['addr_json_file'].name
        data = read_json_file(addr_file_name)
        resp = create_address(pem=data['pem'])['data']

        unsigned_txs = create_unsigned_tx(
            pem=data['pem'],
            recipient=kwargs['recipient'],
            fee=kwargs['fee'],
            value=kwargs['quantity'],
            change_address=kwargs['change_address']
        )

        create_json_file(
            file_name=f"tx{data['vkhandle']}",
            all=kwargs['all'],
            fee=kwargs['fee'],
            recipient=kwargs['recipient'],
            partial=kwargs['partial'],
            vkhandle=data['vkhandle'],
            skhandle=data['skhandle'],
            pem=data['pem'],
            address=resp['address'],
            confrimed_balance=resp['confirmed_balance'],
            n_tx_inputs=len(unsigned_txs)
        )

        create_unsigned_tx_files(unsigned_txs, data['vkhandle'])

        unsigned_tx_view(unsigned_txs, data['vkhandle'], data['skhandle'])

    except Exception as error:
        errors.tx(error, context, config, **kwargs)


@main.command()
@click.argument('tx_json_file', type=click.File('r'), required=True)
@click.option('-aws', 'aws', is_flag=True, required=False, default=True)
@click.option('-sig', 'signature_files', type=click.File('rb'), multiple=True, required=True, cls=VerifySigNumbers)
@pass_config
@click.pass_context
def signed(context, config, **kwargs):
    try:
        tx_file_name = kwargs['tx_json_file'].name
        tx_data = read_json_file(tx_file_name)
        signatures = read_signature_files(
            kwargs.get('signature_files'),
            kwargs.get('aws')
        )

        signed_tx = create_signed_tx(**tx_data, signatures=signatures)

        signed_tx_view(signed_tx)

    except Exception as error:
        errors.signed(error, context, config, **kwargs)
