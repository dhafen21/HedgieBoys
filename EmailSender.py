import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


# email_list = ["johnnigliazzo@gmail.com", "dhafen21@gmail.com"]
email_list = ["dhafen21@gmail.com"]

password = "dollabills"
sender_email = "pynance2@gmail.com"


def send_email(name: str, action: str, side: str, price: str):
    for email in email_list:
        receiver_email = email

        message = MIMEMultipart("alternative")
        message["Subject"] = "{} {}".format(name, side)
        message["From"] = sender_email
        message["To"] = receiver_email
        event_time = "{}:{}".format(time.localtime().tm_hour, time.localtime().tm_min)

        # Create the plain-text and HTML version of your message
        text = "{} {} {} at price ${} at {}".format(action, side, name, price, event_time)


        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )