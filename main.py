from telegram.ext import (
    Updater, CommandHandler, ConversationHandler,
    MessageHandler, Filters, CallbackContext)
from telegram import ReplyKeyboardMarkup, Update
from config import token
import logging
import client

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    reply_keyboard = [[i['name'] for i in client.get_lamps_list()]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте! Из этого бота вы сможете управлять своими лампочками",
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def analyze(update, context):
    text = update.message.text
    command_list = ["Увеличить яркость на 5", "Уменьшить яркость на 5", "Выбрать другую лампу", "Выключить", "Включить"]
    for i in client.get_lamps_list():
        if text == i['name']:
            context.user_data['current_lamp'] = i['name']
            reply_keyboard = [[command_list[0]], [command_list[1]], [command_list[2]]]
            if client.is_power(i['name']):
                reply_keyboard.insert(2, [command_list[3]])
            else:
                reply_keyboard.insert(2, [command_list[4]])
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Что вы хотите сделать с этой лампочкой?",
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if text in command_list:
        if text == command_list[2]:
            reply_keyboard = [[i['name'] for i in client.get_lamps_list()]]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Выберете лампочку",
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        else:
            br = ''
            if text == command_list[0]:
                br = client.brightness_up(context.user_data['current_lamp'], 5)
            elif text == command_list[1]:
                br = client.brightness_down(context.user_data['current_lamp'], 5)
            elif text == command_list[3] or text == command_list[4]:
                client.turn(context.user_data['current_lamp'])
            reply_keyboard = [[command_list[0]], [command_list[1]], [command_list[2]]]

            if client.is_power(context.user_data['current_lamp']):
                reply_keyboard.insert(2, [command_list[3]])
            else:
                reply_keyboard.insert(2, [command_list[4]])

            if br:
                res = "Сделано. {name}, {br}%. Что дальше?".format(name=context.user_data['current_lamp'], br=br)
            else:
                turn = client.is_power(context.user_data['current_lamp'])
                if turn:
                    res = "Сделано. {name} включена. Что дальше?".format(name=context.user_data['current_lamp'])
                else:
                    res = "Сделано. {name} выключена. Что дальше?".format(name=context.user_data['current_lamp'])
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=res,
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def main():
    start_handler = CommandHandler('start', start)
    main_conv = MessageHandler(Filters.text & (~Filters.command), analyze)

    dispatcher.add_handler(main_conv)
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
