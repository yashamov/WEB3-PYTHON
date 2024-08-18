import time
import random
from web3 import Web3
from web3.middleware import geth_poa_middleware


class swapExample():
    def __init__(self):

        #Setup Wallet Informations and RPC
        with open("private_keys.txt") as f:
            self.private_keys = [line.strip() for line in f]

        #Use public rpc
        self.rpc = "https://rpc.ankr.com/polygon"
        self.web3 = Web3(Web3.HTTPProvider(self.rpc)) #connect to web3
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #Setup Swap Value / Gas limit / Gwei
        self.gas = 500000 #gas limit

        #Setup MATIC token address (to spend) and USDC token address (to buy)
        self.WETH = self.web3.toChecksumAddress("0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270")
        self.token_to_buy = self.web3.toChecksumAddress("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")

        #Setup router address (Sushiswap Router Address)
        self.router = self.web3.toChecksumAddress("0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506")

        #Setup SwapExactETHforTokens ABI
        self.abi = [{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"}]

        #Creating instance.
        #We can call contract functions with this.
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.abi)

        #Do swap.
        self.swap()

    def get_gas_price(self):
        # Get current gas price from Polygon network
        return self.web3.eth.gas_price

    def swap(self):
        #building transaction with swap parameters
        for pk in self.private_keys:
            self.wallet = self.web3.eth.account.privateKeyToAccount(pk).address
            self.buy_amount = random.uniform(1.2, 1.5) # random USDC amount to buy
            txn = {
                'chainId': 137,  # Polygon Network
                'gas': self.gas,  # Gas limit
                'gasPrice': self.get_gas_price(),  # Use current gas price
                'nonce': self.web3.eth.getTransactionCount(self.wallet),
                'from': self.wallet,
                'value': self.web3.toWei(self.buy_amount, 'ether'),
                'to': self.router,
                'data': self.router_contract.encodeABI(fn_name='swapExactETHForTokens',
                                                       args=[0, [self.WETH, self.token_to_buy], self.wallet,
                                                             int(time.time()) + 1000])
            }

            # sign the transaction
            signed_txn = self.web3.eth.account.signTransaction(txn, private_key=pk)

            # send transaction
            try:
                txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                print(f"Transaction {txn_hash.hex()} sent!")
            except ValueError as e:
                print(f"Error: {e}")

            # introduce a delay between transactions
            delay = random.uniform(10, 20)
            print(f"Waiting for {delay} seconds before sending the next transaction...")
            time.sleep(delay)

print('Сибил атака на Сушисвап начинается!')
if __name__ == "__main__":
    example = swapExample()