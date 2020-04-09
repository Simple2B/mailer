from mailer import Mailer


class FormatMailer(Mailer):
    def __init__(self, name: str = 'John', email: str = 'mail1', message: str = 'HI Hi'):
        super().__init__(name, email, message)

    def send(self):
        with open('my_message.txt', 'w') as mes:
            mes.write(self.msg.as_string())
            print(self.msg.as_string())
