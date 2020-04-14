import telebot
from settings import Settings
from logger import log


class SimpleBot(Settings):
    def __init__(self):
        super().__init__()
        self.bot = telebot.TeleBot(self.conf['telegram']['token'])

    def send(self, **args):
        message_template = self.conf['telegram']['message_template']
        message = message_template.format(**args)
        try:
            self.bot.send_message(self.conf['telegram']['chat_id'], message)
        except telebot.apihelper.ApiException as e:
            log(log.ERROR, 'Telegram send failed: %s', e)
            return False
        return True
