import requests
import json

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