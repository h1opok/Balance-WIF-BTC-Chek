from bit import Key
from bit.format import bytes_to_wif
import random
import time
import threading

start_time = time.time()
total_checked = 0
key_with_balance = 0

# Файл для записи ключей с балансом
output_file = open("keys_with_balance.txt", "w")

def generate_key():
    # Генерация случайных приватных ключей
    private_key = bytes.fromhex(format(random.getrandbits(256), 'x').zfill(64))
    wif = bytes_to_wif(private_key, compressed=False)  # Изменение здесь на False
    key = Key(wif)
    return private_key, wif, key

def check_address():
    global total_checked, key_with_balance
    while True:
        private_key, wif, key = generate_key()
        if key.balance > 0:
            print("Found key with balance:", wif)
            key_with_balance += 1
            # Запись ключа с балансом в файл
            output_file.write(wif + "\n")
        total_checked += 1
        if total_checked % 1000 == 0:
            elapsed_time = time.time() - start_time
            speed = total_checked / elapsed_time
            print("Total checked:", total_checked)
            print("Speed:", speed, "keys per second")
            print("Current key being checked:", wif)
            print("Balance:", key.balance)
            print("Keys with balance:", key_with_balance)  # Отображение количества найденных ключей с балансом

num_threads = 3
threads = []

for _ in range(num_threads):
    t = threading.Thread(target=check_address)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

output_file.close()

elapsed_time = time.time() - start_time
print("Total checked:", total_checked)
print("Total keys with balance:", key_with_balance)
print("Execution time:", elapsed_time)
