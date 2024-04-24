# Запуск чат-бота и получение ответа
import json
import search_answer
intents = json.loads(open("intense.json").read())


class BotLogic:
    """
    Логика для чат-бота
    """

    def __init__(self, message: str) -> None:
        """
        Инициализирует объект BotLogic.

        :param message: Текст сообщения
        :type message: str
        """
        self.message = message

    def handle_message(self) -> str:
        """
        Обрабатывает сообщение, которое пришло из чат-бота

        :return: Текст сообщения, которое будет выведено пользователю в ответ
        """
        ints = search_answer.predict_class(self.message)
        answer = search_answer.get_response(ints, intents)
        return answer


print("Chatbot is up!")

while True:
    message = input("")
    result = BotLogic(message).handle_message()
    print(result)
