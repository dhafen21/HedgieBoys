from td.client import TDClient
from td.client import OptionChain
from Company import *


def initialize_companies(company_array: [], td: TDClient, period_type: str = "day", period: str = "5",
                         freq_type: str = "minute", freq="5") -> [Company]:
    """
    Takes in a simple list of company tickers, and returns an array of Company objects with an initalized
    price time series.

    Valid period_types and period:
        day: 1, 2, 3, 4, 5, 10*
        month: 1*, 2, 3, 6
        year: 1*, 2, 3, 5, 10, 15, 20
        ytd: 1*

    Valid freq_type and freq:
        minute: 1*, 5, 10, 15, 30
        daily: 1*
        weekly: 1*
        monthly: 1*

    :param freq: the frequency or time between candles.
    :param freq_type:
    :param period_type:
    :param company_array: List of company tickers to create companies. Strings in this list
    must be the ticker symbol, and must be in all caps
    :param td: The TDAmeritade client that is used to get the time series for all the companies.
    :param period:
    :return:
    """
    companies = []
    for company in company_array:
        quote = td.get_price_history(company, period_type=period_type, period=period, frequency_type=freq_type,
                                     frequency=freq,
                                     extended_hours=False)
        companies.append(Company(company, quote))
    return companies


def init_macd_indicators(companies: [Company], fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
    """
    Takes in a list of company objects and calculates the MACD for each of them
    :param fastperiod: This is the lookback period for the shorter exponential moving average of the MACD
    :param slowperiod: The lookback period for the longer exponential moving average of the MACD
    :param signalperiod: The lookback for the Exponential moving average of the MACD Line
    :param companies: list of Company objects with initialized time series
    :return:
    """
    for company in companies:
        company.set_macd_indicators(fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        company.set_sma()
