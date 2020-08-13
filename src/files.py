import datetime
import json
from ecdsa import der
from src.bitcoin_addresses import P2PKH


def create_json_file(**data):
    file_name = data.get('file_name')
    file_data = {}
    for key in data:
        if isinstance(data[key], (str, int)):
            file_data[key] = data[key]
        elif isinstance(data[key], bytes):
            file_data[key] = data[key].decode('utf-8')
        else:
            pass
    file = open(f'{file_name}.json', 'w')
    file.write(json.dumps(file_data))
    file.close


def create_csv_file(**kwargs):
    vkhandle = kwargs.get('vkhandle')
    skhandle = kwargs.get('skhandle')
    address = kwargs.get('address')
    confirmed_balance = kwargs.get('confirmed_balance')
    now = datetime.datetime.now()
    csv_file = open(f'{vkhandle}.csv', 'wt')
    csv_file.write(
        f"{vkhandle}, {skhandle}, {address}, {confirmed_balance}, {excel_date(now)}")
    csv_file.close


def create_unsigned_tx_files(messages, vkhandle):
    n = 1
    for msg in messages:
        file = open(f'unsignedTx{vkhandle}_{n}.bin', 'wb')
        file.write(msg)
        file.close
        n += 1


def read_signature_files(signature_files, aws):
    signatures = []
    for file in signature_files:
        signature = file.read()
        file.close()
        if aws:
            signatures.append(aws_der_signature_bug_fix(signature))
        else:
            signatures.append(signatures)
    return signatures


def excel_date(now):
    excel_start_date = datetime.datetime(1899, 12, 30)
    delta = now - excel_start_date
    return float(delta.days) + (float(delta.seconds) / 86400)


def aws_der_signature_bug_fix(signature=None):
    empty = der.remove_sequence(signature)[1]
    if len(empty) != 0:
        signature = signature[:-len(empty)]
    return signature


def read_json_file(file):
    if isinstance(file, str):
        file = open(file, 'r')
    data_json = file.read()
    file.close()
    data = json.loads(data_json)
    # if data.get('pem') is None:
    #     pass
    # else:
    #     data['pem'] = data['pem'].encode('utf-8')
    #     p2pkh = P2PKH(data['pem'])
    #     data['address'] = p2pkh.address
    #     data['confirmed_balance'] = p2pkh.confirmed_balance
    return data
