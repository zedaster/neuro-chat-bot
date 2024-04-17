from ..bot.bot import Bot
from ..logic.bot_logic import BotLogic


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