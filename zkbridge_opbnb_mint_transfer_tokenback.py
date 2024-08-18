

import time
import random
from web3 import Web3
from web3.exceptions import ContractLogicError
from eth_account import Account
from termcolor import colored
from colorama import init

init()


def read_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file.readlines()]
    return private_keys


YOUR_PRIVATE_KEYS = read_private_keys('private_keys.txt')

# NFT_CONTRACT_ADDRESS = '0x61DFDbcC65DaF1F60fB1DbE703D84940dA28526c'
TOKEN_BRIDGE_CONTRACT_ADDRESS = '0x51187757342914E7d94FFFD95cCCa4f440FE0E06'

# Вставьте ваш ABI контракта здесь
TOKEN_BRIDGE_CONTRACT_ABI = '[{"inputs":[{"internalType":"contract IZKBridgeEndpoint","name":"zkBridgeEndpoint_","type":"address"},{"internalType":"contract IL1Bridge","name":"l1Bridge_","type":"address"},{"internalType":"uint256","name":"NATIVE_TOKEN_POOL_ID_","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AddLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"BridgeManagerTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"BridgeManagerTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"BridgeReviewerTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"BridgeReviewerTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ClaimedFees","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":true,"internalType":"uint16","name":"dstChainId","type":"uint16"},{"indexed":true,"internalType":"bool","name":"enabled","type":"bool"}],"name":"DstChainStatusChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"address","name":"bridge","type":"address"}],"name":"NewBridge","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":true,"internalType":"uint16","name":"dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"staticFee","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dynamicFeeNum","type":"uint256"}],"name":"NewFee","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"maxLiquidity","type":"uint256"}],"name":"NewMaxLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":true,"internalType":"uint16","name":"dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"maxTransferLimit","type":"uint256"}],"name":"NewMaxTransferLimit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"address","name":"bridge","type":"address"}],"name":"NewPendingBridge","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"PoolManagerTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"PoolManagerTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":true,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ReceiveToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RemoveLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":true,"internalType":"uint16","name":"dstChainId","type":"uint16"},{"indexed":true,"internalType":"uint256","name":"poolId","type":"uint256"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"TransferToken","type":"event"},{"inputs":[],"name":"DYNAMIC_FEE_DEN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NATIVE_TOKEN_POOL_ID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"acceptBridgeManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"acceptBridgeReviewer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"acceptPoolManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"accumulatedFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"addLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"maxLiquidity","type":"uint256"}],"name":"addLiquidityAndSetMaxLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"addLiquidityETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxLiquidity","type":"uint256"}],"name":"addLiquidityETHAndSetMaxLiquidity","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"addLiquidityETHPublic","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"addLiquidityPublic","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"bridge","type":"address"}],"name":"approveSetBridge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"bridgeLookup","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bridgeManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bridgeReviewer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"}],"name":"convertRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint8","name":"convertRateDecimals","type":"uint8"}],"name":"createPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"}],"name":"dstChains","outputs":[{"components":[{"internalType":"bool","name":"enabled","type":"bool"},{"internalType":"uint128","name":"staticFee","type":"uint128"},{"internalType":"uint64","name":"dynamicFeeNum","type":"uint64"},{"internalType":"uint256","name":"maxTransferLimit","type":"uint256"}],"internalType":"struct Pool.DstChainInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"estimateFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"estimateFeeMux","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"l1Bridge","outputs":[{"internalType":"contract IL1Bridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingBridge","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingBridgeAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingBridgeManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingBridgeReviewer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingDstChainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingPoolManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"}],"name":"poolInfo","outputs":[{"components":[{"internalType":"bool","name":"enabled","type":"bool"},{"internalType":"uint8","name":"convertRateDecimals","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"maxLiquidity","type":"uint256"}],"internalType":"struct Pool.PoolInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"removeLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"bridge","type":"address"}],"name":"setBridge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"bool","name":"enabled","type":"bool"}],"name":"setDstChain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"staticFee","type":"uint256"},{"internalType":"uint256","name":"dynamicFeeNum","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"maxLiquidity","type":"uint256"}],"name":"setMaxLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"maxTransferLimit","type":"uint256"}],"name":"setMaxTransferLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user_","type":"address"},{"internalType":"bool","name":"enabled_","type":"bool"}],"name":"setWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferBridgeManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferBridgeReviewer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"transferETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"transferETHMux","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferPoolManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"transferToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"uint256","name":"poolId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"transferTokenMux","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"zkBridgeEndpoint","outputs":[{"internalType":"contract IZKBridgeEndpoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"address","name":"srcAddress","type":"address"},{"internalType":"uint64","name":"sequence","type":"uint64"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"zkReceive","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

