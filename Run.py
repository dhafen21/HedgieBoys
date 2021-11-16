import time
from VolatilityTradingStrategy import *


if __name__== "__main__":
    api = tradeapi.REST(paper_api_key_hafen_school, paper_secret_key_hafen_school, paper_url, api_version='v2')
    #
    # while not api.get_clock().is_open:
    #     time.sleep(300)
    #     print("Market is not open yet")
    #
    while api.get_clock().is_open:
        run_live()
