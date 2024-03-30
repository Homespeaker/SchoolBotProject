import json
import telebot
import requests

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "6182241691:AAFl3lahEdNLQGp3hurvMI8JeYbAIRlHc54"
bot = telebot.TeleBot(TOKEN)
full_user_data = {}
API_KEY = '8c03ac1e-e46a-454b-aad8-9acea9fe9b97'
headers = {
    'X-Yandex-API-Key': API_KEY
}
url = 'https://api.weather.yandex.ru/v2/forecast'
objects = {
    "Огурец": {"timetoprime": "60 суток", "optimtemppochv": 20, "optimtempforplantday": 15, "vlajnostpochv": 75,
               "vlajnostvozdux": 65},
    "Помидор": {"timetoprime": "110 суток", "optimtemppochv": 16, "optimtempforplantday": 18, "vlajnostpochv": 75,
                "vlajnostvozdux": 65},
    "Капуста": {"timetoprime": "90 суток", "optimtemppochv": 15, "optimtempforplantday": 18, "vlajnostpochv": 80,
                "vlajnostvozdux": 80},
    "Перец": {"timetoprime": "125 суток", "optimtemppochv": 25, "optimtempforplantday": 25, "vlajnostpochv": 65,
              "vlajnostvozdux": 70},
    "Картофель": {"timetoprime": "70 суток", "optimtemppochv": 8, "optimtempforplantday": 19, "vlajnostpochv": 70,
                  "vlajnostvozdux": 70},
    "Морковь": {"timetoprime": "120 суток", "optimtemppochv": 8, "optimtempforplantday": 20, "vlajnostpochv": 75,
                "vlajnostvozdux": 70},
    "Репа": {"timetoprime": "80 суток", "optimtemppochv": 3, "optimtempforplantday": 17, "vlajnostpochv": 65,
             "vlajnostvozdux": 65},
    "Редька": {"timetoprime": "85 суток", "optimtemppochv": 12, "optimtempforplantday": 20, "vlajnostpochv": 70,
               "vlajnostvozdux": 70},
    "Редис": {"timetoprime": "30 суток", "optimtemppochv": 12, "optimtempforplantday": 20, "vlajnostpochv": 75,
              "vlajnostvozdux": 70},
    "Тыква": {"timetoprime": "135 суток", "optimtemppochv": 11, "optimtempforplantday": 16, "vlajnostpochv": 70,
              "vlajnostvozdux": 80},
    "Кабачок": {"timetoprime": "60 суток", "optimtemppochv": 10, "optimtempforplantday": 16, "vlajnostpochv": 70,
                "vlajnostvozdux": 70},
    "Чеснок": {"timetoprime": "95 суток", "optimtemppochv": 5, "optimtempforplantday": 10, "vlajnostpochv": 60,
               "vlajnostvozdux": 65},
    "Свекла": {"timetoprime": "110 суток", "optimtemppochv": 10, "optimtempforplantday": 20, "vlajnostpochv": 60,
               "vlajnostvozdux": 60},
    "Салат": {"timetoprime": "60 суток", "optimtemppochv": 12, "optimtempforplantday": 17, "vlajnostpochv": 70,
              "vlajnostvozdux": 60},
    "Укроп": {"timetoprime": "90 суток", "optimtemppochv": 3, "optimtempforplantday": 15, "vlajnostpochv": 80,
              "vlajnostvozdux": 70},
    "Баклажан": {"timetoprime": "130 суток", "optimtemppochv": 17, "optimtempforplantday": 22, "vlajnostpochv": 70,
                 "vlajnostvozdux": 60}
}

start = ReplyKeyboardMarkup(resize_keyboard=True)
start.add(KeyboardButton("Да"))

restart = ReplyKeyboardMarkup(resize_keyboard=True)
restart.add(KeyboardButton("/start"))
xz = ReplyKeyboardMarkup(resize_keyboard=True)
xz.add(KeyboardButton(""))

full_menu = ReplyKeyboardMarkup(resize_keyboard=True)
for i in list(objects.keys()):
    full_menu.add(KeyboardButton(i))


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     'Добрый день, Вы попали в бота который помогает сажать растения. Вы желаете начать?',
                     reply_markup=start)
    full_user_data[str(message.from_user.id)] = {}
    full_user_data[str(message.from_user.id)]['region'] = False
    full_user_data[str(message.from_user.id)]['user_longitude'] = 0.0
    full_user_data[str(message.from_user.id)]['user_latitude'] = 0.0
    full_user_data[str(message.from_user.id)]['number_question'] = "0"
    full_user_data[str(message.from_user.id)]['object'] = ""
    full_user_data[str(message.from_user.id)]['niceable'] = True


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        if full_user_data[str(message.from_user.id)]['number_question'] == "1":
            bot.send_message(message.chat.id, 'Хорошо')
            full_user_data[str(message.from_user.id)]['user_longitude'] = message.location.latitude
            full_user_data[str(message.from_user.id)]['user_latitude'] = message.location.longitude
        else:
            bot.send_message(message.chat.id, 'Вы сменили местоположение.')
            full_user_data[str(message.from_user.id)]['user_longitude'] = message.location.longitude
            full_user_data[str(message.from_user.id)]['user_latitude'] = message.location.latitude
        full_user_data[str(message.from_user.id)]['number_question'] = "2"
        bot.send_message(message.chat.id, 'Теперь выберите семена из предложенных:', reply_markup=full_menu)


