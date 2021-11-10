from config import *
from TechnicalIndicators import *
import alpaca_trade_api as tradeapi
from Setup import *
import numpy
import robin_stocks as r
import pyotp


def run_backtest():
    api = tradeapi.REST(paper_api_key_hafen_school, paper_secret_key_hafen_school, paper_url, api_version='v2')

    names = ["DIS", "SHOP", "AMZN", "AMAT", "AMD", "NVDA", "FVRR", "CRM", "SQ", "AAPL", "MSFT", "FB", "COIN", "QCOM", ]
    companies = init_companies_alpaca(names, api, "1Min", 1000)

    bag = 10000
    allocaiton = 3000
    profit = 0

    for company in companies:
        difference = get_ema_difference(5, 100, company)
        std = standard_deviation(difference)
        for i in range(len(difference)):
            time = company.datetime[100:]
            price = company.close[100:]
            if not company.holding:
                if difference[i] > (2 * std):
                    if bag > 0:
                        print("\nBuy at time: {}, price {}".format(time[i], price[i]))
                        company.holding = True
                        company.price = price[i]
                        bag -= allocaiton
                    else:
                        print("We got no more damn money")
            else:
                if price[i] > company.price + std:
                    print("sold {} at {}".format(company.name, price[i]))
                    profit += ((price[i] - company.price) / company.price) * allocaiton
                    company.holding = False
                    bag += allocaiton

    for comp in companies:
        if comp.holding:
            print("Got caught holding the bag with {}".format(comp.name))
    print("\nProfit was: {}".format(profit))


def run_live():
    api = tradeapi.REST(paper_api_key_hafen_school, paper_secret_key_hafen_school, paper_url, api_version='v2')
    names = get_trade_list()
    companies = init_companies_alpaca(names, api, "1Min", 1000)
    init_purchased_companies(api, companies)

    while time.localtime().tm_hour < 15:
        update_positions(api, companies)
        print("sleeping")
        time.sleep(60)


def update_positions(api: tradeapi, companies: [Company]):
    for company in companies:
        try:
            curPrice = nasdaq_current_price(company.name)
            time.sleep(1)
        except:
            print("bad price for {}".format(company.name))
            break
        company.close = np.append(company.close[1:], [curPrice])
        difference = get_ema_difference(5, 100, company)
        std = standard_deviation(difference)
        if not company.holding:
            if difference[-1] < -2 * std:
                buying_power = float(api.get_account().buying_power)
                if buying_power < 10000:
                    print("not enough money")
                    break
                comp_price = nasdaq_current_price(company.name)
                print("Buying {}".format(company.name))
                try:
                    company.current_order = api.submit_order(
                        symbol=company.name,
                        qty=round(20000 / comp_price),
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                except Exception as e:
                    print(e)
                    print("Order for {} didn't work".format(company.name))
                    break
                company.holding = True
                while True:
                    company.current_order = api.get_order(company.current_order.id)
                    if company.current_order.filled_at is not None:
                        break
                    time.sleep(5)
                company.current_order = api.submit_order(
                    symbol=company.name,
                    qty=company.current_order.qty,
                    side="sell",
                    type="limit",
                    time_in_force="day",
                    limit_price=float(company.current_order.filled_avg_price) + std
                )
        else:
            company.current_order = api.get_order(company.current_order.id)
            if company.current_order.filled_at is not None:
                print("{} was sold for {}".format(company.name, company.current_order.filled_avg_price))
                company.holding = False


def init_purchased_companies(api: tradeapi.REST, companies: [Company]):
    positions = api.list_positions()
    orders = api.list_orders()

    for pos in positions:
        for comp in companies:
            if pos.symbol == comp.name:
                print("Found existing position for {}".format(comp.name))
                comp.holding = True
                for order in orders:
                    if order.symbol == comp.name:
                        print("Also found a corresponding order for {}".format(comp.name))
                        comp.current_order = order
                        break
                if comp.current_order is None:
                    try:
                        cur_price = nasdaq_current_price(comp.name)
                        time.sleep(1)
                    except:
                        print("bad price for {}".format(comp.name))
                        break
                    comp.close = np.append(comp.close[1:], [cur_price])
                    difference = get_ema_difference(5, 100, comp)
                    std = standard_deviation(difference)
                    comp.current_order = api.submit_order(
                        symbol=comp.name,
                        qty=pos.qty,
                        side="sell",
                        type="limit",
                        time_in_force="day",
                        limit_price=round(float(pos.cost_basis) / float(pos.qty), 2) + std
                    )
                break



