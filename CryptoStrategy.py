from CryptoTrader import *
import matplotlib.pyplot as plt
import time
import pyotp
from dotenv import load_dotenv
import os

load_dotenv()

totp = pyotp.TOTP(os.environ['robin_mfa']).now()
print("Current OTP:", totp)
# Here I am setting store_session=False so no pickle file is used.
login = r.login(os.environ['robin_username'],
                os.environ['robin_password'], store_session=False, mfa_code=totp)

timeSeries_length = 100

trader = CryptoTrader()
trader.init_currencies(["BCH", "BSV", "ETC", "LTC"])
trader.init_timeseries()

def get_strategy():
    try:
        f = open("Currencies/StrategyToExecute.txt", "r")
    except FileNotFoundError:
        f = open("Crypto2/Currencies/StrategyToExecute.txt", "r")

    val = f.read()
    f.close()
    return val

while True:

    strategy = ""
    if time.localtime().tm_min % 3 == 0:
        strategy = get_strategy()
    if strategy == "clean":
        break

    action = trader.flow1()
    if action:
        print_time()
        print("____________\n")
    time.sleep(60)

while trader.num_positions > 0:
    trader.clean_up()
    time.sleep(15)
