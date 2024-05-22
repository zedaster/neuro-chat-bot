import json
import src.neuro_chat_bot.logic.search_answer as search_answer
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill

INTENSE_FILE_PATH = "final_intense_form.json"


class BotLogic:
    """
    Логика для чат-бота
    """

    def __init__(self) -> None:
        """
        Инициализирует логику для чат-бота.
        """
        self.faq = SimilarityMatchingSkill(data_path='src/education-dataset.csv',
                                           x_col_name='Question',
                                           y_col_name='Answer',
                                           save_load_path='./model',
                                           config_type='tfidf_autofaq',
                                           edit_dict={},
                                           train=True)

    def handle_message(self, message) -> str:
        return self.faq([message], [], [])[0]
