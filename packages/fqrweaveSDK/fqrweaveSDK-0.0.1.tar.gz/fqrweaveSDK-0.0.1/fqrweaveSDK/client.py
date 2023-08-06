import arweave
import requests


KEYFILE_PATH = '/path/to/keyfile.json'


def connect(jwk):
    wallet = arweave.Wallet(jwk)
    return wallet


class Fqrweave(object):
    def __init__(self, jwk):
        """

        using https://github.com/MikeHibbert/arweave-python-client
        to connect to Arweave blockchain

        :param: jwk
        """
        self.jwk = jwk
        self.wallet = connect(self.jwk)

    def login(self):
        """
        assign jwk path passed to FQR_WEAVE()
        to connect() function for an easier
        connection with Arweave
        :return: jwk.json path
        """
        global KEYFILE_PATH
        KEYFILE_PATH = self.jwk

        return KEYFILE_PATH


class Tools(object):
    def __init__(self):
        self.wallet = connect(KEYFILE_PATH)

    def pub_address(self):
        return self.wallet.address

    def balance(self):
        """
        :return: wallet's balance in AR or winston * 1E18
        """
        return self.wallet.balance

    def get_max_uploads(self):
        """
        use arweave HTTP api to retrieve 1 byte price in winston
        self.wallet.balance * 1e18 : transform wallet's balance back to winston

        :return: max approx uploads size to the blockweave in mb
        """
        re = requests.get('https://arweave.net/price/1')
        b_price = int(re.text)
        return self.wallet.balance * 1e18 / b_price / 1e6

    def get_n_generators(self):
        """
        use arweave HTTP API to get fQR Weave
        wallet's latest tx

        -----------------------------------------
        fqrweave_addr is owned by fQR Weave team
        and used to send data tx in a form of list

        length: 1

        element: string of jwk['n'] of verified generators
        seperated by a whitespace

        nb of verified generators =
        len((str(last_tx.data, 'utf8')).split(' ')) - 1
        -----------------------------------------

        :return: list of jwk['n'] verified addresses
        """
        fqrweave_addr = 'MtgIRVxVRaooHlL3vHE4Bu875vtnDelgJzwrZ7WnDyo'
        url = f'https://arweave.net/wallet/{fqrweave_addr}/last_tx'
        re = requests.get(url)  # Sends HTTP GET Request
        last_tx = arweave.Transaction(self.wallet, id=re.text)
        last_tx.get_transaction()
        last_tx.get_data()

        #decode from bytestr to ascii, then split it
        #into a list
        return len((str(last_tx.data, 'utf8')).split(' '))







