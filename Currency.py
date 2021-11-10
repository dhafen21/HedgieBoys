import numpy as np

class Currency:

    timeSeries = np.array([])
    waiting_for_buy = True
    current_order = None
    current_price = None
    rsi = None
    volatility = None
    sell_goal = None
    average = None
    waiting_for_sell = None
    purchased_quantity = None
    waiting_for_buy_execution = None
    waiting_for_sell_execution = None
    num_failed_executions = 0
    std_dev = 0
    ema_difference = None

    def __init__(self, symbol):
        self.symbol = symbol

    def calc_sell_goal(self):
        self.sell_goal = float(self.current_order["average_price"]) + (.5 *self.std_dev)
