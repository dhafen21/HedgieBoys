import robin_stocks.robinhood.options as r
import robin_stocks as rh

def historical_butterflies(symbol: str, spread: int = 1):
    dates = r.get_chains(symbol)["expiration_dates"]
    target_date = dates[1]
    prices = rh.robinhood.stocks.get_stock_historicals(symbol, "day", "month")
    for price_candle in prices:
        price = int(float(price_candle["open_price"]))
        date = price_candle["begins_at"]
        options_lower = r.get_option_historicals(symbol, target_date, str(price - spread), "call", "day", "year")
        options_middle = r.get_option_historicals(symbol, target_date, str(price), "call", "day", "year")
        options_upper = r.get_option_historicals(symbol, target_date, str(price + spread), "call", "day", "year")
        if (options_upper == None or options_middle == None or options_lower == None):
            continue
        lower = [lower for lower in options_lower if lower["begins_at"] == date][0]
        middle = [middle for middle in options_middle if middle["begins_at"] == date][0]
        high = [high for high in options_upper if high["begins_at"] == date][0]

        l = float(lower["open_price"])
        m = float(middle["open_price"])
        h = float(high["open_price"])

        debt = (2 * m) - (h + l)
        profit = 1 + debt
        print("Profit Potential on {} is {}".format(date, profit))






