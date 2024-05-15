import json
import src.neuro_chat_bot.logic.search_answer as search_answer

INTENSE_FILE_PATH = "intense.json"


class BotLogic:
    """
    Логика для чат-бота
    """

    def __init__(self) -> None:
        """
        Инициализирует логику для чат-бота.
        """
        with open(INTENSE_FILE_PATH) as intense_file:
            self.intents = json.loads(intense_file.read())

    def handle_message(self, message) -> str:
        """
        Отвечает на сообщение, которое пришло из чат-бота

        :param message: Текст сообщения
        :type message: str

        :return: Текст сообщения, которое будет выведено пользователю в ответ
        """
        ints = search_answer.predict_class(message)
        answer = search_answer.get_response(ints, self.intents)
        return answer
