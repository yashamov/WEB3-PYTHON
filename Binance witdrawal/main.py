from binance.spot import Spot
from loguru import logger
from random import uniform, randint
from time import sleep
    
API_KEY = '' #Ключ с личного кабинета бинанса
SECRET_KEY = '' #Второй ключ с личного кабинета бинанса

SL_EVRY_WITHDRAWAL = [10, 20] #Время в секундах от и до на которое скрипт будет засыпать после каждого вывода
WAIT_TX = 1 # Дожидаться пока бинанс сформирует транзакцию на вывод или нет. По умолчанию включено. 0 = выключено 1 = включено. по идее это может защитить от бана выводов.

AMOUNT = 0.001 #Если рандом ВЫКЛЮЧЕН тут вписываем сумму которая будет без рандома выводиться на каждый кошелек
IF_RANDOM_AMOUNT = 1 #1 = рандом включен, 0 = рандом выключен
RANDOM_AMOUNT = [0.01, 0.0105] # Если рандом включен то тут указываем значения в пределах которых будет рандомиться сумма вывода

TXT_FILE = 'wallets.txt' #Название файла со списком кошельков для вывода. Каждый кошелек с новой строки.

COIN = 'BNB' #Тикер монеты на вывод
NETWORK = 'BSC' #Сеть для вывода (ETH, Arbitrum, Optimism ...) доступны все сети которые есть в лк у Бинанса

def get_txid_from_binance_history(client, withdrawl_id):
    history = client.withdraw_history()
    for h in history:
        if h['id'] == withdrawl_id:
            tx_id = h.get('txId')
            return tx_id


def main(API_KEY, SECRET_KEY, TXT_FILE, AMOUNT, IF_RANDOM_AMOUNT, RANDOM_AMOUNT, COIN, NETWORK, SL_EVRY_WITHDRAWAL):
    logger.info('Start ...')

    client = Spot(API_KEY, SECRET_KEY)
    with open(TXT_FILE, 'r') as f:
        wallets = [i for i in [i.strip() for i in f] if i != '']
    how_many_all_wallets_in_txt = len(wallets)
    for count_wallets, address in enumerate(wallets, 1):
        if IF_RANDOM_AMOUNT == 1:
            AMOUNT = round(uniform(RANDOM_AMOUNT[0], RANDOM_AMOUNT[1]), 6)
            
        withdrawal = client.withdraw(coin=COIN, amount=AMOUNT, address=address, network=NETWORK)
        logger.info(f'Withdrawal {count_wallets} send to Binance')
        if WAIT_TX == 1:
            logger.info(f'Now wait tx hash withdrawal {count_wallets}, last up to 5 minutes dont worry')
            while True:
                withdrawal_tx = get_txid_from_binance_history(client, withdrawal['id'])
                if withdrawal_tx is not None:
                    break
            logger.success(f"withdrawal {count_wallets} DONE: {address} - {AMOUNT} {COIN} in {NETWORK} (hash tx: {withdrawal_tx})")
        else:
            wtd_detail = client.withdraw_history()
            logger.success(f"Withdrawal {count_wallets} CREATE: {address} - {AMOUNT} {COIN} (fee: {wtd_detail[0]['transactionFee']}) in {NETWORK}")
        if count_wallets != how_many_all_wallets_in_txt:
            sl = randint(SL_EVRY_WITHDRAWAL[0], SL_EVRY_WITHDRAWAL[1])
            logger.info(f'Sleep {sl} sec')
            sleep(sl)
        
    logger.success(f"Withdrawal on {how_many_all_wallets_in_txt} wallets DONE!")       

if __name__ == "__main__":
    main(API_KEY, SECRET_KEY, TXT_FILE, AMOUNT, IF_RANDOM_AMOUNT, RANDOM_AMOUNT, COIN, NETWORK, SL_EVRY_WITHDRAWAL)
