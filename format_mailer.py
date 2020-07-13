from mailer import Mailer
from logger import log


OUT_FILE = 'my_message.txt'


class FormatMailer(Mailer):
    def __init__(self, name: str = 'John', email: str = 'mail1', message: str = 'HI Hi'):
        super().__init__(name, email, message, attachment=None)

    def send(self):
        with open(OUT_FILE, 'w') as mes:
            mes.write(self.msg.as_string())
            log(log.INFO, 'e-mail text in %s', OUT_FILE)
