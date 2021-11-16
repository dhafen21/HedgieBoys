from TechnicalIndicators import *
import numpy


class Company:

    current_order = None
    last_buy = None

    def __init__(self, name, time_series):
        self.name = name
        self.time_series = time_series["candles"]
        self.close = numpy.array([float(stick["close"]) for stick in self.time_series])
        self.open = numpy.array([float(stick["open"]) for stick in self.time_series])
        self.high = numpy.array([float(stick["high"]) for stick in self.time_series])
        self.low = numpy.array([float(stick["low"]) for stick in self.time_series])
        self.volume = numpy.array([float(stick["volume"]) for stick in self.time_series])
        self.datetime = numpy.array([stick["datetime"] for stick in self.time_series])
        self.macd = None
        self.signal = None
        self.histogram = None
        self.sma = None
        self.plot = None
        self.call_pos = False
        self.put_pos = False
        self.holding = False
        self.price = 0

    def __init__(self, name):
        self.name = name
        self.holding = False
        self.price = 0

    def get_signal(self):
        """
        Getter for the signal line of the MACD

        :return: numpy array containing the signal line for the MACD
        """
        return self.signal

    def get_macd(self):
        """
        Getter for the MACD line

        :return: numpy array containing the MACD line
        """
        return self.macd

    def get_sma(self):
        """
        Getter for the SMA of a price

        :return: return numpy array for the simple moving average of a price
        """
        return self.sma

    def set_sma(self, period: int = 9):
        """
        Sets the simple moving average for the company

        :param period: Lookback period used when setting the simple moving average
        :return: No return. Sets the SMA property for the company
        """
        self.sma = sma(period, self.close)

    def set_macd_indicators(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        """
        Sets the MACD line Signal line and the Histogram line

        :param fastperiod: This is the lookback period for the shorter exponential moving average of the MACD
        :param slowperiod: The lookback period for the longer exponential moving average of the MACD
        :param signalperiod: The lookback for the Exponential moving average of the MACD Line
        :return: No return. Sets the MACD properties for the company
        """
        self.macd, self.signal, self.histogram = macd(self.close, fastperiod, slowperiod, signalperiod)

    def reset_time_series(self, time_series):
        self.time_series = time_series
        self.close = numpy.array([float(stick.c) for stick in self.time_series])
        self.open = numpy.array([float(stick.o) for stick in self.time_series])
        self.high = numpy.array([float(stick.h) for stick in self.time_series])
        self.low = numpy.array([float(stick.l) for stick in self.time_series])
        self.volume = numpy.array([float(stick.v) for stick in self.time_series])
        self.datetime = numpy.array([stick.t for stick in self.time_series])
