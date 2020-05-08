import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from logger import log
from settings import Settings


class Mailer(Settings):
    def __init__(self, email, name, message, f):
        super().__init__()
        log(log.DEBUG, 'Prepare e-mail')
        self.msg = MIMEMultipart()
        self.msg['From'] = self.conf['mailer']['from_email']
        log(log.DEBUG, 'From: %s', self.msg['From'])
        self.msg['To'] = ', '.join(self.conf['mailer']['to_email'])
        log(log.DEBUG, 'To: %s', self.msg['To'])
        self.msg['Cc'] = ', '.join(self.conf['mailer']['cc_mails'])
        self.msg['Bcc'] = ', '.join(self.conf['mailer']['bcc_mails'])
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.msg['Subject'] = self.conf['mailer']['subject'].format(date=date, name=name)
        log(log.DEBUG, 'Subject: %s', self.msg['Subject'])
        letter_text = (self.conf['mailer']['letter_template']).format(
            date=date, name=name, email=email, message=message, )
        self.msg.attach(MIMEText(letter_text, 'plain'))
        part = MIMEApplication(f)
        self.msg.attach(part)