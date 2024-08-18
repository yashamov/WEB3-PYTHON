
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

NFT_CONTRACT_ADDRESS = '0x61d7e121185b1d7902a3da7f3c8ac9faaee8863b'
NFT_BRIDGE_CONTRACT_ADDRESS = '0xcbbe443e580cb01b67114a53fe90df0d51c26581'

NFT_CONTRACT_ABI = '[{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"},{"internalType":"uint256","name":"_mintLimit","type":"uint256"},{"internalType":"string","name":"_metadataUri","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"InvalidQueryRange","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_size","type":"uint256"}],"name":"batchMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"explicitOwnershipOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"explicitOwnershipsOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"getMintSurplus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintEndTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintStartTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_newMetadataUri","type":"string"}],"name":"setMetadataUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintLimit","type":"uint256"}],"name":"setMintLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"}],"name":"setMintTimes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"start","type":"uint256"},{"internalType":"uint256","name":"stop","type":"uint256"}],"name":"tokensOfOwnerIn","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
NFT_BRIDGE_CONTRACT_ABI = '[{"inputs": [{"internalType": "address","name": "_token","type": "address"},{"internalType": "uint256","name": "_tokenId","type": "uint256"},{"internalType": "uint16","name": "_recipientChain","type": "uint16"},{"internalType": "address","name": "_recipient","type": "address"},{"internalType": "bytes","name": "_adapterParams","type": "bytes"}],"name": "transferNFT","outputs": [],"stateMutability": "nonpayable","type": "function"}]'

opBNB_RPC = Web3(Web3.HTTPProvider('https://opbnb-mainnet-rpc.bnbchain.org'))
assert opBNB_RPC.is_connected(), 'Подключение к opBNB RPC не удалось'


NFT_CONTRACT_ADDRESS = opBNB_RPC.to_checksum_address(NFT_CONTRACT_ADDRESS)
nft_contract = opBNB_RPC.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=NFT_CONTRACT_ABI)


NFT_BRIDGE_CONTRACT_ADDRESS = opBNB_RPC.to_checksum_address(NFT_BRIDGE_CONTRACT_ADDRESS)
nft_bridge_contract = opBNB_RPC.eth.contract(address=NFT_BRIDGE_CONTRACT_ADDRESS, abi=NFT_BRIDGE_CONTRACT_ABI)



def transferNFT(YOUR_PRIVATE_KEY, token_id):
    account = Account.from_key(YOUR_PRIVATE_KEY)
    YOUR_ADDRESS = account.address
    transfer_nft_amount = opBNB_RPC.to_wei(0.0005, 'ether')
    token_address = NFT_CONTRACT_ADDRESS
    recipient_chain = 27
    recipient = YOUR_ADDRESS
    recipient_bytes32 = '0x' + '0' * 24 + recipient[2:]
    nonce = opBNB_RPC.eth.get_transaction_count(YOUR_ADDRESS)

    estimate_fee = nft_bridge_contract.functions.estimateFee(poolId, dstChainId, amount).call()
    print(f'Estimated Fee: {estimate_fee}')

    gas_price = opBNB_RPC.eth.gas_price
    gas_estimate = nft_bridge_contract.functions.transferNFT(token_address, token_id, recipient_chain, recipient, bytes.fromhex('00')).estimate_gas({
        'from': YOUR_ADDRESS,
        'gasPrice': gas_price,
    })

    transfer_tx = nft_bridge_contract.functions.transferNFT(token_address, token_id, recipient_chain, recipient, bytes.fromhex('00')).build_transaction({
        'from': YOUR_ADDRESS,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce,
        'value': transfer_nft_amount
    })


    signed_transaction = opBNB_RPC.eth.account.sign_transaction(transfer_tx, YOUR_PRIVATE_KEY)
    tx_hash = opBNB_RPC.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f'Транзакция transferNFT отправлена: {opBNB_RPC.to_hex(tx_hash)}')

    return YOUR_ADDRESS, opBNB_RPC.to_hex(tx_hash)




if __name__ == '__main__':
    text = "СИБИЛ АТАКА на полихедру запущена"
    colored_text = colored(text, 'red', attrs=['bold'])
    print(colored_text)

results = []
errors = []


for private_key in YOUR_PRIVATE_KEYS:
    try:
        transaction_hash = '0x2c1d674d39569864905ed24c4755d640701c8e3c1bc8b47a999a1be3f885e464'
        #transaction_hash = opBNB_RPC.to_checksum_address(transaction_hash)
        tx_receipt = opBNB_RPC.eth.wait_for_transaction_receipt(transaction_hash)
        minted_token_id = nft_contract.events.Transfer().process_receipt(tx_receipt)[0]['args']['tokenId']

        address, tx_hash = transferNFT(private_key, minted_token_id)
        results.append((address, tx_hash))
    except ContractLogicError as e:
        print("Ошибка выполнения контракта:", e)


with open('result.txt', 'w') as file:
    for address, transaction_hash in results:
        file.write(f'{address}:{transaction_hash}\n')

#with open('errors.txt', 'w') as file:
    #for private_key in errors:
        #file.write(f'{private_key}\n')

text = "СИБИЛ АТАКА ЗАВЕРШЕНА"
colored_text = colored(text, 'green', attrs=['bold'])
print(colored_text)
