import smtplib
from mailer import Mailer


class WorkMailer(Mailer):
    def __init__(self, name: str, email: str, message: str):
        super().__init__(name, email, message)

    def send(self):
        with smtplib.SMTP(self.settings['server'], 587) as server:  # Connect to the server
            server.starttls()  # Use TLS
            server.login(self.settings['from_email'], self.settings['passw'])  # Login to the email server
            server.sendmail('from_email', self.settings['from_email'], self.msg.as_string())  # Send the email
            server.quit()  # Logout of the email server
