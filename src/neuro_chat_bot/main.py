"""
Главный модуль
"""

from bot.telegram_bot import TelegramBot
from logic.bot_logic import BotLogic


def main():
    bot_logic = BotLogic()
    TelegramBot(bot_logic)


if __name__ == "__main__":
    main()
