import hashlib
from src.adapters import get_confirmed_sat_balance, get_tx_inputs
from src.bitcoin_addresses import P2PKH

from src.bitcoin_scripts import PubKeyScript, SigScript, TxOutputScript


class SignedTx:

    def __init__(self, pem, unsigned_tx, signatures):
        self.pem = pem
        self.unsigned_tx = unsigned_tx
        self.signatures = signatures

    @property
    def hex(self):
        tx = bytearray()

        tx += self.unsigned_tx.version
        tx += self.unsigned_tx.tx_in_count
        for tx_in in self.unsigned_tx.tx_inputs:

            sig_script = SigScript(
                self.signatures, self.unsigned_tx, tx_in, self.pem)

            tx += self.unsigned_tx.previous_output(tx_in)
            tx += sig_script.script_bytes
            tx += sig_script.script
            tx += self.unsigned_tx.sequence
        tx += self.unsigned_tx.tx_out_count
        for tx_out in self.unsigned_tx.tx_outs.outputs:
            tx += tx_out
        tx += self.unsigned_tx.lock_time

        return tx.hex()


class UnsignedTx:

    def __init__(self, pem, recipient, fee, value, change_address):
        self.p2pkh = P2PKH(pem)
        self.address = self.p2pkh.address
        self.confirmed_balance = self.p2pkh.confirmed_balance
        self.tx_inputs = get_tx_inputs(self.address)
        self.tx_outs = TxOutputScript(
            self.address, self.confirmed_balance, recipient, fee, value, change_address)
        self.pub_key_script = PubKeyScript(self.address)

    @property
    def messages(self):
        messages = []
        for tx in self.tx_inputs:
            msg = bytearray()
            msg += self.version
            msg += self.tx_in_count
            for tx_in in self.tx_inputs:
                msg += self.previous_output(tx_in)
                if tx == tx_in:
                    msg += self.pub_key_script.bytes
                    msg += self.pub_key_script.script
                else:
                    msg += self.placeholder
                msg += self.sequence
            msg += self.tx_out_count
            for tx_output in self.tx_outs.outputs:
                msg += tx_output
            msg += self.lock_time
            msg += self.hash_code

            messages.append({'message': msg, 'tx_input': tx})

        return messages

    @property
    def to_sign(self):
        to_signs = []
        for msg in self.messages:
            to_signs.append(hashlib.sha256(msg['message']).digest())
        return to_signs

    @property
    def version(self):
        return (1).to_bytes(4, byteorder="little", signed=True)

    @property
    def tx_in_count(self):
        return (len(self.tx_inputs)).to_bytes(1, byteorder="little", signed=False)

    def previous_output(self, tx_in):
        output = bytearray()
        output += tx_in['outpoint_hash']
        output += tx_in['outpoint_index']
        return output

    @property
    def placeholder(self):
        return (0).to_bytes(1, byteorder='little', signed=False)

    @property
    def sequence(self):
        return bytes.fromhex("ffffffff")

    @property
    def tx_out_count(self):
        return (len(self.tx_outs.outputs)).to_bytes(1, byteorder="little", signed=False)

    @property
    def lock_time(self):
        return (0).to_bytes(4, byteorder="little", signed=False)

    @property
    def hash_code(self):
        return (1).to_bytes(4, byteorder='little', signed=False)
