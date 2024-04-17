from abc import ABC

from ..logic.bot_logic import BotLogic


class Bot(ABC):
    """
    Абстракция чат-бота
    """

    def __init__(self, logic: BotLogic):
        """
        Создает и запускает чат-бота

        :param logic: Логика для чат-бота
        """
        self.logic = logic