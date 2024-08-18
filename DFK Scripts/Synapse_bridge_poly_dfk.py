from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
from web3.exceptions import ContractLogicError
import json
import time
import random


# Initialize a web3 instance with the Polygon node
web3 = Web3(Web3.HTTPProvider("https://polygon.blockpi.network/v1/rpc/public"))

# USDC contract address
usdc_contract_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# Synapse Bridge contract address
#synapse_bridge_contract_address = "0x1c6ae197ff4bf7ba96c66c5fd64cb22450af9cc8"
synapse_bridge_contract_address = web3.toChecksumAddress('0x1c6ae197ff4bf7ba96c66c5fd64cb22450af9cc8')

# ABI контракта USDC
usdc_contract_abi = '[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

# The ABI for the Synapse Bridge contract
synapse_bridge_abi = '[{"inputs":[{"internalType":"address payable","name":"_wethAddress","type":"address"},{"internalType":"address","name":"_swapOne","type":"address"},{"internalType":"address","name":"tokenOne","type":"address"},{"internalType":"address","name":"_swapTwo","type":"address"},{"internalType":"address","name":"tokenTwo","type":"address"},{"internalType":"contract ISynapseBridge","name":"_synapseBridge","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH_ADDRESS","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"dx","type":"uint256"}],"name":"calculateSwap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"liqTokenIndex","type":"uint8"},{"internalType":"uint256","name":"liqMinAmount","type":"uint256"},{"internalType":"uint256","name":"liqDeadline","type":"uint256"}],"name":"redeemAndRemove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"minDy","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"redeemAndSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"dx","type":"uint256"},{"internalType":"uint256","name":"minDy","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapAndRedeem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"dx","type":"uint256"},{"internalType":"uint256","name":"minDy","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"liqTokenIndex","type":"uint8"},{"internalType":"uint256","name":"liqMinAmount","type":"uint256"},{"internalType":"uint256","name":"liqDeadline","type":"uint256"}],"name":"swapAndRedeemAndRemove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"dx","type":"uint256"},{"internalType":"uint256","name":"minDy","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"swapTokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"swapTokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"swapMinDy","type":"uint256"},{"internalType":"uint256","name":"swapDeadline","type":"uint256"}],"name":"swapAndRedeemAndSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint8","name":"tokenIndexFrom","type":"uint8"},{"internalType":"uint8","name":"tokenIndexTo","type":"uint8"},{"internalType":"uint256","name":"dx","type":"uint256"},{"internalType":"uint256","name":"minDy","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHAndRedeem","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"swapMap","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"swapTokensMap","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'  # Fill this with the Synapse Bridge contract's ABI

# Get the contract instances
contract = web3.eth.contract(address=Web3.toChecksumAddress(usdc_contract_address), abi=usdc_contract_abi)
synapse_bridge_contract = web3.eth.contract(address=synapse_bridge_contract_address, abi=synapse_bridge_abi)

# Replace 'destination_chain_id' with the chain id of the destination network
destination_chain_id = 53935

# Read private keys from file
with open('private_keys.txt', 'r') as f:
    private_keys = [line.strip() for line in f]

print("СИБИЛ АТАКА ЗАПУЩЕНА")

for private_key in private_keys:
    # Get account address from private key
    account_address = web3.eth.account.privateKeyToAccount(private_key).address

    # Get USDC balance
    balance = contract.functions.balanceOf(account_address).call()

    if balance > 0:
        # Build the approve transaction for the USDC contract
        # Выполнение функции approve()

        nonce = web3.eth.getTransactionCount(account_address)
        gas_price = web3.eth.gasPrice + 100
        print("Цена газа:", gas_price)

        try:
            # Ваш код, вызывающий ошибку ContractLogicError
            gas_estimate = contract.functions.approve(synapse_bridge_contract_address, balance).estimateGas({
                'from': account_address,
                'gasPrice': gas_price,
            })
        except ContractLogicError as e:
            print("Ошибка выполнения контракта:", e)
        
        approve_tx = contract.functions.approve(synapse_bridge_contract_address, balance).buildTransaction({
            'from': account_address,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign the transaction
        signed_approve_txn = web3.eth.account.signTransaction(approve_tx, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_approve_txn.rawTransaction)

        print(f'Транзакция approve отправлена: {web3.toHex(tx_hash)}')

        # Ждем от 20 до 30 секунд
        time.sleep(random.randint(15, 25))

        # Wait for the transaction to be mined
        web3.eth.waitForTransactionReceipt(tx_hash)

        gas_price = web3.eth.gasPrice + 100
        print("Цена газа:", gas_price)
        try:
            # Ваш код, вызывающий ошибку ContractLogicError
            gas_estimate = synapse_bridge_contract.functions.swapAndRedeem(account_address, destination_chain_id,
                                                                      '0xB6c473756050dE474286bED418B77Aeac39B02aF', 2, 0,
                                                                      balance, 1467313, int(time.time()) + 600).estimateGas({
                'from': account_address,
                'gasPrice': gas_price,
                'value': 0
            })
        except ContractLogicError as e:
            print("Ошибка выполнения контракта:", e)


        nonce = web3.eth.getTransactionCount(account_address)
        # Build the deposit transaction
        deposit_txn = synapse_bridge_contract.functions.swapAndRedeem(account_address, destination_chain_id,
                                                                      '0xB6c473756050dE474286bED418B77Aeac39B02aF', 2, 0,
                                                                      balance, 1467313, int(time.time()) + 600).buildTransaction({
            'from': account_address,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
            'value': 0
        })

        # Sign the transaction
        signed_deposit_txn = web3.eth.account.signTransaction(deposit_txn, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_deposit_txn.rawTransaction)

        print(f"Succesfully bridged {web3.fromWei(balance, 'ether')} USDC from {account_address}")

    # Random delay between 30 and 60 seconds
    time.sleep(random.randint(20, 40))

print("СИБИЛ АТАКА ЗАВЕРШЕНА")