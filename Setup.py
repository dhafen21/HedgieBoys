from td.client import TDClient
from td.client import OptionChain
from Company import *


def initialize_companies(company_array: [], td: TDClient, period = "5") -> [Company]:
    companies = []
    for company in company_array:
        quote = td.get_price_history(company, period_type="day", period=period, frequency_type='minute',
                                            frequency="1",
                                            extended_hours=False)
        companies.append(Company(company, quote))
    return companies

def init_indicators(companies: [Company]):
    for company in companies:
        company.set_macd_indicators()
        company.set_sma()