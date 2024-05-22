

def main():
    bot_logic = BotLogic()
    telegram_bot = TelegramBot(bot_logic)
    telegram_bot.start()


if __name__ == "__main__":
    main()