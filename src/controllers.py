import datetime
import hashlib
import json


from src.adapters import get_fee_estimate, get_tx_inputs
from src.bitcoin_addresses import P2PKH
from src.models import SignedTx, SigScript, UnsignedTx


# ADDRESS CONTROLLERS
def create_address(**data):
    p2pkh = P2PKH(data.get('pem'))
    address = p2pkh.address
    confirmed_balance = p2pkh.confirmed_balance
    resp = {'data': {'address': address, 'confirmed_balance': confirmed_balance}}

    return resp


# FEE CONTROLLERS
def create_fee(**data):
    n_inputs = len(get_tx_inputs(data['address']))
    n_outputs = 1 if data['all'] else 2
    estimates = get_fee_estimate(n_inputs, n_outputs)

    return {'estimates': estimates, 'n_inputs': n_inputs, 'n_outputs': n_outputs}


# TRANSACTION CONTROLLERS
def create_unsigned_tx(**data):
    to_sign = UnsignedTx(
        data['pem'],
        data['recipient'],
        data['fee'],
        data['value'],
        data['change_address']).to_sign

    return to_sign


def create_signed_tx(**data):
    unsigned_tx = UnsignedTx(
        data['pem'],
        data['recipient'],
        data['fee'],
        data.get('value'),
        data.get('change_address')
    )

    signedTx = SignedTx(data['pem'], unsigned_tx, data['signatures'])

    return signedTx.hex
