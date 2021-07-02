import matplotlib.pyplot as plt
from Company import *


def display_simple_macd_call_charts(company: Company, lookback: int = None) -> float:
    """
    Displays two charts. One is the MACD line and the signal line. the second chart displays the price
    It also plots the position of the hypothetical buys and sells when buying on convergence to the upside
    and selling when the price dips below the simple moving average.

    :param company: The company (instance of Company class) that is being tested
    :param lookback: How long of a period to examine / backtest
    :return: returns the hypothetical profit from this strategy
    """

    if lookback is None:
        lookback = len(company.close) - 33
    bought = False

    col = ["white"]

    profit = 0
    buy_price = 0

    for i in range(1, len(company.macd[-lookback:])):
        if not bought:
            if company.macd[-lookback:][i] > 0 and company.signal[-lookback:][i] > 0:
                if company.macd[-lookback:][i - 1] <= company.signal[-lookback:][i - 1] \
                        and company.macd[-lookback:][i] > company.signal[-lookback:][i]:
                    col.append("green")
                    bought = True
                    buy_price = company.close[-lookback:][i]
                else:
                    col.append("white")
            else:
                col.append("white")
        else:
            if company.close[-lookback:][i] < company.sma[-lookback:][i]:
                col.append("red")
                bought = False
                sell_price = company.close[-lookback:][i]
                profit = profit + (sell_price - buy_price)
            else:
                col.append("white")
    col.append("white")

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(company.macd[-lookback:], label="macd")
    ax1.plot(company.signal[-lookback:], label="signal")

    ax2.plot(company.close[-lookback:], label="Price")
    ax2.plot(company.sma[-lookback:], label="SMA")
    for i in range(len(company.macd[-lookback:])):
        if col[i] != "white":
            ax1.scatter(x=i, y=0, c=col[i], s=18)
            ax2.scatter(x=i, y=company.close[-lookback:][i], c=col[i], s=18)
    ax1.legend()
    ax2.legend()
    ax2.text(0.1, 1.1, "{}: Total profit: ${}".format(company.ticker, round(profit * 100) / 100),
             horizontalalignment='center', verticalalignment='center',
             transform=ax1.transAxes)

    print("{} total profit: {}".format(company.ticker, profit))
    plt.savefig("Plots/{}_plot.pdf".format(company.ticker))
    company.plot = ax1
    return profit


def backtest_simple_macd_call(company: Company) -> float:
    """
    Similar to the plotting function, it just does not create a graph. Only used for backtesting and getting
    a hypothetical profit value.

    :param company: The company (instance of Company class) that is being tested
    :return: float that contains hypothetical profits from this strategy
    """

    lookback = len(company.close) - 33

    profit = 0
    buy_price = 0
    bought = False

    for i in range(1, len(company.macd[-lookback:])):
        if not bought:
            if company.macd[-lookback:][i] > 0 and company.signal[-lookback:][i] > 0:
                if company.macd[-lookback:][i - 1] <= company.signal[-lookback:][i - 1] \
                        and company.macd[-lookback:][i] > company.signal[-lookback:][i]:
                    bought = True
                    buy_price = company.close[-lookback:][i]
        else:
            if company.close[-lookback:][i] < company.sma[-lookback:][i]:
                bought = False
                sell_price = company.close[-lookback:][i]
                profit = profit + (sell_price - buy_price)

    print("Total profit: {}".format(profit))
    return profit

def display_simple_macd_put_charts(company: Company, lookback: int = None) -> float:
    """
    Displays two charts. One is the MACD line and the signal line. the second chart displays the price
    It also plots the position of the hypothetical buys and sells when buying on divergence to the downside
    and selling when the price increases above the simple moving average.

    :param company: The company (instance of Company class) that is being tested
    :param lookback: How long of a period to examine / backtest
    :return: returns the hypothetical profit from this strategy
    """

    if lookback is None:
        lookback = len(company.close) - 33
    bought = False

    col = ["white"]

    profit = 0
    buy_price = 0

    for i in range(1, len(company.macd[-lookback:])):
        if not bought:
            if company.macd[-lookback:][i] < 0 and company.signal[-lookback:][i] < 0:
                if company.macd[-lookback:][i - 1] >= company.signal[-lookback:][i - 1] \
                        and company.macd[-lookback:][i] < company.signal[-lookback:][i]:
                    col.append("green")
                    bought = True
                    buy_price = company.close[-lookback:][i]
                else:
                    col.append("white")
            else:
                col.append("white")
        else:
            if company.close[-lookback:][i] > company.sma[-lookback:][i]:
                col.append("red")
                bought = False
                sell_price = company.close[-lookback:][i]
                profit = profit + (buy_price - sell_price)
            else:
                col.append("white")
    col.append("white")

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(company.macd[-lookback:], label="macd")
    ax1.plot(company.signal[-lookback:], label="signal")

    ax2.plot(company.close[-lookback:], label="Price")
    ax2.plot(company.sma[-lookback:], label="SMA")
    for i in range(len(company.macd[-lookback:])):
        if col[i] != "white":
            ax1.scatter(x=i, y=0, c=col[i], s=18)
            ax2.scatter(x=i, y=company.close[-lookback:][i], c=col[i], s=18)
    ax1.legend()
    ax2.legend()
    ax2.text(0.1, 1.1, "{}: Total profit: ${}".format(company.ticker, round(profit * 100) / 100),
             horizontalalignment='center', verticalalignment='center',
             transform=ax1.transAxes)

    print("{} total profit: {}".format(company.ticker, profit))
    plt.savefig("Plots/{}_plot.pdf".format(company.ticker))
    company.plot = ax1
    return profit
