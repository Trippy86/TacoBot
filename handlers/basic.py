from pyrogram import MessageHandler, Filters
from phrases import start_phrase, help_phrase, delete_message_fail_phrase, admins_only_phrase,\
    silenced_mode_off_phrase, silenced_mode_on_phrase
from dbmodels import Chats
from pyrogram import CallbackQueryHandler
from chattools import get_uid, store_name, clean_chat
import json


def start_callback(bot, message):
    """ callback for /start (private) """
    uid = get_uid(message)

    bot.send_message(uid,
                     start_phrase,
                     parse_mode='html')


start_handler = MessageHandler(callback=start_callback,
                               filters=Filters.command('start') & Filters.private)


def help_callback(bot, message):
    """ callback for /help (private) """
    uid = get_uid(message)

    bot.send_message(uid,
                     help_phrase,
                     parse_mode='html')


help_handler = MessageHandler(callback=help_callback,
                              filters=Filters.private)


def store_names_callback(bot, message):
    """ stores names for each user, if not already present in DB"""
    store_name(message.from_user)


store_names_handler = MessageHandler(callback=store_names_callback)


def less_callback(bot, message):
    chat = Chats.get(Chats.cid == message.chat.id)
    clean_chat(chat.mids, chat.cid, message, bot)

    user = bot.get_chat_member(chat_id=message.chat.id,
                               user_id=message.from_user.id)

    if message.from_user.id == chat.invited_by or\
            user.status == 'administrator' or\
            user.status == 'creator':                   #TODO
        if chat.less is False:
            text = silenced_mode_on_phrase
            chat.less = True
        else:
            chat.less = False
            text = silenced_mode_off_phrase
        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id
        chat.mids = json.dumps([mid])
        chat.save()
    else:
        text = admins_only_phrase
        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id
        chat.mids = json.dumps([mid])
        chat.save()
    pass


less_handler = MessageHandler(callback=less_callback,
                              filters=Filters.command('tacosilence') & Filters.group)


def delete_callback(bot, callbackquery):
    data = callbackquery.data
    user = bot.get_chat_member(chat_id=callbackquery.message.chat.id,
                               user_id=callbackquery.from_user.id)

    if int(data.split(':')[1]) == callbackquery.from_user.id or\
            user.status == 'administrator' or\
            user.status == 'creator':               #TODO
        try:
            bot.delete_messages(chat_id=callbackquery.message.chat.id,
                                message_ids=callbackquery.message.message_id)
        except Exception as e:
            print(e)
            pass
    else:
        bot.answer_callback_query(callback_query_id=callbackquery.id,
                                  text=delete_message_fail_phrase)


delete_handler = CallbackQueryHandler(filters=Filters.callback_data,
                                      callback=delete_callback)
