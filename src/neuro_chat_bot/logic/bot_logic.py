import json
import search_answer

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


# Для тестирования логики бота. Перед этим необходимо запустить создание модели (training.py)
if __name__ == "__main__":
    logic = BotLogic()
    print("Chatbot is up!")

    while True:
        message = input("")
        result = logic.handle_message(message)
        print(result)
