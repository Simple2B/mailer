import smtplib
import json
from mailer import Mailer


class Work_mailer(Mailer):
    def __init__(self, name: str = 'John', email: str = 'mail1', message: str = 'HI Hi'):
        super().__init__(name, email, message)


def send(name, email, message):
    message_to_send = Mailer.form_message(email, name, message)
    with open('mailer_settings.json', 'r') as preferences:
        data = json.load(preferences)
        data = dict(data)

        server = smtplib.SMTP(data['server'], 587)  # Connect to the server
        server.starttls()  # Use TLS
        server.login(data['from_email'], data['passw'])  # Login to the email server
        server.sendmail('from_email', email, message_to_send)  # Send the email
        server.quit()  # Logout of the email server
