from unittest import mock
from click.testing import CliRunner
from tests.test_data import TestDataOne, MockFeeEstOne
from src.routes import addr, main
from src.files import excel_date
import datetime
import json

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

    if os.path.exists(t.output_path):
        os.rmdir(t.output_path)


# TEST CREATE ADDR CSV FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_json_file', return_value=None, autospec=True)
def test_addr_csv_file(*args):
    set_up_files()
    runner = CliRunner()
    runner.invoke(main, ['-out', f'{t.output_path}', 'addr',
                         t.pub_key_file_name, '-v', f'{t.vkhandle}', '-s', f'{t.skhandle}'])
    control_date = str(excel_date(datetime.datetime.now()))

    file = open(f"{t.output_path}/{t.vkhandle}.csv", 'r')
    test_csv = file.read().split(sep=', ')
    file.close()
    test_date = test_csv.pop()

    if test_date != control_date:
        tear_down_files()
        assert test_date == control_date

    if test_csv != t.addr_csv_file:
        tear_down_files()
        assert test_csv[0] == t.vkhandle
        assert test_csv[1] == t.skhandle
        assert test_csv[2] == t.address
        assert int(test_csv[3]) == t.confirmed_balance

    tear_down_files()


# TEST CREATE ADDR JSON FILE
@mock.patch('src.bitcoin_addresses.get_confirmed_sat_balance', return_value=t.confirmed_balance, autospec=True)
@mock.patch('src.models.get_tx_inputs', return_value=t.tx_inputs, autospec=True)
@mock.patch('src.routes.create_csv_file', return_value=None, autospec=True)
def test_addr_json_file(*args):
    set_up_files()
    runner = CliRunner()
    runner.invoke(main, ['-out', f'{t.output_path}', 'addr',
                         t.pub_key_file_name, '-v', f'{t.vkhandle}', '-s', f'{t.skhandle}'])

    file = open(f"{t.output_path}/addr{t.vkhandle}.json", 'r')
    test_json = file.read()
    file.close()

    test_addr_file = json.loads(test_json)

    if test_addr_file != t.addr_json_file:
        tear_down_files()
        assert test_addr_file['file_name'] == t.addr_json_file['file_name']
        assert test_addr_file['vkhandle'] == t.addr_json_file['vkhandle']
        assert test_addr_file['skhandle'] == t.addr_json_file['skhandle']
        assert test_addr_file['pem'] == t.addr_json_file['pem']
        assert test_addr_file['output_path'] == t.addr_json_file['output_path']

    tear_down_files()


# TEST CREATE UNSIGNED TX BIN FILES

# TEST CREATE TX JSON FILES
