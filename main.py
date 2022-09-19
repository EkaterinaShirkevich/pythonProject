from flask import Flask, request, render_template
from datetime import datetime               # flask - название пакета Flask - класс "веб-приложение"
import json

app = Flask(__name__)                       # создаем новое приложение


def load_chat():                           # загружаем данные из файла
    with open("chat.json", "r") as json_file:
        data = json.load(json_file)        # загрузить файл в переменную data
        return data["messages"]


all_messages = load_chat()


def save_chat():
    data = {"messages": all_messages}      # готовим данные
    with open("chat.json", "w") as json_file:  # открываем файл для записи
        json.dump(data, json_file)         # сохраняем данные в файл


@app.route("/chat")
def display_chat():
    return render_template("form.html")


@app.route("/")                             # связываем страницу с функцией
def index_page():                           # добавляем приветствие на странице
    return "Welcome to Messenger"


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@app.route("/send_message")                # http://127.0.0.1.5000/send_message?name=Mike&text=Hello
def send_message():
    sender = request.args["name"]
    if not 3 <= len(sender) >100:
        print ("{} Error! Длина имени пользователя короче 3 символов или длиннее 100 символов!", format(datetime.now()))
        return "Name length error"
    text = request.args["text"]
    if len(text) >3000:
        print("{} Error! Длина текста превышает 3000 символов!", format(datetime.now()))
        return "Text length error"
    add_message(sender, text)
    save_chat()
    return "Ok"


def add_message(sender, text):              # ф-ция добавления сообщения
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    }
    all_messages.append(new_message)


app.run(host="0.0.0.0", port=80)                                   # запуск приложения
