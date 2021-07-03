from Company import *
from EmailSender import send_email


def update_call_pos(companies: [Company]):
    for company in companies:
        if company.call_pos:
            if company.macd[-1] > 0 and company.signal[-1] > 0:
                if company.macd[-1] >= company.signal[-1] and company.macd[-2] < company.signal[-2]:
                    company.call_pos = True
                    send_email(company.ticker, "bought", "call", str(company.close[-1]))
        else:
            if company.close[-1] < company.sma[-1]:
                company.call_pos = False
                send_email(company.ticker, "sold", "call", str(company.close[-1]))


def update_put_pos(companies: [Company]):
    for company in companies:
        if company.put_pos:
            if company.macd[-1] > 0 and company.signal[-1] > 0:
                if company.macd[-1] >= company.signal[-1] and company.macd[-2] < company.signal[-2]:
                    company.put_pos = True
                    send_email(company.ticker, "bought", "put", str(company.close[-1]))
        else:
            if company.close[-1] < company.sma[-1]:
                company.put_pos = False
                send_email(company.ticker, "sold", "put", str(company.close[-1]))
