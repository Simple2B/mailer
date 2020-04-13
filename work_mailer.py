import smtplib
from mailer import Mailer
from logger import log
from simplebot import SimpleBot


class WorkMailer(Mailer):
    def __init__(self, name: str, email: str, message: str):
        super().__init__(name, email, message)

    def send(self):
        log(log.INFO, 'SMTP connect to %s:%d', self.conf['mailer']['SMTP']['server'], self.conf['mailer']['SMTP']['port'])
        with smtplib.SMTP(self.conf['mailer']['SMTP']['server'], self.conf['mailer']['SMTP']['port']) as server:  # Connect to the server
            server.starttls()  # Use TLS
            server.login(self.conf['mailer']['from_email'], self.conf['mailer']['passw'])  # Login to the email server
            log(log.INFO, 'send email')
            log(log.DEBUG, 'from: %s', self.conf['mailer']['from_email'])
            log(log.DEBUG, 'to: %s', self.conf['mailer']['to_email'])
            recipients = self.conf['mailer']['to_email'] + self.conf['mailer']['cc_mails']
            server.sendmail(from_addr=self.conf['mailer']['from_email'],
                            to_addrs=recipients,
                            msg=self.msg.as_string())
            log(log.DEBUG, 'e-mail sent.')
            server.quit()  # Logout of the email server
        bot = SimpleBot(self.conf['telegram']['token'])
        tele_mess = self.conf['telegram']['message_template'].format(name=self.conf['mailer']['name'])
        bot.send_to_channel(tele_mess)
