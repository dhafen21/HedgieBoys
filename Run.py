from config import *
from Setup import *
from RegressionTesting import *
from MACDSimpleStrategy import *
import time

TDSession = TDClient(client_id=apiKey, redirect_uri=redirect_uri, credentials_path=credentials_path)
TDSession.login()

tradeList = ["SPY", "AAPL", "TSLA", "BA", "AMZN"]
# tradeList = ["AMZN"]


companies = initialize_companies(tradeList, TDSession)
init_macd_indicators(companies)
#
# while time.localtime().tm_hour < 15:
#     while time.localtime().tm_min % 5 != 0:
#         time.sleep(1)
#     update_company_prices(companies, TDSession)
#     init_macd_indicators(companies)
#     update_call_pos(companies)
#     update_put_pos(companies)

profit = 0.0
for company in companies:
    profit = profit + display_simple_macd_call_charts(company)
    profit = profit + display_simple_macd_put_charts(company)