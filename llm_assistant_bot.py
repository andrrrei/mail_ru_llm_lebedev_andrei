import telebot
from telebot import types
import logging
from logging.handlers import RotatingFileHandler

from model_wrapper import ModelWrapper

"""
get_text_messages - обработка любого текстового сообщения, в том числе того, что отправился при нажатии кнопки.

Методы, реализующие одноименные команды телеграм-боту:
start
help
generate
checkmodel
model
"""

bot = telebot.TeleBot('7176555672:AAFRT8nbLrCsoXcsBA-R50sWuE7KGSgbKig')
logger = logging.getLogger('bot_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('bot.log', maxBytes=1e6, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_telegram_notification(message):
    bot.send_message('@llm_bot_notifier', message)

model_wrapper = ModelWrapper() # внутри класса описание

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} запустил бота с командой /help")

    help_message = """Доступны следующие команды:
/start старт бота
/model выбор модели
/checkmodel посмотреть, как модель сейчас загружена
/generate сгенерировать текст по контексту (можно использовать без введения команды)
"""
    bot.send_message(message.from_user.id, help_message)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} запустил бота с командой /start")
    send_telegram_notification("Кто-то запустил бота")

    bot.send_message(message.from_user.id, "Привет! Для знакомства с доступными командами введите /help")


@bot.message_handler(commands=['model'])
def model(message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} запустил бота с командой /model")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("StatLM")
    btn2 = types.KeyboardButton("GPT")
    btn3 = types.KeyboardButton("Llama")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "Выберите модель для генерации", reply_markup=markup)


@bot.message_handler(commands=['checkmodel'])
def checkmodel(message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} запустил бота с командой /checkmodel")
    
    bot.send_message(message.from_user.id, f"Текущая модель: {str(model_wrapper.current_model_name)}")


@bot.message_handler(commands=['generate'])
def generate(message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} запустил бота с командой /generate")

    bot.send_message(message.from_user.id,
                     "Введите вопрос, на который нужно ответить, либо текст, который нужно продолжить")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_message = message.text
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} отправил сообщение: {user_message}")
    
    print(f'<{message.text}>')
    if message.text in ['StatLM', 'GPT', 'Llama']:
        print(f'@{message.text}@')
        status, result = model_wrapper.load(message.text, test_inference=True)
        if status:
            bot.send_message(message.from_user.id, f"Модель {message.text} загружена")
        else:
            bot.send_message(message.from_user.id, f"Проблемы с загрузкой модели, ошибки описаны ниже.\n{result}")
    else:
        status, result = model_wrapper.generate(message.text)
        if status:
            bot.send_message(message.from_user.id, result)
        else:
            bot.send_message(message.from_user.id, f"Проблемы с генерацией, ошибки описаны ниже.\n{result}")


bot.polling(none_stop=True, interval=0)
