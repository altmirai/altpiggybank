import datetime
import json
import click


def addr_view(**data):
    vkhandle = data['vkhandle']
    address = data['address']
    confirmed_balance = data['confirmed_balance']
    now = datetime.datetime.now()

    click.echo('')
    click.secho(f'File addr{vkhandle}.json created', fg='red')
    click.secho(f'File {vkhandle}.csv created', fg='red')

    click.echo('')
    click.secho(f"Address: {address}", fg='blue')
    click.secho(
        f"Confirmed Balance(SAT): {confirmed_balance} as of {now.strftime('%X')} {now.strftime('%x')}", fg='blue')
    click.echo('')


def show_address_view(**data):
    vkhandle = data.get('vkhandle')
    address = data.get('address')
    confirmed_balance = data.get('confirmed_balance')

    now = datetime.datetime.now()

    click.echo('')
    click.secho(f'File {vkhandle}.csv created', fg='red')

    click.echo('')
    click.secho(f"Address: {address}", fg='blue')
    click.secho(
        f"Confirmed Balance(SAT): {confirmed_balance} as of {now.strftime('%X')} {now.strftime('%x')}", fg='blue')
    click.echo('')


def fee_estimate_view(estimates, n_inputs, n_outputs, address):
    click.echo('')
    click.secho(
        f'The fee estimates for a transaction for {address} with {n_inputs} inputs and {n_outputs} outputs are:', fg='blue')
    click.echo('')
    for urgency, est in estimates.items():
        click.secho(f'{urgency}: {est} sat', fg='blue')
    click.echo('')


def unsigned_tx_view(messages, vkhandle, skhandle):
    click.echo('')
    n = 1
    while n < len(messages)+1:
        click.secho(f'File unsignedTx{vkhandle}_{n}.bin created', fg='red')
        n += 1
    click.secho(f'File tx{vkhandle}.json created', fg='red')
    click.echo('')
    aws_cloudHsm_instructions(messages, vkhandle, skhandle)


def aws_cloudHsm_instructions(messages, vkhandle, skhandle):
    click.secho('AWS cloudHsm instructions:', bold=True, fg='blue')
    click.secho('1. Log into your cloudHSM', fg='blue')
    click.secho(
        '2. Run the following to sign your unsigned raw transaction(s):', fg='blue')
    click.echo('')
    n = 1
    while n < len(messages)+1:
        click.secho(
            f'sign -f unsignedTx{vkhandle}_{n}.bin -k {skhandle} -m 17 -out signedTx{vkhandle}_{n}.der', fg='green')
        n += 1
    click.echo('')
    click.secho('3. Run the following to verify your signature(s):', fg='blue')
    click.echo('')
    n = 1
    while n < len(messages)+1:
        click.secho(
            f'verify -f unsignedTx{vkhandle}_{n}.bin -s signedTx{vkhandle}_{n}.der -k {vkhandle} -m 17', fg='green')
        n += 1
    click.echo('')


def signed_tx_view(hex):
    click.echo('')
    click.secho(
        'Copy and past the below raw transaction into a third-party broadcast transaction service.', fg='blue')
    click.echo('')
    click.secho(hex, fg="green")
    click.echo('')

    # if config.verify:
    #     click.echo('')
    #     click.secho('Below are console script(s) that convert hex formated unsigned raw transacton(s) to binary and create file(s) to sign. They are in hex format below, so they can be decoded to verify the details before signing. Your unsigned raw transaction is the stuff between the two quatation marks. See www.altmirai.com for more information.', fg='blue')
    #     click.echo('')
    #     n = 1
    #     for msg in messages:
    #         click.secho(
    #             f'echo "{msg.hex()}" | xxd -r -p | openssl dgst -sha256 -binary -m 17 -out unsignedRawTx{vkhandle}_{n}.bin', fg='green')
    #         click.echo('')
    #         n += 1
    #     click.secho('Once you have verified your unsigned raw transaction(s), copy and paste the entire script (one at a time, if more that one) in the terminal and hit enter. Then follow the next steps.', fg="blue")
    #     click.echo('')
    #     next_steps(messages)
