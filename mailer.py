import json
import datetime
import pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from invalid_usage import InvalidUsage

PATH_TO_CONF_FILE = pathlib.Path(__file__).parent.absolute().joinpath('config.json')


class Mailer(object):
    def __init__(self, email, name, message):
        # Read preferences
        self.conf = None
        with open(PATH_TO_CONF_FILE, 'r') as f:
            self.conf = json.load(f)
        if not self.conf:
            raise InvalidUsage('Bad settings file')
        self.msg = MIMEMultipart()
        self.msg['From'] = self.conf['from_email']
        self.msg['To'] = self.conf['to_email']
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.msg['Subject'] = self.conf['subject'].format(date=date, name=name)
        letter_text = self.conf['letter_template'].format(
            date=date, name=name, email=email, message=message)
        self.msg.attach(MIMEText(letter_text, 'plain'))
