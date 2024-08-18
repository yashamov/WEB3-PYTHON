import requests
import random
import time


def parse_data(wallet_address, mode):
    if mode == 1:
        random_number = random.randint(1, 15)
        url = f"https://api.reya.xyz/api/xp/generate-game-boost-rate/{wallet_address}/child{random_number}"
    elif mode == 2:
        url = f"https://api.reya.xyz/api/xp/lock-game-boost-rate/{wallet_address}"
    elif mode == 3:
        url = f"https://api.reya.xyz/api/xp/user-game-status/{wallet_address}"
    else:
        return "Invalid mode specified"

    try:
        response = requests.get(url)
        data = response.json()

        if mode == 1:
            boostRate_value = data.get("boostRate")
            return f"{wallet_address} - {boostRate_value}"
        elif mode == 2:
            return "Boost activated successfully"
        elif mode == 3:
            status = data.get("status")
            if status == "lockedIn":
                boostRate_value = data.get("boostRate")
                return f"{wallet_address} - Boost is activated : {boostRate_value}"
            elif status == "notLocked":
                return f"{wallet_address} - Boost is not activated"
            else:
                return "Unknown status"
    except Exception as e:
        return f"Error: {e}"


def main():
    # Выбор режима работы
    mode = int(input("Enter mode (1: Choose multiplier, 2: Activate boost, 3: Check status): "))

    # Чтение списка кошельков из файла
    with open("wallets.txt", "r") as file:
        wallets = file.read().splitlines()

    # Парсинг значений для каждого кошелька
    for wallet_address in wallets:
        parsed_data = parse_data(wallet_address, mode)
        print(parsed_data)

        # Генерация случайной задержки от 5 до 15 секунд и вывод в лог
        delay = random.randint(10, 30)
        time.sleep(delay)


if __name__ == "__main__":
    main()
