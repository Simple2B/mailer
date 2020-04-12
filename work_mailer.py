import smtplib
from mailer import Mailer
from logger import log


class WorkMailer(Mailer):
    def __init__(self, name: str, email: str, message: str):
        super().__init__(name, email, message)

    def send(self):
        log(log.INFO, 'SMTP connect to %s:%d', self.conf['SMTP']['server'], self.conf['SMTP']['port'])
        with smtplib.SMTP(self.conf['SMTP']['server'], self.conf['SMTP']['port']) as server:  # Connect to the server
            server.starttls()  # Use TLS
            server.login(self.conf['from_email'], self.conf['passw'])  # Login to the email server
            log(log.INFO, 'send email')
            log(log.DEBUG, 'from: %s', self.conf['from_email'])
            log(log.DEBUG, 'to: %s', self.conf['from_email'])
            recipients = self.conf['to_email'] + self.conf['cc_mails']
            server.sendmail(from_addr=self.conf['to_email'],
                            to_addrs=recipients,
                            msg=self.msg.as_string())
            log(log.DEBUG, 'e-mail sent.')
            server.quit()  # Logout of the email server
