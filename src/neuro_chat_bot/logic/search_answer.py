# Поиск ответа на полученный вопрос

# необходимые модули
import random
import pickle
import numpy as np
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

# загрузка файлов, которые мы создали ранее
lemmatizer = WordNetLemmatizer()
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')


# Эта функция будет отделять слова от предложений, которые мы будем вводить в качестве входных данных
def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


# Эта функция добавит 1 к переменной списка ‘bag’, если слово содержится в наших входных данных
# и также присутствует в списке слов, созданных ранее
def bagw(sentence):
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


# Эта функция будет предсказывать класс предложения, введенного пользователем
def predict_class(sentence):
    bow = bagw(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        return return_list


# Эта функция выведет случайный ответ из любого класса, к которому относится предложение/слова, введенные пользователем
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            # выводит случайный ответ
            result = random.choice(i['responses'])
            break
    return result
