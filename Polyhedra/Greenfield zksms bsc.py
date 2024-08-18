import time
import random
from web3 import Web3
from eth_account import Account
from web3.exceptions import ValidationError
import requests

# Create a Web3 object
w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/bsc'))
assert w3.isConnected(), 'Подключение к BSC не удалось'

# Contract information and functions
contract_address = '0x044332f4b34fd5639482de41cd1d767f7304fa00'
contract_abi = '[{"inputs":[{"internalType":"address","name":"_zkBridgeEntrypoint","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":true,"internalType":"uint32","name":"dstChainId","type":"uint32"},{"indexed":true,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"string","name":"message","type":"string"}],"name":"MessageSend","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"fee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"dstAddress","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"string","name":"message","type":"string"}],"name":"sendMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxLength","type":"uint256"}],"name":"setMsgLength","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"zkBridgeEntrypoint","outputs":[{"internalType":"contract IZKBridgeEntrypoint","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'  # Specify the ABI of the contract here

# Function parameters
send_message_amount = Web3.toWei('0.0005', 'ether')

# Load private keys from file
with open('private_keys.txt', 'r') as file:
    private_keys = file.read().splitlines()

failed_addresses = []

# Send messages for each private key
for i, private_key in enumerate(private_keys, start=1):
    # Create an account object
    account = Account.from_key(private_key)
    recipient = account.address

    # Randomly determine dst_chain_id
    dst_chain_id = random.choice([14, 4, 6, 12])
    if dst_chain_id == 14:
        dst_address = '0xa4c813cff67DC99145ba4848536489CCA486593d'
        dst_network = 'Arbitrum Nova'
    elif dst_chain_id == 4:
        dst_address = '0x6f66d0E8c60670c0Ff3E129D7b990683d113FcE0'
        dst_network = 'Polygon'
    elif dst_chain_id == 6:
        dst_address = '0x05D0C7DEB769eeDA7675C2fBbf9A79140196FF87'
        dst_network = 'Fantom'
    elif dst_chain_id == 12:
        dst_address = '0x200743C9179D88B2D038223268D97Dcd7dc017Ec'
        dst_network = 'Gnosis'

    # Send POST request to obtain message URI
    post_data = {
        "text": "<div style=\"text-align:center\"><strong>Releasing Greenfield zkMessenger 📧</strong></div><br/><u>Polyhedra Network </u>is delighted to release Greenfield zkMessenger 📧, the first cross-chain data availability protocol powered by <u>BNB Greenfield</u> and <u>zkBridge.</u>🌈<br/><br/>With Greenfield zkMessenger, you can send Web3 emails across multiple blockchain networks, just as convenient as Internet emails. Your data is protected by <u>BNB Greenfield</u> and <u>zkBridge.</u><br/><br/>We would like to express our gratitude for the community's support.<u> Polyhedra Network </u>remains committed to launching innovative products and enhancing user experience.🎉"
    }

    response = requests.post('https://gfapi.zkbridge.com/v1/saveMessage', json=post_data)
    response_json = response.json()
    message_uri = response_json['data']['uri']

    # Create a contract object
    contract = w3.eth.contract(address=w3.toChecksumAddress(contract_address), abi=contract_abi)

    # Determine the nonce for the current account
    nonce = w3.eth.getTransactionCount(account.address)

    try:
        # Estimate gas and get the current gas price
        gas_estimate = contract.functions.sendMessage(dst_chain_id, dst_address, recipient, message_uri).estimateGas({'value': send_message_amount})
        gas_price = w3.eth.gasPrice

        # Prepare the transaction
        transaction = {
            'to': contract.address,
            'value': send_message_amount,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': contract.functions.sendMessage(dst_chain_id, dst_address, recipient, message_uri).buildTransaction({'gas': gas_estimate, 'gasPrice': gas_price, 'nonce': nonce, 'value': send_message_amount})['data'],
            'chainId': 56,  # ChainId for Binance Smart Chain
        }

        # Sign the transaction
        signed_txn = account.sign_transaction(transaction)

        # Send the transaction
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print(f'{i}/{len(private_keys)} | BSC to {dst_network}: {txn_hash.hex()}')

    except ValidationError as e:
        if e.args[0]['code'] == -32000 and "insufficient funds for gas" in e.args[0]['message']:
            failed_addresses.append(recipient)
            print(f'Error: Insufficient funds on the account {recipient}')
        else:
            raise

    # Delay between accounts
    time.sleep(random.randint(60, 80))