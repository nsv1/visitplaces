import telebot
import csv

TOKEN = "619948069:AAEUrKhGPu0SGcP4g0HLzgHpgQ9A6ZOBH-Q"
tb = telebot.TeleBot(TOKEN)

@tb.message_handler(content_types=['location'])
def handle_location(message):
    print(message.location)
    photo = open('error.jpg', 'rb')
    tb.send_photo(message.chat.id, photo, 
                  caption=
'''Шота паламалася. 
Вероятно будет реализовано другими участниками забега.''')

def check_location(message):
    text = message.text.lower()
    if "улица" in text or "ул." in text:
        return True
    return False

def add_location(message):
    chat_id = message.chat.id
    location = message.text
    with open('location.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([chat_id, location])
        
def list_lacation(message):
    with open('location.csv', newline='', encoding='utf-8') as f:
        data = csv.reader(f, delimiter=';')
        res = []
        for row in data:
            if row[0] == str(message.chat.id):
                res.append(row[1])
    if len(res) > 10:
        res = res[-10:]
    if len(res) == 0:
        res = [
'''Удивительно, но у вас нет сохраненных мест.
Жмакайте скорее на /add или
вводите адрес объекта'''
]
    return '\n'.join(res)

def reset_location(message):
    with open('location.csv', newline='', encoding='utf-8') as f:
        data = csv.reader(f, delimiter=';')
        res = ''
        for row in data:
            if row[0] != str(message.chat.id):
                res.append(row)
    with open('location.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for i in res:
            writer.writerow(i)

@tb.message_handler(func=check_location)
def handle_savelocation(message):
    print(message.text)
    add_location(message)
    tb.send_message(chat_id=message.chat.id, 
        text='Адрес сохранен.')

@tb.message_handler(commands=['start'])
def handle_start(message):
    print(message.text)
    tb.send_message(chat_id=message.chat.id, 
        text=
'''Бот предназначен для сохранения посещаемых мест.
Доступные команды:
    /add - добавление объекта
    /list - просмотр последних 10-ти объектов (или менее)
    /reset - удаление всех сохраненных объектов''')

@tb.message_handler(commands=['add'])
def handle_add(message):
    print(message.text)
    tb.send_message(chat_id=message.chat.id, 
        text=
'''Введите адрес объекта.
Адрес должен содержать слово "улица" или "ул."''')

@tb.message_handler(commands=['list'])
def handle_list(message):
    print(message.text)
    text='Список последних посещений:\n' + list_lacation(message)
    tb.send_message(message.chat.id, text)
    

@tb.message_handler(commands=['reset'])
def handle_reset(message):
    print(message.text)
    reset_location(message)
    tb.send_message(chat_id=message.chat.id, 
        text='Список мест очищен')

@tb.message_handler()
def handle_message(message):
    print("default")
    tb.send_message(chat_id=message.chat.id, 
        text=
'''Адрес должен содержать содержать слово "улица" или "ул."
или
для ввода адреса воспользуйтесь командой /add.''')

tb.polling()