
import time
import random
from web3 import Web3
from eth_account import Account
from termcolor import colored
from colorama import init

init()

def read_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file.readlines()]
    return private_keys

YOUR_PRIVATE_KEYS = read_private_keys('private_key.txt')

NFT_CONTRACT_ADDRESS = '0xd2ccc9ee7ea2ccd154c727a46d475dda49e99852'
BRIDGE_CONTRACT_ADDRESS = '0xE09828f0DA805523878Be66EA2a70240d312001e'

# Вставьте ваш ABI контракта здесь
NFT_CONTRACT_ABI = '[{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"},{"internalType":"uint256","name":"_mintLimit","type":"uint256"},{"internalType":"string","name":"_metadataUri","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"InvalidQueryRange","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"explicitOwnershipOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"explicitOwnershipsOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"getMintSurplus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintEndTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintStartTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_newMetadataUri","type":"string"}],"name":"setMetadataUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"}],"name":"setMintTimes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"start","type":"uint256"},{"internalType":"uint256","name":"stop","type":"uint256"}],"name":"tokensOfOwnerIn","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/bsc'))
assert w3.isConnected(), 'Подключение к BSC не удалось'

NFT_CONTRACT_ADDRESS = w3.toChecksumAddress(NFT_CONTRACT_ADDRESS)
BRIDGE_CONTRACT_ADDRESS = w3.toChecksumAddress(BRIDGE_CONTRACT_ADDRESS)

nft_contract = w3.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=NFT_CONTRACT_ABI)

BRIDGE_CONTRACT_ABI = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldContract","type":"address"},{"indexed":true,"internalType":"address","name":"newContract","type":"address"}],"name":"ContractUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingImplementation","type":"address"},{"indexed":true,"internalType":"address","name":"newImplementation","type":"address"}],"name":"NewPendingImplementation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"sourceToken","type":"address"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenID","type":"uint256"},{"indexed":false,"internalType":"uint16","name":"sourceChain","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"sendChain","type":"uint16"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"ReceiveNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"address","name":"nftBridge","type":"address"}],"name":"RegisterChain","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenID","type":"uint256"},{"indexed":false,"internalType":"uint16","name":"recipientChain","type":"uint16"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"TransferNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"MIN_LOCK_TIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId_","type":"uint16"}],"name":"bridgeContracts","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"confirmContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"destChainId","type":"uint16"}],"name":"fee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"impl","type":"address"}],"name":"isInitialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"isWrappedAsset","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"contractAddress","type":"address"}],"name":"registerChain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"destChainId","type":"uint16"},{"internalType":"uint256","name":"fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"lockTime","type":"uint256"}],"name":"setLockTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"zkBridge","type":"address"}],"name":"setZkBridge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"submitContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"toUpdateTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenID","type":"uint256"},{"internalType":"uint16","name":"recipientChain","type":"uint16"},{"internalType":"bytes32","name":"recipient","type":"bytes32"}],"name":"transferNFT","outputs":[{"internalType":"uint64","name":"sequence","type":"uint64"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"tokenChainId","type":"uint16"},{"internalType":"bytes32","name":"tokenAddress","type":"bytes32"}],"name":"wrappedAsset","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"zkBridge","outputs":[{"internalType":"contract IZKBridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"address","name":"srcAddress","type":"address"},{"internalType":"uint64","name":"sequence","type":"uint64"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"zkReceive","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

bridge_contract = w3.eth.contract(address=BRIDGE_CONTRACT_ADDRESS, abi=BRIDGE_CONTRACT_ABI)

def mint_and_approve(YOUR_PRIVATE_KEY):
    account = Account.from_key(YOUR_PRIVATE_KEY)
    YOUR_ADDRESS = account.address
    nonce = w3.eth.getTransactionCount(YOUR_ADDRESS)
    gas_price = w3.eth.gasPrice
    gas_estimate = nft_contract.functions.mint().estimateGas({
        'from': YOUR_ADDRESS,
        'gasPrice': gas_price,
    })

    mint_tx = nft_contract.functions.mint().buildTransaction({
        'from': YOUR_ADDRESS,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_tx = Account.sign_transaction(mint_tx, YOUR_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f'Транзакция mint отправлена: {w3.toHex(tx_hash)}')

    # Ждем от 15 до 25 секунд можешь изменить таймаут
    time.sleep(random.randint(15, 25))

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    minted_token_id = nft_contract.events.Transfer().processReceipt(tx_receipt)[0]['args']['tokenId']
    SPENDER_ADDRESS = '0xE09828f0DA805523878Be66EA2a70240d312001e'

    nonce = w3.eth.getTransactionCount(YOUR_ADDRESS)
    gas_estimate = nft_contract.functions.approve(SPENDER_ADDRESS, minted_token_id).estimateGas({
        'from': YOUR_ADDRESS,
        'gasPrice': gas_price,
    })

    approve_tx = nft_contract.functions.approve(SPENDER_ADDRESS, minted_token_id).buildTransaction({
                'from': YOUR_ADDRESS,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_tx = Account.sign_transaction(approve_tx, YOUR_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f'Транзакция approve отправлена: {w3.toHex(tx_hash)}')

    # Ждем от 20 до 30 секунд можешь изменить таймаут
    time.sleep(random.randint(20, 30))

    address, tx_hash = transferNFT(YOUR_PRIVATE_KEY, minted_token_id)

    return address, tx_hash
    
def transferNFT(YOUR_PRIVATE_KEY, token_id):
    account = Account.from_key(YOUR_PRIVATE_KEY)
    YOUR_ADDRESS = account.address

    transfer_nft_amount = w3.toWei(0.001, 'ether')
    token_address = NFT_CONTRACT_ADDRESS
    recipient_chain = 5
    recipient = YOUR_ADDRESS
    recipient_bytes32 = '0x' + '0' * 24 + recipient[2:]

    nonce = w3.eth.getTransactionCount(YOUR_ADDRESS)
    gas_price = w3.eth.gasPrice
    gas_estimate = bridge_contract.functions.transferNFT(token_address, token_id, recipient_chain, recipient_bytes32).estimateGas({
        'from': YOUR_ADDRESS,
        'gasPrice': gas_price,
        'value': transfer_nft_amount
    })

    transfer_tx = bridge_contract.functions.transferNFT(token_address, token_id, recipient_chain, recipient_bytes32).buildTransaction({
        'from': YOUR_ADDRESS,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce,
        'value': transfer_nft_amount
    })

    signed_tx = Account.sign_transaction(transfer_tx, YOUR_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f'Транзакция transferNFT отправлена: {w3.toHex(tx_hash)}')

    return YOUR_ADDRESS, w3.toHex(tx_hash)

if __name__ == '__main__':
    text = "СИБИЛ АТАКА ОТ GRANTA DAO ЗАПУЩЕНА"
    colored_text = colored(text, 'red', attrs=['bold'])

    print(colored_text)
    results = []

    for private_key in YOUR_PRIVATE_KEYS:
        address, tx_hash = mint_and_approve(private_key)
        results.append((address, tx_hash))

    with open('result.txt', 'w') as file:
        for address, tx_hash in results:
            file.write(f'{address}:{tx_hash}\n')
            
    text = "СИБИЛ АТАКА ЗАВЕРШЕНА"
    colored_text = colored(text, 'green', attrs=['bold'])
    print(colored_text)
