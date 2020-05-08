import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import log
from settings import Settings
from email.mime.base import MIMEBase
from email import encoders


class Mailer(Settings):
    def __init__(self, email, name, message, attachment):
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
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        attach_name = str(attachment.filename)
        part.add_header("Content-Disposition", "attachment", filename=attach_name)
        self.msg.attach(part)
