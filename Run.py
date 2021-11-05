from config import *
from Setup import *
from MACDSimpleStrategy import *
import time


if __name__== "__main__":
    TDSession = TDClient(client_id=apiKey, redirect_uri=redirect_uri, credentials_path=credentials_path)
    TDSession.login()

    api = tradeapi.REST(paper_api_key_hafen_school, paper_secret_key_hafen_school, paper_url, api_version='v2')

    tradeList = ["SPY", "AAPL", "TSLA", "BA", "AMZN"]

    companies = init_companies_alpaca(tradeList, api)
    init_macd_indicators(companies)
    #
    while api.get_clock().is_open:
        while time.localtime().tm_min % 5 != 0:
            time.sleep(1)
        time.sleep(20)
        print("------------------")
        update_last_price(companies)
        init_macd_indicators(companies)
        update_call_pos(companies)
        print("------------------\n")
        time.sleep(100)

