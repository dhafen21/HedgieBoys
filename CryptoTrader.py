import numpy

from config import *
import robin_stocks.robinhood as r
import yfinance as yf
import numpy as np
import talib
from Currency import *
import time
from TechnicalIndicators import *


class CryptoTrader:
    currencies = []
    num_positions = 0
    symbols = []

    def init_currencies(self, currency_list=None):
        if currency_list is None:
            currency_list = ["BTC", "ETH", "BSV", "BCH", "DOGE", "LTC", "ETC"]

        self.symbols = currency_list

        for symbol in currency_list:
            self.currencies.append(Currency(symbol))

        self.init_purchased_currencies()

    def init_timeseries(self):
        for currency in self.currencies:
            series = r.crypto.get_crypto_historicals(currency.symbol, "5minute", "day")
            series = [float(x["close_price"]) for x in series]
            currency.timeSeries = numpy.array(series)
            self.set_ema_diference(5, 100, currency)
            currency.std_dev = standard_deviation(currency.ema_difference)

    def set_ema_diference(self, p1: int, p2: int, currency):
        short_ema = ema(p1, currency.timeSeries)
        long_ema = ema(p2, currency.timeSeries)
        currency.ema_difference = long_ema[p2:] - short_ema[p2:]
        currency.std_dev = standard_deviation(currency.ema_difference)


    def init_purchased_currencies(self):
        currencies = r.get_crypto_positions()
        for currency in currencies:
            symbol = currency['currency']['code']
            if symbol in self.symbols:
                quantity = float(currency['quantity'])
                if quantity != 0:
                    print("Initializing Sell info for {}".format(symbol))
                    for currency in self.currencies:
                        if currency.symbol == symbol:
                            ini_inv = self.read_file(currency)
                            purch_price = float(ini_inv) / quantity
                            currency.sell_goal = purch_price + currency.std_dev
                            print("Sell goal for {} is {}".format(currency.symbol, currency.sell_goal))
                            currency.waiting_for_sell = True
                            currency.waiting_for_buy = False
                            currency.purchased_quantity = quantity
                            self.num_positions += 1

    def five_minute_variation(self, currency: Currency):
        local_max = max(currency.timeSeries[-20:])
        local_min = min(currency.timeSeries[-20:])

        currency.volatility = (local_max - local_min) / local_min

    def rsi(self, currency: Currency, minutes):
        if minutes == 0:
            currency.rsi = 0
            return
        rsi_lookback = minutes * 4
        currency.rsi = (talib.RSI(currency.timeSeries[-(rsi_lookback + 1):], rsi_lookback))[-1]

    def get_historical_crypto_price(self, currency: Currency):
        currency.timeSeries = currency.timeSeries[-20:]
        self.get_current_price(currency)
        currency.timeSeries = np.append(currency.timeSeries, currency.current_price)

    def get_current_price(self, currency: Currency):
        currency.current_price = float(r.get_crypto_quote(currency.symbol)["mark_price"])
        return currency.current_price

    def five_min_average_price(self, currency: Currency):
        """Calculates the price average over the last 5 minutes"""
        currency.average = np.average(currency.timeSeries[-20:])

    def update_currency_indicators(self, currency: Currency, rsi_lookback):
        """Calculates each of the data members for the currency"""
        self.get_historical_crypto_price(currency)
        self.five_minute_variation(currency)
        self.rsi(currency, rsi_lookback)
        self.five_min_average_price(currency)

    def flow1(self):
        action = False
        for currency in self.currencies:
            time.sleep(2)
            cur_price = self.get_current_price(currency)
            currency.timeSeries = numpy.delete(numpy.append(currency.timeSeries, [cur_price]), 0)
            self.set_ema_diference(5, 100, currency)
            if currency.waiting_for_buy:
                action = self.waiting_for_buy(currency) or action
            elif currency.waiting_for_buy_execution:
                action = self.waiting_for_buy_execution(currency) or action
            elif currency.waiting_for_sell:
                action = self.waiting_for_sell(currency) or action
            elif currency.waiting_for_sell_execution:
                action = self.waiting_for_sell_execution(currency) or action
        return action



    def flow(self, decrease, goal_increase, decrease_lookback, rsi_lookback, rsi_threshold):
        """Pattern recognition that decides when to buy and sell
        :param decrease: the desired percent decrease given from the high in the currency timeseries
        :type info: float
        :param goal_increase: desired increase for the given currency. Sets the sell threshold
        :type goal_increase: float
        :param decrease_lookback: desired lookback length in minutes for last high
        :type decrease_lookback: int
        :param rsi_lookback: lookback length for rsi threshold
        :type rsi_lookback: int
        :param rsi_threshold: Smalles threshold for when to buy the stock for the rebound
        :type rsi_threshold: int
        :returns: None"""

        for currency in self.currencies:
            time.sleep(1)  ##Lets make sure robinhood doesn't ban us
            self.update_currency_indicators(currency, rsi_lookback)
            if currency.waiting_for_buy:
                self.waiting_for_buy(currency)
            elif currency.waiting_for_buy_execution:
                self.waiting_for_buy_execution(currency)
            elif currency.waiting_for_sell:
                self.waiting_for_sell(currency)
            elif currency.waiting_for_sell_execution:
                self.waiting_for_sell_execution(currency)

    def clean_up(self, rsi_lookback=0):
        for currency in self.currencies:
            time.sleep(1)
            self.update_currency_indicators(currency, rsi_lookback)
            if currency.waiting_for_sell:
                self.waiting_for_sell(currency)
            elif currency.waiting_for_buy_execution:
                self.waiting_for_sell_execution(currency)

    def waiting_for_buy(self, currency: Currency):
        if currency.ema_difference[-1] > (2 * currency.std_dev):
            print("Buying {} at {}".format(currency.symbol, currency.current_price))
            stock_value = self.read_file(currency)
            if stock_value == '':
                print("Could not read file for {}".format(currency.symbol))
                return True
            try:
                if currency.symbol == "DOGE":
                    currency.current_order = self.dogeHelper(float(stock_value))
                else:
                    currency.current_order = r.order_buy_crypto_by_price(currency.symbol, float(stock_value), "gtc")
            except:
                print("was not able to submit a buy order")
                currency.waiting_for_buy = True
                return True
            currency.waiting_for_buy = False
            currency.waiting_for_buy_execution = True
        else:
            return False

    def waiting_for_buy_execution(self, currency: Currency):
        try:
            currency.current_order = r.get_crypto_order_info(currency.current_order["id"])
        except:
            print("cannot find the buy order for {}".format(currency.symbol))
            currency.waiting_for_buy_execution = False
            currency.waiting_for_buy = True
            return True

        if currency.current_order['state'] == 'canceled':
            print("The order for {} was canceled".format(currency.symbol))
            currency.waiting_for_buy_execution = False
            currency.waiting_for_buy = True
            return True
        try:
            if currency.current_order["average_price"] is not None:
                currency.waiting_for_sell = True
                currency.calc_sell_goal()
                currency.purchased_quantity = float(currency.current_order["quantity"])
                currency.waiting_for_buy_execution = False
                print("{} buy executed at Avg Price: {}, sell goal is {}".format(currency.symbol, currency.current_order["average_price"], currency.sell_goal))
                self.num_positions += 1
            else:
                print("{} buy order not filled yet".format(currency.symbol))
                currency.num_failed_executions += 1
                if currency.num_failed_executions > 2:
                    print("Canceling buy order for {}".format(currency.symbol))
                    r.cancel_crypto_order(currency.current_order["id"])
                    currency.num_failed_executions = 0
                    currency.waiting_for_buy_execution = False
                    currency.waiting_for_buy = True
        except:
            print("bad buy order for {}".format(currency.symbol))
        return True

    def waiting_for_sell(self, currency: Currency):
        try:
            currency.current_order = r.order_sell_crypto_limit(currency.symbol, currency.purchased_quantity, round(currency.sell_goal, 2))
            currency.waiting_for_sell_execution = True
            currency.waiting_for_sell = False
            print("submitting sell order for {}".format(currency.symbol))
        except:
            print("Created bad sell order for {}".format(currency.symbol))
        return True

    def waiting_for_sell_execution(self, currency: Currency):
        try:
            currency.current_order = r.get_crypto_order_info(currency.current_order["id"])
        except:
            print("cannot find the sell order for {}".format(currency.symbol))

        if currency.current_order['state'] == 'canceled':
            currency.waiting_for_buy_execution = False
            return True
        try:
            if currency.current_order["average_price"] is not None:
                stock_value = float(currency.current_order["quantity"]) * float(currency.current_order["average_price"])
                print("Limit order for {} was executed".format(currency.symbol))
                print("Current value is: {}, waiting_for_sell quantity is: {}, stock value is: {}".format(
                    currency.current_price, currency.purchased_quantity, stock_value))
                self.write_file(currency, str(stock_value))
                currency.waiting_for_sell = False
                currency.waiting_for_sell_execution = False
                currency.waiting_for_buy = True
                currency.num_failed_executions = 0
                self.num_positions -= 1
        except:
            print("Bad sell order")
            currency.waiting_for_sell_execution = False
            currency.waiting_for_buy = True
        return True

    def get_end_totals(self):
        for currency in self.currencies:
            total = 0
            total = self.read_file(currency)
            print(total)

    def dogeHelper(self, amountInDollars, priceType='ask_price', timeInForce='gtc'):
        from uuid import uuid4
        import robin_stocks.crypto as crypto
        import robin_stocks.helper as helper
        import robin_stocks.urls as urls

        symbol = "DOGE"

        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message, file=helper.get_output())
            return None

        crypto_info = crypto.get_crypto_info(symbol)
        price = helper.round_price(crypto.get_crypto_quote_from_id(
            crypto_info['id'], info=priceType))

        try:
            shares = helper.round_price(amountInDollars / price)
        except:
            shares = 0

        shares = int(shares)

        payload = {
            'account_id': crypto.load_crypto_profile(info="id"),
            'currency_pair_id': crypto_info['id'],
            'price': price,
            'quantity': shares,
            'ref_id': str(uuid4()),
            'side': 'buy',
            'time_in_force': timeInForce,
            'type': 'market'
        }

        print("price: {}, shares: {}".format(price, shares))

        url = urls.order_crypto()
        data = helper.request_post(url, payload, json=True)
        return (data)

    def read_file(self, currency: Currency):
        try:
            f = open("Currencies/{}.txt".format(currency.symbol), "r")
        except FileNotFoundError:
            f = open("Crypto2/Currencies/{}.txt".format(currency.symbol), "r")

        val = f.read()
        f.close()
        return val

    def write_file(self, currency: Currency, stock_value):
        try:
            f = open("Currencies/{}.txt".format(currency.symbol), "w")
        except FileNotFoundError:
            f = open("Crypto2/Currencies/{}.txt".format(currency.symbol), "w")

        f.write(stock_value)
        f.close()