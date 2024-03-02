import telebot
from telebot import types
import requests
import random
import json
from gtts import gTTS
from io import BytesIO
from googletrans import Translator
TOKEN = '5315502911:AAEAh8TGtWnVmFAmPkobvnAYWWdzgSW7F_k'
banned_users = []


bot = telebot.TeleBot(TOKEN)
translator = Translator()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, созданный с помощью Telebot. Как я могу вам помочь?")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем объект фотографии
    photo = message.photo[-1]
    file_id = photo.file_id

    # Получаем информацию о файле
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Скачиваем файл на компьютер
    downloaded_file = bot.download_file(file_path)
    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "Фото сохранено")

@bot.message_handler(commands=['joke'])
def send_joke(message):
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = response.json()
        setup = data['setup']
        punchline = data['punchline']
        joke = f"{setup}\n{punchline}"
        bot.send_message(message.chat.id, joke)
        translated = translator.translate(f"{setup}\n{punchline}", src='en', dest='ru')
        bot.send_message(message.chat.id, f"Перевод на русский: {translated.text}")
    except Exception as e:
        bot.send_message(message.chat.id, "К сожалению, не удалось выполнить перевод. Попробуйте еще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, "К сожалению, не удалось получить шутку. Попробуйте позже.")

@bot.message_handler(commands=['quote'])
def send_quote(message):
    try:
        response = requests.get("https://favqs.com/api/qotd")
        data = response.json()
        quote = data['quote']['body']
        author = data['quote']['author']
        full_quote = f"\"{quote}\"\n- {author}"
        bot.send_message(message.chat.id, full_quote)
        translated = translator.translate(f"\"{quote}\"\n- {author}", src='en', dest='ru')
        bot.send_message(message.chat.id, f"Перевод на русский: {translated.text}")
    except Exception as e:
        bot.send_message(message.chat.id, "К сожалению, не удалось выполнить перевод. Попробуйте еще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, "К сожалению, не удалось получить цитату. Попробуйте позже.")

@bot.message_handler(commands=['fact'])
def send_fact(message):
    facts = ["Факт 1", "Факт 2", "Факт 3"]
    fact = random.choice(facts)
    bot.send_message(message.chat.id, fact)

@bot.message_handler(commands=['speak'])
def handle_speak(message):
    text = message.text[7:]  # Убираем '/speak ' из текста команды
    tts = gTTS(text, lang='ru')  # Создаем объект для озвучивания текста на русском языке
    voice_message = BytesIO()
    tts.write_to_fp(voice_message)
    voice_message.seek(0)
    bot.send_voice(message.chat.id, voice_message)

@bot.message_handler(commands=['weather'])
def send_weather(message):
    weather = "Текущая погода: солнечно"
    bot.send_message(message.chat.id, weather)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    # Получаем ID пользователя, которого нужно забанить
    user_id = message.from_user.id

    # Проверяем, забанен ли уже пользователь
    if user_id in banned_users:
        bot.reply_to(message, "Пользователь уже забанен.")
        return

    # Добавляем пользователя в список забаненных
    banned_users.append(user_id)

    # Баним пользователя
    bot.ban_chat_member(message.chat.id, user_id)

    # Отправляем сообщение о том, что пользователь забанен
    bot.reply_to(message, "Пользователь забанен.")

# Обработчик команды /unban
@bot.message_handler(commands=['unban'])
def unban_user(message):
    # Получаем ID пользователя, которого нужно разбанить
    user_id = message.from_user.id

    # Проверяем, забанен ли пользователь
    if user_id not in banned_users:
        bot.reply_to(message, "Пользователь не забанен.")
        return

    # Удаляем пользователя из списка забаненных
    banned_users.remove(user_id)

    # Разбаниваем пользователя
    bot.unban_chat_member(message.chat.id, user_id)

    # Отправляем сообщение о том, что пользователь разбанен
    bot.reply_to(message, "Пользователь разбанен.")





@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Я получил ваше сообщение: " + message.text)
# Запуск бота
bot.polling()