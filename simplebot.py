import telebot


class SimpleBot(object):
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)

    def send_to_channel(self, message: str):
        self.bot.send_message(-469664009, message)