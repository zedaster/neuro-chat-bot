"""
Главный модуль
"""

from bot.telegram_bot import TelegramBot
from logic.bot_logic import BotLogic


def main():
    bot_logic = BotLogic()
    telegram_bot = TelegramBot(bot_logic)
    telegram_bot.start()


if __name__ == "__main__":
    main()
