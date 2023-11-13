from bit import Key
from bit.format import bytes_to_wif
import random
import time
import threading
import logging

class KeyGenerator:
    def __init__(self, output_file_path="keys_with_balance.txt"):
        self.output_file_path = output_file_path
        self.total_checked = 0
        self.key_with_balance = 0
        self.output_file = open(self.output_file_path, "w")

    def generate_key(self):
        private_key = bytes.fromhex(format(random.getrandbits(256), 'x').zfill(64))
        wif = bytes_to_wif(private_key, compressed=False)
        key = Key(wif)
        return private_key, wif, key

    def check_address(self):
        while True:
            private_key, wif, key = self.generate_key()
            if key.balance > 0:
                logging.info("Found key with balance: %s", wif)
                self.key_with_balance += 1
                self.output_file.write(wif + "\n")
            self.total_checked += 1
            if self.total_checked % 1000 == 0:
                self.log_statistics(wif, key)

    def log_statistics(self, wif, key):
        elapsed_time = time.time() - start_time
        speed = self.total_checked / elapsed_time
        logging.info("Total checked: %d", self.total_checked)
        logging.info("Speed: %f keys per second", speed)
        logging.info("Current key being checked: %s", wif)
        logging.info("Balance: %s", key.balance)
        logging.info("Keys with balance: %d", self.key_with_balance)

    def run_threads(self, num_threads=3):
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=self.check_address)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def close_output_file(self):
        self.output_file.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_time = time.time()

    key_generator = KeyGenerator()
    key_generator.run_threads()
    key_generator.close_output_file()

    elapsed_time = time.time() - start_time
    logging.info("Total checked: %d", key_generator.total_checked)
    logging.info("Total keys with balance: %d", key_generator.key_with_balance)
    logging.info("Execution time: %f", elapsed_time)