bsc_RPC = Web3(Web3.HTTPProvider('https://rpc.ankr.com/bsc'))
assert bsc_RPC.is_connected(), 'Подключение к BSC ANKR не удалось'


# NFT_CONTRACT_ADDRESS = w3.to_checksum_address(NFT_CONTRACT_ADDRESS)
# nft_contract = w3.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=NFT_CONTRACT_ABI)


TOKEN_BRIDGE_CONTRACT_ADDRESS = bsc_RPC.to_checksum_address(TOKEN_BRIDGE_CONTRACT_ADDRESS)
token_bridge_contract = bsc_RPC.eth.contract(address=TOKEN_BRIDGE_CONTRACT_ADDRESS, abi=TOKEN_BRIDGE_CONTRACT_ABI)


def bridge_to_opnb(YOUR_PRIVATE_KEY):
    account = Account.from_key(YOUR_PRIVATE_KEY)
    YOUR_ADDRESS = account.address
    nonce = bsc_RPC.eth.get_transaction_count(YOUR_ADDRESS)
    dstChainId = 23
    poolId = 10
    recipient = YOUR_ADDRESS
    transfer_bnb_amount = bsc_RPC.to_wei(random.uniform(0.009, 0.0105), 'ether')
    amount = transfer_bnb_amount


    estimate_fee = token_bridge_contract.functions.estimateFee(poolId, dstChainId, amount).call()
    print(f'Estimated Fee: {estimate_fee}')

    gas_price = bsc_RPC.eth.gas_price
    gas_estimate = token_bridge_contract.functions.transferETH(dstChainId, amount, recipient).estimate_gas({
        'from': YOUR_ADDRESS,
        'gasPrice': gas_price,
        'value': transfer_bnb_amount + estimate_fee
    })

    # билдим транзу бриджа в опбнб
    bridge_tx = token_bridge_contract.functions.transferETH(dstChainId, amount, recipient).build_transaction({
        'from': YOUR_ADDRESS,
        'gas': gas_estimate,
        'gasPrice': bsc_RPC.to_wei(random.uniform(1.1, 1.25), 'gwei'),
        'nonce': nonce,
        'value': transfer_bnb_amount + estimate_fee
    })


    # Подпись транзакции
    signed_transaction = bsc_RPC.eth.account.sign_transaction(bridge_tx, YOUR_PRIVATE_KEY)

    # Хэш
    transaction_hash = bsc_RPC.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f'Транзакция Bridge в opBNB отправлена: {bsc_RPC.to_hex(transaction_hash)}')


    # Ждем от 15 до 25 секунд можешь изменить таймаут
    time.sleep(random.randint(15, 200))
    tx_receipt = bsc_RPC.eth.wait_for_transaction_receipt(transaction_hash)
    print(f'Транзакция Bridge в opBNB подтверждена в сети BSC')

    return YOUR_ADDRESS, bsc_RPC.to_hex(transaction_hash)


if __name__ == '__main__':
    text = "СИБИЛ АТАКА на полихедру запущена"
    colored_text = colored(text, 'red', attrs=['bold'])
    print(colored_text)


results = []
errors = []


for private_key in YOUR_PRIVATE_KEYS:
    try:
        address, transaction_hash = bridge_to_opnb(private_key)
    except ContractLogicError as e:
        print("Ошибка выполнения контракта:", e)

    with open('result.txt', 'w') as file:
        for address, transaction_hash in results:
            file.write(f'{address}:{transaction_hash}\n')

    with open('errors.txt', 'w') as file:
        for private_key in errors:
            file.write(f'{private_key}\n')

    text = "СИБИЛ АТАКА ОТ GRANTA DAO ЗАВЕРШЕНА"
    colored_text = colored(text, 'green', attrs=['bold'])
    print(colored_text)
