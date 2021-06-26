import talib as tl

def macd(series, fastperiod = 12, slowperiod = 26, signalperiod = 9):
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