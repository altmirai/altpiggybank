from unittest import mock
from click.testing import CliRunner
from tests.test_data import TestDataOne, MockFeeEstOne
from src.routes import main
from src.files import excel_date
import datetime
import json
from hashlib import sha256

import os

t = TestDataOne()


def set_up_files():
    tear_down_files()
    os.mkdir(t.output_path)


def tear_down_files():
    if os.path.exists(f"{t.output_path}/{t.vkhandle}.csv"):
        os.remove(f"{t.output_path}/{t.vkhandle}.csv")

    if os.path.exists(f"{t.output_path}/addr{t.vkhandle}.json"):
        os.remove(f"{t.output_path}/addr{t.vkhandle}.json")

    if os.path.exists(f"{t.output_path}/tx{t.vkhandle}.json"):
        os.remove(f"{t.output_path}/tx{t.vkhandle}.json")

    i = 1
    while i < len(t.tx_inputs) + 1:
        if os.path.exists(f"{t.output_path}/unsignedTx{t.vkhandle}_{i}.bin"):
            os.remove(f"{t.output_path}/unsignedTx{t.vkhandle}_{i}.bin")
        i += 1

    if os.path.exists(t.output_path):
        os.rmdir(t.output_path)


# TEST ADDR CSV FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
def test_addr_csv_file(*args):
    set_up_files()
    runner = CliRunner()
    result = runner.invoke(main, ['-out', t.output_path, 'addr',
                         t.pub_key_file_name, '-v', t.vkhandle, '-s', t.skhandle])
    control_date = str(excel_date(datetime.datetime.now()))

    file = open(f"{t.output_path}/{t.vkhandle}.csv", 'r')
    test_csv = file.read().split(sep=', ')
    file.close()
    test_date = test_csv.pop()

    tear_down_files()

    assert result.exit_code == 0
    assert test_date == control_date
    assert test_csv[0] == t.vkhandle
    assert test_csv[1] == t.skhandle
    assert test_csv[2] == t.address
    assert int(test_csv[3]) == t.confirmed_balance



# TEST ADDR JSON FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_csv_file', return_value=None, autospec=True)
def test_addr_json_file(*args):
    set_up_files()
    runner = CliRunner()
    result = runner.invoke(main, ['-out', t.output_path, 'addr',
                         t.pub_key_file_name, '-v', t.vkhandle, '-s', t.skhandle])

    file = open(f"{t.output_path}/addr{t.vkhandle}.json", 'r')
    json_data = file.read()
    file.close()
    tear_down_files()

    data = json.loads(json_data)

    assert result.exit_code == 0
    for key in data.keys():
        assert data[key] == t.addr_json_file[key]

    for key in t.addr_json_file.keys():
        assert data[key] == t.addr_json_file[key]




# TEST REFRESH CSV FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
def test_refresh_csv_file(*args):
    set_up_files()
    runner = CliRunner()
    result = runner.invoke(main, ['-out', t.output_path, 'refresh', t.addr_json_file_name])
    control_date = str(excel_date(datetime.datetime.now()))

    file = open(f"{t.output_path}/{t.vkhandle}.csv", 'r')
    test_csv = file.read().split(sep=', ')
    file.close()
    test_date = test_csv.pop()

    tear_down_files()

    assert result.exit_code == 0
    assert test_date == control_date
    assert test_csv[0] == t.vkhandle
    assert test_csv[1] == t.skhandle
    assert test_csv[2] == t.address
    assert int(test_csv[3]) == t.confirmed_balance



# TEST TX JSON FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_unsigned_tx_files', return_value=None, autospec=True)
def test_tx_json_file(*args):
    set_up_files()
    runner = CliRunner()
    result = runner.invoke(main, ['-out', t.output_path, 'tx', t.tx_json_file_name, '-a', '-f', t.fee, '-r', t.recipient])

    file = open(f"{t.output_path}/tx{t.vkhandle}.json", 'r')
    json_data = file.read()
    file.close()
    tear_down_files()

    data = json.loads(json_data)

    assert result.exit_code == 0
    for key in data.keys():
        assert data[key] == t.tx_json_file[key]
    for key in t.tx_json_file.keys():
        assert data[key] == t.tx_json_file[key]


# TEST TX BIN FILES
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
def test_tx_bin_files(*args):
    set_up_files()
    runner = CliRunner()
    result = runner.invoke(main, ['-out', t.output_path, 'tx', t.tx_json_file_name, '-a', '-f', t.fee, '-r', t.recipient])

    if result.exit_code != 0:
        tear_down_files()
    assert result.exit_code == 0


    i = 1
    tx_bin_files = []
    while i < len(t.tx_inputs) + 1:
        file = open(f"{t.output_path}/unsignedTx{t.vkhandle}_{i}.bin", 'rb')
        tx_bin_files.append(file.read().hex())
        file.close()
        i += 1
    tear_down_files()

    assert tx_bin_files == t.tosign_tx_hashed_hex

