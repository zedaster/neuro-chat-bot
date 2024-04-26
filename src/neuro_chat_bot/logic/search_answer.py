# Поиск ответа на полученный вопрос

import random
import pickle
import numpy as np
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

WORDS_FILE_PATH = 'words.pkl'
CLASSES_FILE_PATH = 'classes.pkl'
MODEL_FILE_PATH = 'chatbotmodel.keras'


def load_pickle_from_file(file_path):
    """
    Открывает и загружает pickle файл
    :param file_path: Путь к файлу
    :return:
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)


# загрузка файлов, которые мы создали ранее
lemmatizer = WordNetLemmatizer()
words = load_pickle_from_file(WORDS_FILE_PATH)
classes = load_pickle_from_file(CLASSES_FILE_PATH)
model = load_model(MODEL_FILE_PATH)


def clean_up_sentences(sentence):
    """
    Отделяет слова от предложений, которые мы будем вводить в качестве входных данных

    :param sentence:
    :return:
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bagw(sentence):
    """
    Добавляет 1 к переменной списка ‘bag’, если слово содержится в наших входных данных
    и также присутствует в списке слов, созданных ранее

    :param sentence: Предложение
    :return:
    """
    # выделите слова из входного предложения
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            # проверьте, присутствует ли слово также во входных данных
            if word == w:
                bag[i] = 1
    # возвращает числовой массив
    return np.array(bag)


def predict_class(sentence):
    """
    Эта функция будет предсказывать класс предложения, введенного пользователем

    :param sentence: Предложение
    :return:
    """
    bow = bagw(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        return return_list


def get_response(intents_list, intents_json):
    """
    Эта функция выведет случайный ответ из любого класса, к которому относится предложение/слова, введенные пользователем

    :param intents_list:
    :param intents_json:
    :return:
    """
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            # выводит случайный ответ
            result = random.choice(i['responses'])
            break
    return result
