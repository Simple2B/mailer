from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import datetime


class Mailer(object):
    def __init__(self, email, name, message):
        self.email = email
        self.name = name
        self.message = message

    def form_message(email, name, message):
        # open json file and read params
        with open('mailer_settings.json', 'r') as preferences:
            data = json.load(preferences)
            data = dict(data)
            data['user_message']
        msg = MIMEMultipart()
        msg['From'] = data['from_email']
        msg['To'] = data['to_email']
        msg['Subject'] = data['subject'] + ' ' + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        form_message = data['user_message'].format(name=name, email=email, message=message)
        msg.attach(MIMEText(form_message, 'plain'))
        return msg.as_string()

    def send():
        raise NotImplementedError
