from unittest import mock
from click.testing import CliRunner
import datetime

from src.routes import main, addr, refresh, fee, tx, signed
from tests.test_data import TestDataOne, MockFeeEstOne


t = TestDataOne()


#TEST ADDR STANDARD OUTPUT
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
@mock.patch('src.routes.create_csv_file', return_value=None, autospec=True)
def test_addr(*args):
    runner = CliRunner()
    result = runner.invoke(
        addr, [t.pub_key_file_name, '-v', f'{t.vkhandle}', '-s', f'{t.skhandle}'])
    output = [item for item in result.output.split(sep='\n') if item]
    now = datetime.datetime.now()

    assert result.exit_code == 0
    assert output[0] == f"File addr{t.vkhandle}.json created"
    assert output[1] == f"File {t.vkhandle}.csv created"
    assert output[2] == f"Address: {t.address}"
    assert output[3] == f"Confirmed Balance(SAT): {t.confirmed_balance} as of {now.strftime('%X')} {now.strftime('%x')}"


# TEST REFRESH STANDARD OUTPUT
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
@mock.patch('src.routes.create_csv_file', return_value=None, autospec=True)
def test_refresh(*args):
    runner = CliRunner()
    result = runner.invoke(refresh, [t.addr_json_file_name])
    output = [item for item in result.output.split(sep='\n') if item]
    now = datetime.datetime.now()

    assert result.exit_code == 0
    assert output[0] == f"File {t.vkhandle}.csv created"
    assert output[1] == f"Address: {t.address}"
    assert output[2] == f"Confirmed Balance(SAT): {t.confirmed_balance} as of {now.strftime('%X')} {now.strftime('%x')}"

# TEST FEE STANDARD OUTPUT
@mock.patch('src.controllers.get_fee_estimate', return_value=t.bitcoinfees_mock_api, autospec=True)
@mock.patch('src.controllers.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
def test_fee(*args):
    runner = CliRunner()
    result = runner.invoke(fee, [t.addr_json_file_name, '-a'])
    output = [item for item in result.output.split(sep='\n') if item]

    assert result.exit_code == 0
    assert output[0] == f'The fee estimates for a transaction for 1DSRQWjbNXLN8ZZZ6gqcGx1WNZeKHEJXDv with {len(t.tx_inputs)} inputs and {1 if t.all else 2} outputs are:'
    i = 0
    for urgency, est in t.bitcoinfees_mock_api.items():
        i += 1
        assert output[i] == f'{urgency}: {est} sat'


# TEST TX STANDARD OUTPUT
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
@mock.patch('src.routes.create_unsigned_tx_files', return_value=None, autospec=True)
def test_tx(*args):
    runner = CliRunner()
    result = runner.invoke(tx, [t.addr_json_file_name,  '-a', '-f', t.fee, '-r', t.recipient])
    output = [item for item in result.output.split(sep='\n') if item]

    assert result.exit_code == 0
    i = 0
    while i < len(t.tx_inputs):
        assert output[i] == f'File unsignedTx{t.vkhandle}_{i+1}.bin created'
        i += 1
    assert output[i] == f'File tx{t.vkhandle}.json created'
    i += 1
    assert output[i] == 'AWS cloudHsm instructions:'
    i += 1
    assert output[i] == '1. Log into your cloudHSM'
    i += 1
    assert output[i] == '2. Run the following to sign your unsigned raw transaction(s):'
    i += 1
    n = 0
    while n < len(t.tx_inputs):
        assert output[i] == f'sign -f unsignedTx7340043_{n+1}.bin -k 7340044 -m 17 -out signedTx7340043_{n+1}.der'
        n += 1
        i += 1
    assert output[i] == '3. Run the following to verify your signature(s):'
    i += 1
    n = 0
    while n < len(t.tx_inputs):
        assert output[i] == f'verify -f unsignedTx7340043_{n+1}.bin -s signedTx7340043_{n+1}.der -k 7340043 -m 17'
        n += 1
        i += 1


# TEST TX SIGNED STANDARD OUTPUT
