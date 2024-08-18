import requests
import time
import random
import asyncio

def get_block_data(client_url, block_number):
    # Получение данных о блоке по его номеру через запрос к узлу Ethereum
    response = requests.post(client_url, json={"jsonrpc": "2.0", "method": "eth_getBlockByNumber", "params": [hex(block_number), True], "id": 1})
    if response.status_code == 200:
        block = response.json().get("result")
        if block:
            print(f"Block Number: {block_number}")
            print(f"Timestamp: {block['timestamp']}")
            print(f"Number of Transactions: {len(block['transactions'])}")
            print("----")
        else:
            print("Block not found.")
    else:
        print(f"Failed to retrieve block data. Status code: {response.status_code}")

def get_latest_block_number(client_url):
    # Получение номера последнего сгенерированного блока через запрос к узлу Ethereum
    response = requests.post(client_url, json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1})
    if response.status_code == 200:
        result = response.json().get("result")
        latest_block_number_hex = result if isinstance(result, str) else None
        if latest_block_number_hex:
            latest_block_number = int(latest_block_number_hex, 16)
            return latest_block_number
        else:
            print("Latest block number is not a valid hexadecimal string.")
            return None
    else:
        print(f"Failed to retrieve latest block number. Status code: {response.status_code}")
        return None
    
async def runner(provider: str, proxy: str):
    # Подключение к узлу Ethereum (например, Infura) через прокси
    client_url = provider
    proxies = {"http": proxy, "https": proxy}
    
    while True:
        time_to_wait = random.uniform(10, 45)
        try:
            latest_block_number = get_latest_block_number(client_url)
            if latest_block_number:
                get_block_data(client_url, latest_block_number)
            print(f"Waiting for {time_to_wait:.2f} seconds before the next attempt...")
        except Exception as e:
            print(f"Error in main loop: {e}")
            print(f"Waiting for a random time ({time_to_wait:.2f} seconds) before retrying...")

        await asyncio.sleep(time_to_wait)

async def main():
    with open("providers.txt", "r") as file:
        providers = file.readlines()
    with open("proxies.txt", "r") as file:
        proxies = file.readlines()
    tasks = [runner(provider.strip(), proxy.strip()) for provider in providers for proxy in proxies]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())