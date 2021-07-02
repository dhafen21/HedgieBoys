from config import *
from Setup import *
from RegressionTesting import *

TDSession = TDClient(client_id=apiKey, redirect_uri=redirect_uri, credentials_path=credentials_path)
TDSession.login()

tradeList = ["SPY", "AAPL", "TLSA", "BA", "AMZN"]

companies = initialize_companies(tradeList, TDSession)
init_indicators(companies)

for company in companies:
    display_simple_macd_call_charts(company)