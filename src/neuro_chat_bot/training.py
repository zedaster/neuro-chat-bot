# Обучение нейронной сети

import random
import json
import pickle
import numpy as np
import nltk

from keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

WORDS_FILE_PATH = 'words.pkl'
CLASSES_FILE_PATH = 'classes.pkl'
MODEL_FILE_PATH = 'chatbotmodel.keras'

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# чтение файла intense.json
intents = json.loads(open("intense.json").read())

# создание пустых списков для хранения данных
words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # отделение слов от шаблонов
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)  # и добавляем их в список слов

        # связывание шаблонов с соответствующими тегами
        documents.append(((word_list), intent['tag']))

        # добавление тегов в список классов
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

        # запоминание корневых слов или леммы
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# сохранение списка слов и классов в двоичные файлы
pickle.dump(words, open(WORDS_FILE_PATH, 'wb'))
pickle.dump(classes, open(CLASSES_FILE_PATH, 'wb'))

# нам нужны числовые значения слов, тк нейронная сеть нуждается в числовых значениях для работы
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # создание копии output_empty
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training, dtype="object")

# разделение данных
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# создание модели последовательного машинного обучения
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),
                activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),
                activation='softmax'))

# компиляция модели
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)

# сохранение модели
model.save(MODEL_FILE_PATH, hist)

# вывод строки, чтобы показать результат успешного обучения модели чат-бота
print("Yay!")
