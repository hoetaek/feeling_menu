from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot_helper import build_menu
from classify import classify_feeling
from service import recommend_menu, get_bot_token
from train import store_training
from data import feeling_data


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def classify_message(update, context):
    message = update.message.text
    context.chat_data['train_data'] = message

    feeling = classify_feeling(message)
    recommended_message = recommend_menu(feeling)
    context.bot.send_message(chat_id=update.effective_chat.id, text=recommended_message)

    show_list = [InlineKeyboardButton('네', callback_data='네'), InlineKeyboardButton('아니요', callback_data='아니요')]
    show_markup = InlineKeyboardMarkup(build_menu(show_list, 2))  # make markup
    context.bot.send_message(chat_id=update.effective_chat.id, text="답이 마음에 드나요?", reply_markup=show_markup)


def train_handler(update, context):
    train_data = ' '.join(context.args)
    print(train_data)
    context.chat_data['train_data'] = train_data
    select_feeling(train_data, update, context)


def callback_train_again(update, context):
    context.bot.edit_message_text("어느 감정을 느꼈나요?",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)
    train_data = context.chat_data
    select_feeling(train_data, update, context)


def select_feeling(train_data, update, context):
    show_list = [InlineKeyboardButton(i, callback_data=f"감정, {i}") for i in feeling_data.keys()]
    show_markup = InlineKeyboardMarkup(build_menu(show_list, 2))  # make markup

    if train_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text='어느 감정을 느꼈나요?', reply_markup=show_markup
                                 )


def callback_train(update, context):
    train_data = context.chat_data['train_data']
    feeling = ''.join(update.callback_query.data.split(', ')[1:])

    store_training(train_data, feeling)
    context.bot.edit_message_text(f"{feeling}을/를 선택하였습니다.",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)


def callback_exit_conversation(update, context):
    context.bot.edit_message_text("감사합니다.",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)


if __name__ == "__main__":
    token = get_bot_token()

    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    classify_message_handler = MessageHandler(Filters.text & (~Filters.command), classify_message)
    dispatcher.add_handler(classify_message_handler)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('train', train_handler))
    dispatcher.add_handler(CallbackQueryHandler(callback_train, pattern='^감정'))
    dispatcher.add_handler(CallbackQueryHandler(callback_exit_conversation, pattern='^네'))
    dispatcher.add_handler(CallbackQueryHandler(callback_train_again, pattern='^아니요'))

    updater.start_polling()
