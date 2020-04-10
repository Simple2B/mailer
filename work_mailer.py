import smtplib
from mailer import Mailer


class WorkMailer(Mailer):
    def __init__(self, name: str, email: str, message: str):
        super().__init__(name, email, message)

    def send(self):
        with smtplib.SMTP(self.conf['SMTP']['server'], self.conf['SMTP']['port']) as server:  # Connect to the server
            server.starttls()  # Use TLS
            server.login(self.conf['from_email'], self.conf['passw'])  # Login to the email server
            server.sendmail(from_addr=self.conf['from_email'],
                            to_addrs=self.conf['to_email'],
                            msg=self.msg.as_string())
            server.quit()  # Logout of the email server
