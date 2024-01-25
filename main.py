import json
import telebot
from telebot import types

TOKEN = '6922861550:AAG6-PugcPBe68GTOQ3TcvgJtHlI9_rtLc0'  # Замените на токен вашего бота
bot = telebot.TeleBot(TOKEN)


def load_game_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # Замените 'utf-8' на кодировку вашего файла, если она отличается
        return json.load(f)


def play_game(message, game_data, stage):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if "options" in game_data[stage]:
        itemises = [types.KeyboardButton(option) for option in game_data[stage]["options"].keys()]
        markup.add(*itemises)
    else:
        markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, game_data[stage]["message"], reply_markup=markup)
    if "image" in game_data[stage]:
        with open(game_data[stage]["image"], 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    if "options" in game_data[stage]:
        bot.register_next_step_handler(message, process_step, game_data, game_data[stage]["options"])


def process_step(message, game_data, options):
    choice = message.text
    if choice in options:
        play_game(message, game_data, options[choice])
    else:
        bot.send_message(message.chat.id, "Недопустимый ввод. Пожалуйста, выберите одну из предложенных опций.")
        bot.register_next_step_handler(message, process_step, game_data, options)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Добро пожаловать в квест бота,в который вы поможете ЧЕРВЮ в его выборах. Чтобы "
                              "начать игру используйте команду'/game'")


@bot.message_handler(commands=['game'])
def start_game(message):
    game_data = load_game_data("game_data.json")
    play_game(message, game_data, "start")


bot.polling(none_stop=True)
