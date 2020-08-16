from hashlib import sha256
from unittest import mock
from click.testing import CliRunner
import datetime
import os
import pytest

from src.controllers import create_address, create_fee
from src.models import UnsignedTx, SignedTx
from src.files import read_signature_files, excel_date
from tests.test_data import TestDataOne, MockFeeEstOne
from src.routes import addr, main


t = TestDataOne()
fee_estimate = MockFeeEstOne()

# TEST CREATE P2PKH ADDRESS FROM PEM
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
def test_create_addr(*args):

    file = open(t.pub_key_file_name, 'rb')
    pem = file.read()
    file.close()

    resp = create_address(pem=pem)['data']

    assert(resp['address'] == t.address)
    assert(resp['confirmed_balance'] == t.confirmed_balance)


# TEST CREATE FEE ESTIMATE
@mock.patch('src.controllers.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.adapters.requests.get', return_value=fee_estimate, autospec=True)
def test_fee(*args):
    resp = create_fee(address=t.address, all=all)

    assert(resp['estimates'] == t.mock_fees['estimates'])


# TEST CREATE TOSIGN TXS
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
def test_tosign_tx(*args):
    file = open(t.pub_key_file_name, 'rb')
    pem = file.read()
    file.close()

    unsigned_tx = UnsignedTx(
        pem=pem,
        recipient=t.recipient,
        fee=t.fee,
        value=t.value,
        change_address=t.change_address
    )

    tosign_tx = []
    for msg in unsigned_tx.messages:
        tosign_tx.append(msg['message'].hex())

    # TEST FOR TO_SIGN IF TX_INPUTS ARE SORTED DIFFERENTLY (THERE IS NO "CORRECT" OR CONVENTION FOR SORTING)
    # tosign_tx_test_data_parts = []
    # for item in t.tosign_tx:
    #     tosign_tx_test_data_parts += item[10:].split('ffffffff')
    # tosign_tx_test_data_parts.sort()

    # tosign_tx_parts = []
    # for item in tosign_tx:
    #     tosign_tx_parts += item[10:].split('ffffffff')
    # tosign_tx_parts.sort()
    # assert(tosign_tx_parts == tosign_tx_test_data_parts)

    tosigns = unsigned_tx.to_sign
    tosign = []
    for item in tosigns:
        hashed = sha256(item).digest()
        tosign.append(hashed.hex())
    tosign.sort()

    tosign_test_data = t.tosign
    tosign_test_data.sort()

    assert(tosign_tx == t.tosign_tx)
    assert(tosign == tosign_test_data)


# TEST CREATE SIGNED TRANSACTION HEX
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
def test_tx_hex(*args):
    file = open(t.pub_key_file_name, 'rb')
    pem = file.read()
    file.close()

    unsigned_tx = UnsignedTx(pem, t.recipient, t.fee,
                             t.value, t.change_address)

    signatures = read_signature_files(t.signature_files, t.aws)

    signed_tx = SignedTx(pem, unsigned_tx, signatures)

    assert(signed_tx.hex == t.tx_hex)
