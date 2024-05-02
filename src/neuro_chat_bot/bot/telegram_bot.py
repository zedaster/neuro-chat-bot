from ..bot.bot import Bot
from ..logic.bot_logic import BotLogic
from telegram.ext import Updater, MessageHandler, Filters

TOKEN_FILE_PATH = 'telegram_token.txt'


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

    def start(self):
        """
        Запускает бота для Телеграм
        """
        updater = Updater(token=self.token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text, self.respond))
        updater.start_polling()
        updater.idle()

    def respond(self, update, context):
        """
        Отвечает на сообщение пользователя

        :param update: Обновление из Телеграма
        :param context: Контекст выполнения
        """
        question = update.message.text
        answer = self.logic.handle_message(question)
        update.message.reply_text(answer)