@bot.message_handler(content_types=['text'])
def otvetka(message):
    try:
        def photo(link):
            with open(link, 'rb') as f:
                bot.send_photo(message.chat.id, f)  # photo('https://imgur.com/a/385WKtY')

        if full_user_data[str(message.from_user.id)]['number_question'] == "0":
            if message.text == "Да":
                bot.send_message(message.chat.id, 'Хорошо, для начала следуйте фото инструкции.', reply_markup=xz)
                bot.send_photo(message.chat.id, photo='https://imgur.com/a/385WKtY')
                bot.send_message(message.chat.id, 'Жду геолокацию места, куда ты хочешь посадить растение.',
                                 reply_markup=xz)
                full_user_data[str(message.from_user.id)]['number_question'] = "1"
            else:
                bot.send_message(message.chat.id, 'Неверный ввод, нажмите кнопку "Да" для старта.')
                print(list(objects.keys()))
        elif str(message.text) in list(objects.keys()):
            full_user_data[str(message.from_user.id)]['object'] = message.text
            params = {
                'lat': full_user_data[str(message.from_user.id)]['user_latitude'],
                'lon': full_user_data[str(message.from_user.id)]['user_longitude'],
                'lang': 'ru_RU',
                'limit': 7  # прогноз на 3 дня вперед
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                # print(data["fact"]["temp"])
                for day in data['forecasts']:
                    date = day['date']
                    temperature = day['parts']['day']['temp_min']
                    print(temperature)
                    temppo4v = day['parts']['day']['soil_temp']
                    print(temppo4v)
                    vlajnostvozdux = day['parts']['day']['humidity']
                    print(vlajnostvozdux)
                    if int(temperature) < objects[message.text]['optimtempforplantday'] or int(temppo4v) < \
                            objects[message.text]['optimtemppochv'] or int(vlajnostvozdux) < objects[message.text][
                        'vlajnostvozdux']:
                        bot.send_message(message.chat.id,
                                         f'Семена посадить не получится, {date} погодные условия не будут соответствовать рекомендуемым значениям для данного растения.',
                                         reply_markup=restart)
                        # full_user_data[str(message.from_user.id)]['niceable'] = False
                        if int(temperature) < objects[message.text]['optimtempforplantday']:
                            bot.send_message(message.chat.id,
                                             f"Ваша температура не подходит:\n Вашатемпература: {int(temperature)}. Нужная температура: {objects[message.text]['optimtempforplantday']}")
                        if int(temppo4v) < objects[message.text]['optimtemppochv']:
                            bot.send_message(message.chat.id,
                                             f"Ваша температура почвы не подходит:\nВаша температура: {int(temppo4v)}. Нужная температура: {objects[message.text]['optimtemppochv']}")
                        if int(vlajnostvozdux) < objects[message.text]['vlajnostvozdux']:
                            bot.send_message(message.chat.id,
                                             f"Ваша влажность воздуха не подходит:\nВаша влажность: {int(vlajnostvozdux)}. Нужная влажность: {objects[message.text]['vlajnostvozdux']}")

                        break
                    elif full_user_data[str(message.from_user.id)]['niceable']:
                        bot.send_message(message.chat.id,
                                         f'Требования по посадке данных семян соответствуют погодным условиям на неделю вперед. Сейчас будут выведены рекомендации для посадки.')
                        bot.send_message(message.chat.id,
                                         f"Рекомендуемая влажность воздуха: {objects[full_user_data[str(message.from_user.id)]['object']]['vlajnostvozdux']}%\nРекомендуемая температура почвы: {objects[full_user_data[str(message.from_user.id)]['object']]['optimtemppochv']}°\nРекомендуемая температура днём: {objects[full_user_data[str(message.from_user.id)]['object']]['optimtempforplantday']}°\nОжидание до полной готовности: {objects[full_user_data[str(message.from_user.id)]['object']]['timetoprime']}",
                                         reply_markup=restart)
            else:
                print(f'Ошибка: {response.status_code}')


    except:
        bot.send_message(message.chat.id, f'Неверный ввод, нажмите /start для перезапуска.')


bot.polling()
