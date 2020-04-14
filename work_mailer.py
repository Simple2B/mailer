import smtplib
from mailer import Mailer
from logger import log


class WorkMailer(Mailer):
    def __init__(self, name: str, email: str, message: str):
        super().__init__(name, email, message)

    def send(self):
        try:
            log(log.INFO, 'SMTP connect to %s:%d',
                self.conf['mailer']['SMTP']['server'], self.conf['mailer']['SMTP']['port'])
            # Connect to the server
            with smtplib.SMTP(self.conf['mailer']['SMTP']['server'], self.conf['mailer']['SMTP']['port']) as server:
                server.starttls()  # Use TLS
                # Login to the email server
                server.login(self.conf['mailer']['from_email'], self.conf['mailer']['passw'])
                log(log.INFO, 'send email')
                log(log.DEBUG, 'from: %s', self.conf['mailer']['from_email'])
                log(log.DEBUG, 'to: %s', self.conf['mailer']['to_email'])
                recipients = self.conf['mailer']['to_email'] + self.conf['mailer']['cc_mails']
                server.sendmail(from_addr=self.conf['mailer']['from_email'],
                                to_addrs=recipients,
                                msg=self.msg.as_string())
                log(log.DEBUG, 'e-mail sent.')
                server.quit()  # Logout of the email server
        except smtplib.SMTPException as e:
            log(log.ERROR, 'SMTP Error: %s', e)
