from Company import *
from EmailSender import send_email


def update_call_pos(companies: [Company]):
    for company in companies:
        if not company.call_pos:
            if company.macd[-1] > 0 and company.signal[-1] > 0:
                if company.macd[-1] >= company.signal[-1] and company.macd[-2] < company.signal[-2]:
                    company.call_pos = True
                    try:
                        send_email(company.name, "bought", "call", str(company.close[-1]))
                    except:
                        print('Sending email failed')
                    print("buing {} call position".format(company.name))
        else:
            if company.close[-1] < company.sma[-1]:
                company.call_pos = False
                try:
                    send_email(company.name, "sold", "call", str(company.close[-1]))
                except:
                    print("Sending email failed")
                print("selling {} call position".format(company.name))


def update_put_pos(companies: [Company]):
    for company in companies:
        if not company.put_pos:
            if company.macd[-1] < 0 and company.signal[-1] < 0:
                if company.macd[-1] <= company.signal[-1] and company.macd[-2] > company.signal[-2]:
                    company.put_pos = True
                    try:
                        send_email(company.name, "bought", "put", str(company.close[-1]))
                    except:
                        print("Sending email failed")
                    print("buing {} put position".format(company.name))
        else:
            if company.close[-1] > company.sma[-1]:
                company.put_pos = False
                try:
                    send_email(company.name, "sold", "put", str(company.close[-1]))
                except:
                    print("Sending email failed")
                print("selling {} put position".format(company.name))

