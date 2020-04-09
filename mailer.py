import json
import datetime
import pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from invalid_usage import InvalidUsage

PATH_TO_SETTINGS_FILE = pathlib.Path(__file__).parent.absolute().joinpath('settings.json')


class Mailer(object):
    def __init__(self, email, name, message):
        self.email = email
        self.name = name
        self.message = message
        # Read preferences
        self.settings = None
        with open(PATH_TO_SETTINGS_FILE, 'r') as f:
            self.settings = json.load(f)
        if not self.settings:
            raise InvalidUsage('Bad settings file')
        self.msg = MIMEMultipart()
        self.msg['From'] = self.settings['from_email']
        self.msg['To'] = self.settings['to_email']
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.msg['Subject'] = self.settings['subject'].format(date=date, name=name)
        letter_text = self.settings['letter_template'].format(
            date=date, name=name, email=email, message=message)
        self.msg.attach(MIMEText(letter_text, 'plain'))
