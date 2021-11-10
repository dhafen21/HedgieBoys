import time
import Company
import numpy as np
import talib as tl
from datetime import datetime
import requests
import json


def macd(series, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    :param series: numpy array representing the closing prices for a given
    stock. Intervals and periods can vary
    :param fastperiod: the lookback period for the shorter of the MACD EMA periods
    :param slowperiod: the lookback period for the longer of the MACD EMA periods
    :param signalperiod: the lookback for the signal EMA line
    :return:
    MACD, Signal line, and Histogram
    """
    macd, signal, hist = tl.MACD(series, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, signal, hist


def ema(period: int, series):
    """

    :param period:
    :param series:
    :return:
    """
    return tl.EMA(series, period)


def sma(period: int, series):
    return tl.SMA(series, period)


def ts2string(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y, %H:%M:%S")


def nasdaq_current_price(name):
    """
    Reutrns the current price for the given asset

    :param name: The ticker symbol for the company name
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

    url = "https://api.nasdaq.com/api/quote/{}/info?assetclass=stocks".format(name)

    try:
        page = requests.get(url, headers=headers)
    except:
        print("could not load price for {}".format(name))
        return

    content = json.loads(page.text)

    price = content["data"]["primaryData"]["lastSalePrice"]

    return float(price.split('$')[1])


def standard_deviation(series):
    """
    Returns the standard deviation for a time series list
    :param series: list of time series data
    :return: the standard deviation for the time series
    """
    a = np.array([x for x in series])
    return np.std(a)


def get_ema_difference(p1: int, p2: int, company: Company):
    """
    The difference between two EMAs gives a rough approximation of the second derivative of a time series.
    a larger difference denotes how how fast a price is increasing or decreasing
    :param p1: Period for the shorteer exponential moving average
    :param p2:  Period for the longer exponential moving average
    :param company: Company to calculate the difference in EMA for.
    :return: Difference between the two EMAs
    """
    short_ema = ema(p1, company.close)
    long_ema = ema(p2, company.close)
    difference = short_ema[p2:] - long_ema[p2:]
    return difference


def print_time():
    """
    Prints the current local time.
    :return:
    """
    print("{}:{}:{}".format(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))


def get_trade_list():
    """
    Initializes a list of companies to trade from TradeList.txt. If file does not exist, returns empty array
    :return: array of ticker symbols to trade
    """
    company_names = []

    try:
        file = open("TradeList.txt", 'r')
    except FileNotFoundError:
        print("The file does not exist in the directory. Please create a 'TradeList.txt' file.")
        return np.array([])

    for line in file:
        name = line.rstrip()
        company_names.append(name)

    file.close()

    return company_names
