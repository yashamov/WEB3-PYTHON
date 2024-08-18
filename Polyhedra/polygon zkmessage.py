import time
import random
from web3 import Web3
from eth_account import Account
import requests
from web3.exceptions import ValidationError

# Replace the provider URL below
provider_url = 'https://endpoints.omniatech.io/v1/matic/mainnet/public'

# Contract information and functions
contract_address = '0x8163a9b0901f63c27471b4d051b7250ecddd362d'
contract_abi = '[{"inputs":[{"internalType":"address","name":"_zkBridgeEntrypoint","type":"address"},{"internalType":"address","name":"_lzEndpoint","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":true,"internalType":"uint32","name":"dstChainId","type":"uint32"},{"indexed":true,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"string","name":"message","type":"string"}],"name":"LzMessageSend","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":true,"internalType":"uint32","name":"dstChainId","type":"uint32"},{"indexed":true,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"string","name":"message","type":"string"}],"name":"MessageSend","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"NewFee","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"bool","name":"zkBridgePaused","type":"bool"},{"indexed":false,"internalType":"bool","name":"layerZeroPaused","type":"bool"}],"name":"PauseSendAction","type":"event"},{"inputs":[],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"address","name":"_recipient","type":"address"},{"internalType":"string","name":"_message","type":"string"}],"name":"estimateLzFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"fees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"forceResumeReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"}],"name":"getConfig","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getSendVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"layerZeroPaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lzEndpoint","outputs":[{"internalType":"contract ILayerZeroEndpoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"lzChainId","type":"uint16"},{"internalType":"address","name":"lzDstAddress","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"string","name":"message","type":"string"}],"name":"lzSendMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"maxLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"zkBridgePaused_","type":"bool"},{"internalType":"bool","name":"layerZeroPaused_","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"dstAddress","type":"address"},{"internalType":"uint16","name":"lzChainId","type":"uint16"},{"internalType":"address","name":"lzDstAddress","type":"address"},{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"string","name":"message","type":"string"}],"name":"sendMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"},{"internalType":"bytes","name":"_config","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxLength","type":"uint256"}],"name":"setMsgLength","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"zkBridgeEntrypoint","outputs":[{"internalType":"contract IZKBridgeEntrypoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"zkBridgePaused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"dstAddress","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"string","name":"message","type":"string"}],"name":"zkSendMessage","outputs":[],"stateMutability":"payable","type":"function"}]'

# Function parameters
send_message_amount = Web3.toWei('0', 'ether')
dst_addresses = {
    18: '0xc773ea6E2374b500F4F29d74b38d8e38930b1bBE',
    14: '0x52c491c2afdA8b6FB361404213122644D98e0AA0',
    6: '0xfCF250b621872aceB9C0BB78AACe1F1cFc5820b1'
}
dst_chain_names = {
    18: "Celo",
    14: "Arbitrum nova",
    6: "Fantom"
}
message = 'Embrace the future of cross-chain interoperability on zkBridge! 🌈'

# Create a Web3 object
w3 = Web3(Web3.HTTPProvider(provider_url))

# Load private keys from file
with open('private_keys.txt', 'r') as file:
    private_keys = file.read().splitlines()

failed_addresses = []

total_wallets = len(private_keys)

print(f"Total wallets: {total_wallets}")
print("Networks script sends to: ZkMessage to Arbitrum Nova, Gnosis, BSC, Fantom")
print("Сибильные смски Activateeeed\n")

# Send messages for each private key
for i, private_key in enumerate(private_keys, 1):
    # Create an account object
    account = Account.from_key(private_key)
    recipient = account.address

    #dst_chain_id = random.choice([14, 3, 18, 6])
    dst_chain_id = 18

    # Create a contract object
    contract = w3.eth.contract(address=w3.toChecksumAddress(contract_address), abi=contract_abi)

    # Determine the nonce for the current account
    nonce = w3.eth.getTransactionCount(account.address)

    # Send POST request to obtain message URI
    post_data = {
        "text": "<div style=\"text-align:center\"><strong>Releasing Greenfield zkMessenger 📧</strong></div><br/><u>Polyhedra Network </u>is delighted to release Greenfield zkMessenger 📧, the first cross-chain data availability protocol powered by <u>BNB Greenfield</u> and <u>zkBridge.</u>🌈<br/><br/>With Greenfield zkMessenger, you can send Web3 emails across multiple blockchain networks, just as convenient as Internet emails. Your data is protected by <u>BNB Greenfield</u> and <u>zkBridge.</u><br/><br/>We would like to express our gratitude for the community's support.<u> Polyhedra Network </u>remains committed to launching innovative products and enhancing user experience.🎉"
    }

    response = requests.post('https://gfapi.zkbridge.com/v1/saveMessage', json=post_data)
    response_json = response.json()
    message_uri = response_json['data']['uri']

    # Estimate gas and get the current gas price
    gas_estimate = contract.functions.zkSendMessage(dst_chain_id, dst_addresses[dst_chain_id], recipient,
                                                    message_uri).estimateGas({'value': send_message_amount})
    gas_price = w3.eth.gasPrice

    # Prepare the transaction
    transaction = {
        'to': contract.address,
        'value': send_message_amount,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': nonce,
        'data': contract.functions.zkSendMessage(dst_chain_id, dst_addresses[dst_chain_id], recipient, message_uri).buildTransaction({'gas': gas_estimate, 'gasPrice': gas_price, 'nonce': nonce, 'value': send_message_amount})['data']
    }

    try:
        # Sign the transaction
        signed_txn = account.sign_transaction(transaction)

        # Send the transaction
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print(f"\n{i}/{total_wallets} | Polygon to {dst_chain_names[dst_chain_id]}: {recipient} | Transaction sent: {txn_hash.hex()}\n")
        print("===========================")

    except ValidationError as e:
        if e.args[0]['code'] == -32000 and "insufficient funds for gas * price + value" in e.args[0]['message']:
            failed_addresses.append(recipient)
            print(f'Error: Insufficient funds on the account {recipient}')
        else:
            raise

    # Delay between accounts
    time.sleep(random.randint(61, 80))
