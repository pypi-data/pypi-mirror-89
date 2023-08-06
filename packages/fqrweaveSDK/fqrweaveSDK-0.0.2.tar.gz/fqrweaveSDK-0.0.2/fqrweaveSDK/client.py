import arweave
import requests
import os, sys
import qrcode
from bs4 import BeautifulSoup as BS


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

    def batch_generator(self, instance, data_list, dir_name):
        self.instance = instance
        self.data_list = data_list

        path = os.path.join(sys.path[0], dir_name)

        _html_1 = '<html>' + '<head></head>' + \
                  '<body> <center><h1>verified fQR</h1> </center>' + \
                  '< br > < br > < center > < div > < table > < tr > < th > Data < / th > < th > info < / th > < / tr >'

        _html_2 = '</table></div></body></html>'


        if self.instance.startswith('https://'):
            url = self.instance
        else:
            url = f"https://arweave.net/{self.instance}"

        re = requests.get(url)
        html = BS(re.text, features="lxml")
        labels = html.find_all('label')

        product_metadata = []  # store all generator instance metadata
        table_data = []
        html_table = []

        for element in labels:
            clean_1 = str(element).replace('<label for="product">', '')
            clean_2 = str(clean_1).replace('</label>', '')
            clean_3 = clean_2.split(':')
            clean_4 = clean_3[0]
            product_metadata.append(clean_4)

        if len(self.data_list) != len(product_metadata):
            return 'unmatched arguments'
        else:
            for entry in range(len(self.data_list)):
                entry_data = [product_metadata[entry - 1], self.data_list[entry - 1]]
                table_data.append(entry_data)


        for tb in table_data:
            table_el = f'<tr><td>{tb[0]}</td><td>{tb[1]}</td></tr>'
            html_table.append(table_el)

        fqr_html = _html_1 + ''.join(html_table) + _html_2
        modified_html = (fqr_html.replace(' ', ''))

        transaction = arweave.Transaction(self.wallet, data=modified_html)
        transaction.add_tag('Content-Type', 'text/html')
        transaction.sign()
        transaction.send()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(transaction.id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'{path}\\{transaction.id}.png')

        return transaction.id







