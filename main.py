import os
import random

import telebot
import uuid
import speech_recognition as sr

from telebot import types, TeleBot

token = '#'
bot = TeleBot(token)
r = sr.Recognizer()

days = ("""
8:30-9:15         География 0209 
9:30-10:15       Русский язык 0209
10:35-11:20     Биология 0218   
11:30-12:15     Химия 0319 
12:30-13:15     Технология 0211/0328
14:05-14:50     Обществознание 0209 
14:55-16:30     ТВиМС 0209 """, "8:30-9:15       Литература 0209 \n9:30-10:15     Русский язык 0209 \n10:35-11:20   "
                             "Информатика 0327 \n11:35-13:15   Алгебра 0209 \n14:05-14:50   ОБЖ 0209 \n14:55-16:30   "
                             "Геометрия 0209", "8:30-9:15       Родная литература 0209 \n9:35-10:20     Англ. язык 0209/0225 "
                             "\n11:45-13:20   Алгебра 0209 \n13:25-14:10   Геометрия 0209 \n14:45-15:30   Химия 0319 "
                             "\n15:35-17:10   ОП 0212/0328", "8:30-10:20     Физика 0225 \n10:40-11:25   История 0209 \n11:45-13:20   ОлМат 0209 "
                             "\n13:35-14:10   Физическая культура \n14:45-15:30   Биология 0218 \n15:35-17:10   "
                             "Русский язык 0209", "8:30-9:15       История 0209 \n9:35-10:20     Французский язык 0209 \n10:40-11:25   "
                             "Англ. язык 0209/0225 \n11:45-12:30   Физика 0225 \n12:35-13:20   Постановка физ. "
                             "эксперимента 0225 \n13:25-14:10   Физра (бассейн) \n15:35-17:05   Консультация по "
                             "физике"
)

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language='ru_RU')
            return text
        except:
            return "Try again."

@bot.message_handler(commands=['start'])
def hello(message):
    text = f"<b>Приветствую, {message.from_user.first_name}</b>! 👋🏻\nЧтобы получить список команд, напиши /help. Они есть и в блоке <i>меню</i>. Кроме того, я принимаю <b>голосовые команды,</b> попробуйте попросить меня о чем-то."
    bot.send_message(message.from_user.id, text, parse_mode="html")

@bot.message_handler(commands=['news'])
def news(message):
    import requests
    from bs4 import BeautifulSoup as BS
    try:
        soup = BS(requests.get('https://sochisirius.ru/').text, 'html.parser')
        news = soup.find('div', class_='news-summary__items-list slides-pagination')
        url = news.find_all('a', class_='news-summary__item', href=True)
        for j in url:
            text = j.text.replace('\n', '').replace(' ' * 78, '')
            mes = text + '\n' + 'https://sochisirius.ru' + str(j.get('href'))
            bot.send_message(message.from_user.id, mes)
    except:
        bot.send_message(message.from_user.id, 'Не удалось найти новости')

@bot.message_handler(commands=['help'])
def help(message):
    text = "Вот мой список команд:\n /schedule - расписание \n /news - новости с сайта Сириус \n /site - сайт \n /random - случайное число"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Перейти на сайт', url='https://github.com/dmitq'))
    bot.send_message(message.from_user.id, "Нажмите на кнопку ниже", reply_markup=markup)

@bot.message_handler(commands=['contacts'])
def contacts(message):
    bot.send_message(message.from_user.id, "Телефон: +7(777)777-77-77")

@bot.message_handler(commands=['schedule'])
def schedule(message):
    keyboard = types.InlineKeyboardMarkup()
    key_monday = types.InlineKeyboardButton(text='Понедельник', callback_data='monday')
    keyboard.add(key_monday)
    key_tue = types.InlineKeyboardButton(text='Вторник', callback_data='tuesday')
    keyboard.add(key_tue)
    key_wed = types.InlineKeyboardButton(text='Среда', callback_data='wednesday')
    keyboard.add(key_wed)
    key_thur = types.InlineKeyboardButton(text='Четверг', callback_data='thursday')
    keyboard.add(key_thur)
    key_fri = types.InlineKeyboardButton(text='Пятница', callback_data='friday')
    keyboard.add(key_fri)
    bot.send_message(message.from_user.id, 'Выбери день недели и нажми на кнопку!', reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "monday":
            bot.send_message(call.message.chat.id, days[0])
        elif call.data == "tuesday":
            bot.send_message(call.message.chat.id, days[1])
        elif call.data == "wednesday":
            bot.send_message(call.message.chat.id, days[2])
        elif call.data == "thursday":
            bot.send_message(call.message.chat.id, days[3])
        elif call.data == "friday":
            bot.send_message(call.message.chat.id, days[4])

@bot.message_handler(commands=['random'])
def randomazer(message):
    msg = bot.send_message(message.from_user.id, 'Введите два числа <b>через тире,\n</b>вот так: <i>x-y</i>',
                           parse_mode="html")
    bot.register_next_step_handler(msg, randomazer_step_2)
def randomazer_step_2(message):
    if '-' in message.text:
        tire = message.text.find('-')
        f_num = int(message.text[:tire])
        l_num = int(message.text[tire + 1:])
        bot.send_message(message.chat.id, "Случайное число от " + str(f_num) + " до " + str(l_num) + ": " + str(
            random.randint(f_num, l_num)))

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = filename + ".ogg"
    file_name_full_converted = filename + ".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i " + file_name_full + "  " + file_name_full_converted)
    text = recognise(file_name_full_converted)
    bot.send_message(message.chat.id, "Распознано:\n" + text)
    if "новости" in text or "новое" in text:
        bot.send_message(message.chat.id, "Собираю новости... ")
        news(message)
    elif 'понедельник' in text:
        bot.send_message(message.chat.id, days[0])
    elif 'вторник' in text:
        bot.send_message(message.chat.id, days[1])
    elif 'среда' in text or 'среду' in text:
        bot.send_message(message.chat.id, days[2])
    elif 'четверг' in text:
        bot.send_message(message.chat.id, days[3])
    elif 'пятница' in text or "пятницу" in text:
        bot.send_message(message.chat.id, days[4])
    elif "расписание" in text:
        schedule(message)
    elif 'сайт' in text:
        site(message)
    elif 'число' in text and "от" in text and "до" in text:
        ot = text.find('от')
        do = text.find('до')
        f_num = text[ot + 3:do - 1]
        l_num = text[do + 3:]
        if f_num.isdigit() and l_num.isdigit():
            f_num = int(f_num)
            l_num = int(l_num)
            bot.send_message(message.chat.id, str(random.randint(f_num, l_num)))
        else:
            bot.send_message(message.chat.id, "Пожалуйста, повторите.")
    elif 'число' in text:
        bot.send_message(message.chat.id, str(random.randint(1, 100)))
    elif 'контакты' in text:
        contacts(message)
    else:
        bot.send_message(message.chat.id, "Команда не найдена")

    os.remove(file_name_full)
    os.remove(file_name_full_converted)


bot.polling(none_stop=True, interval=0)
