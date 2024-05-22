import nltk
import csv

from nltk import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

ignore_letters = ["?", "!", "."]
with open("intents.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=",")

    data_set = dict()
    count = 0
    # Считывание данных из CSV файла
    for row in file_reader:
        if count == 0:
            print(f'Файл содержит столбцы: {", ".join(row)}')
        else:
            question = row[0].replace(',', '').lower()
            # отделение слов от шаблонов
            question = nltk.word_tokenize(question)
            # преобразование слова в его начальную форму
            question = [lemmatizer.lemmatize(word) for word in question if word not in ignore_letters]

            answer = row[1].replace(',', '').lower()
            answer = nltk.word_tokenize(answer)
            answer = [lemmatizer.lemmatize(word) for word in answer if word not in ignore_letters]

            if len(answer) <= 1 or len(question) <= 1:
                continue

            data_set[". ".join(question)] = ". ".join(answer)

        print('1')
        count += 1

with open("form2.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(["Question", "Answer"])
    for question, answer in data_set.items():
        file_writer.writerow([question, answer])