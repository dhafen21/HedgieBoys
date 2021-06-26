from td.client import TDClient
from td.option_chain import OptionChain
from config import *
from Company import *
from RegressionTesting import *
import time
import robin_stocks as r

# acc = r.robinhood.login("dhafen21@gmail.com", "basketballer15")
# msft = r.robinhood.options.get_option_historicals("MSFT", "2021-06-18", "260", "call", "5minute")

threeHundredMinutesAsMS = 300 * 60 * 1000

TDSession = TDClient(client_id=apiKey, redirect_uri=redirect_uri, credentials_path=credentials_path)


TDSession.login()
quote = TDSession.get_price_history("SPY", period_type="day", period="5", frequency_type='minute', frequency="1",
                                    extended_hours=False)

# quote = TDSession.get_price_history("TSLA", period_type="day", frequency_type="minute", frequency="5", start_date=str(round(time.time() * 1000)), end_date=str(round((time.time() * 1000) - threeHundredMinutesAsMS)), extended_hours=False)
company = Company("SPY", quote)

company.set_macd_indicators()
company.set_sma()

display_simple_macd_put_charts(company, 500)
display_simple_macd_call_charts(company)


chain = OptionChain(symbol="MSFT", contract_type="call", strike_count=1, include_quotes=True, strategy="analytical",
                    strike=249.77, opt_range="otm")
a = TDSession.get_options_chain(chain)



