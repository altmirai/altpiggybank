class MockFeeEstOne():
    @property
    def status_code(self):
        return 200

    def json(self):
        return {"fastestFee": 200, "halfHourFee": 200, "hourFee": 100}


class TestDataOne():
    @property
    def path(self):
        return 'tests/test_files'

    @property
    def pub_key_file_name(self):
        return f"{self.path}/pubKey{self.vkhandle}.pem"

    @property
    def vkhandle(self):
        return '7340043'

    @property
    def skhandle(self):
        return '7340044'

    @property
    def address(self):
        return '1DSRQWjbNXLN8ZZZ6gqcGx1WNZeKHEJXDv'

    @property
    def confirmed_balance(self):
        return 5763656

    @property
    def all(self):
        return True

    @property
    def fee(self):
        return 104600

    @property
    def recipient(self):
        return '1BHznNt5x9rqMQ1dpWy4fw5y5PSJV3ZR3L'

    @property
    def value(self):
        return None

    @property
    def change_address(self):
        return None

    @property
    def tx_inputs(self):
        return [
            {
                'output_no': 0,
                'outpoint_index': b'\x00\x00\x00\x00',
                'outpoint_hash': bytearray(
                    b"Y:N~v%0\xbc\xcf\xbc\xd9@\xc2K\xc3\x92\xc6\xfb\xe7#\xcf\x8e\xf4\xe8\xa9t\xf5m\x1fE\'\x9d"
                )
            },
            {
                'output_no': 0,
                'outpoint_index': b'\x00\x00\x00\x00',
                'outpoint_hash': bytearray(
                    b'qg/\xe5\x86\xbcvS\xc7t\\D\r\xc4\x1dG8\xe9\xab3\xa4|N.x(\xa7v\xaf\x8d\xcfx'
                )
            },
            {
                'output_no': 0,
                'outpoint_index': b'\x00\x00\x00\x00',
                'outpoint_hash': bytearray(
                    b'"\x9a\xd5\x904\\^\xac^\xc1\xe6c>\x93mU\xfc\xf8\xab\x17\xf4G[\xae\xd9\x13\xb9\xc6\xe7\x05\x7f_'
                )
            }
        ]

    @property
    def mock_fees(self):
        return {
            'estimates': {
                'Fastest': 97600,
                'Half hour': 97600,
                'One hour': 48800
            },
            'n_inputs': 3,
            'n_outputs': 1
        }

    @property
    def tosign_tx_hex(self):
        return [
            '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf780000000000ffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f0000000000ffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000',
            '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d0000000000ffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf78000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f0000000000ffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000',
            '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d0000000000ffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf780000000000ffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000'
        ]

    @property
    def tosign_tx_hashed_hex(self):
        return [
            'af69b4567cbcd15f2c719a62311ef8fe47711e21c038dad27f3fc631baf21f3c', '600da7c38b14b9bfc44a6deba21621555b1aadba9066a1e76fe4a7e48082748f', 'f5aa21d884e6e5b4eac08803640b6546145b2f2bf34a04945ea7685615454f27'
            ]

    @property
    def tx_hex(self):
        return '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d000000008a473044022038096755f89ba2cb28f4b4a7db056bbbe77972560d65da3a55e2ef702fd837f90220196ed119a36cb134000f90ff6048a7b1a838ee65c2369207145305155c3953fa0141046e9cd8479193a02d025d236545e72edf10237e54a64a887df866f8d5b86a0fd55449ad821df8e2568116e52cdee3a6b11d7ae7d5e1920244e2426704c5f58005ffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf78000000008a473044022022bc4f1e0075c943af3065072ee45231846fc3a7e2c9192766ded3a963e207880220415b88dcae7cf63eeb504c6c96ebb3b8049f00cc41dee7ed0309d29c06549e4b0141046e9cd8479193a02d025d236545e72edf10237e54a64a887df866f8d5b86a0fd55449ad821df8e2568116e52cdee3a6b11d7ae7d5e1920244e2426704c5f58005ffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f000000008b483045022100f659e8a85019ae4562665a2377caae4535b7674a2478567adcc44133c96cd4bc022045e7076b0e212159323b68cc4a29805e0d12f349d23e8ca8f6fac79a1d9afcc60141046e9cd8479193a02d025d236545e72edf10237e54a64a887df866f8d5b86a0fd55449ad821df8e2568116e52cdee3a6b11d7ae7d5e1920244e2426704c5f58005ffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac00000000'

    @property
    def signature_files(self):
        signature_file_names = ['signedTx7340043_1.der',
                                'signedTx7340043_2.der', 'signedTx7340043_3.der']
        signature_files = []
        for signature_file_name in signature_file_names:
            file = open(f'{self.path}/{signature_file_name}', 'rb')
            signature_files.append(file)

        return signature_files

    @property
    def aws(self):
        return True

    @property
    def output_path(self):
        return 'test_output'

    @property
    def pem(self):
        return '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEbpzYR5GToC0CXSNlRecu3xAjflSmSoh9\n+Gb41bhqD9VUSa2CHfjiVoEW5Sze46axHXrn1eGSAkTiQmcExfWABQ==\n-----END PUBLIC KEY-----\n'

    @property
    def addr_json_file(self):
        return {
            'file_name': f'addr{self.vkhandle}',
            'vkhandle': self.vkhandle,
            'skhandle': self.skhandle,
            'pem': self.pem
            }

    @property
    def addr_csv_file(self):
        return [self.vkhandle, self.skhandle, self.address, str(self.confirmed_balance)]

    @property
    def addr_json_file_name(self):
        return f"{self.path}/addr{self.vkhandle}.json"

    @property
    def bitcoinfees_mock_api(self):
        n_inputs = len(self.tx_inputs)
        n_outputs = 1 if self.all else 2
        bytes = 10 + (n_inputs * 148) + (n_outputs * 34)
        resp = {"fastestFee": 100, "halfHourFee": 75, "hourFee": 50}
        estimate = {'Fastest': resp['fastestFee'] * bytes,
                    'Half hour': resp['halfHourFee'] * bytes,
                    'One hour': resp['hourFee'] * bytes}
        return estimate

    @property
    def signature_file_names(self):
        i = 0
        sig_file_names = []
        while i < len(self.tx_inputs):
            sig_file_names.append(f'{self.path}/signedTx{self.vkhandle}_{i+1}.der')
            i += 1   
        return sig_file_names

    @property
    def tx_json_file_name(self):
        return f'{self.path}/tx{self.vkhandle}.json'

    @property
    def tx_json_file(self):
        return {
            'file_name': f'tx{self.vkhandle}',
            'all': self.all,
            'fee': self.fee,
            'recipient': self.recipient,
            'partial': False if self.all else True,
            'vkhandle': self.vkhandle,
            'skhandle': self.skhandle,
            'pem': self.pem,
            'address': self.address,
            'confrimed_balance': self.confirmed_balance,
            'n_tx_inputs': len(self.tx_inputs)
        }
