"""
Главный модуль
"""

from src.neuro_chat_bot.bot.telegram_bot import TelegramBot
from src.neuro_chat_bot.logic.bot_logic import BotLogic


def main():
    bot_logic = BotLogic()
    telegram_bot = TelegramBot(bot_logic)
    telegram_bot.start()


if __name__ == "__main__":
    main()
