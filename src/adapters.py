import requests


def get_confirmed_sat_balance(address):
    r = requests.get(
        f"https://sochain.com/api/v2/get_address_balance/BTC/{address}", timeout=5)
    assert r.status_code == 200, f'API returned a status_code of {r.status_code}, please try again later'
    resp = r.json()['data']
    btc_bal = resp['confirmed_balance']
    sat_bal = int(float(btc_bal) * 100000000)

    return sat_bal


def get_tx_inputs(address):
    resp = requests.get(
        f"https://sochain.com//api/v2/get_tx_unspent/BTC/{address}", timeout=5)
    assert resp.status_code == 200, f'block explorer return status code {resp.status_code}'
    resp_tx_inputs = resp.json()['data']['txs']
    tx_inputs = []
    for resp_tx in resp_tx_inputs:
        tx = {}
        tx['output_no'] = resp_tx['output_no']
        tx['outpoint_index'] = (resp_tx['output_no']).to_bytes(
            4, byteorder='little', signed=False)
        hash = bytearray.fromhex(resp_tx['txid'])
        hash.reverse()
        tx['outpoint_hash'] = hash
        tx_inputs.append(tx)

    return tx_inputs


def get_fee_estimate(n_inputs, n_outputs):
    bytes = 10 + (n_inputs * 148) + (n_outputs * 34)
    r = requests.get(
        'https://bitcoinfees.earn.com/api/v1/fees/recommended', timeout=60)
    assert r.status_code == 200
    resp = r.json()
    estimate = {'Fastest': resp['fastestFee'] * bytes,
                'Half hour': resp['halfHourFee'] * bytes,
                'One hour': resp['hourFee'] * bytes}

    return estimate
