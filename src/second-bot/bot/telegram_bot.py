import telebot
from src.neuro_chat_bot.logic.bot_logic import BotLogic
from src.neuro_chat_bot.bot.bot import Bot

TOKEN_FILE_PATH = '../../config/telegram_token.txt'


def load_token(filename):
    """
    Загрузка токена из файла
    """
    with open(filename, 'r') as file:
        return file.read().strip()


class TelegramBot(Bot):
    """
    Чат-бот для Телеграм
    """

    def __init__(self, logic: BotLogic):
        """
        Создает и запускает чат-бота для Телеграм

        :param logic: Логика для чат-бота
        """
        super().__init__(logic)
        self.token = load_token(TOKEN_FILE_PATH)
        self.bot = telebot.TeleBot(self.token)

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            question = message.text
            answer = self.logic.handle_message(question)
            self.bot.reply_to(message, answer)

    def start(self):
        """
        Запускает бота для Телеграм
        """
        print('[Telegram] Bot is pooling now...')
        self.bot.polling()
