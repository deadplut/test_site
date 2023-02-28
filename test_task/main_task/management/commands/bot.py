from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from telebot import types
import requests
import json

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


class Command(BaseCommand):

    URL = "https://s1-nova.ru/app/private_test_python/"

    COUNT_START = 0

    def handle(self, *args, **kwargs):
        # Запускаам бота
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков

        @bot.message_handler(commands=['start'])
        def start(message):

            if self.COUNT_START == 0:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
                keyboard.add(button_phone)

                bot.send_message(message.chat.id,
                                 "Привет, а дай номер!",
                                 reply_markup=keyboard)
                self.COUNT_START += 1
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Обнулить старты")
                keyboard.add(button_phone)

                bot.send_message(message.chat.id,
                                 "А это уже не первый /start",
                                 reply_markup=keyboard)

        @bot.message_handler(content_types=['text'])
        def func(message):

            if message.text == "Обнулить старты":
                self.COUNT_START = 0
                bot.send_message(message.chat.id,
                                 "/start обнулены",
                                 )

        @bot.message_handler(content_types=['contact'])
        def confirming(message):

            if message.content_type == "contact":
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, "Мы получили ваш номер.", reply_markup=keyboard)

                data = {"phone": message.contact.phone_number, "login": message.from_user.username, }

                requests.post(self.URL, json=data)

            else:
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, "Номер не был отправлен.", reply_markup=keyboard)

        # Бесконечный цикл
        bot.infinity_polling()
