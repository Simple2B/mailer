from mailer import Mailer


class Format_mailer(Mailer):
    def __init__(self, name: str = 'John', email: str = 'mail1', message: str = 'HI Hi'):
        super().__init__(name, email, message)


def send(email, name, message):
    with open('my_message.txt', 'w') as mes:
        mes.write(str(Mailer.form_message(email, name, message)))
        print(Mailer.form_message(email, name, message))
    return 'OK'
