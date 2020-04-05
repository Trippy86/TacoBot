from decouple import config
from pyrogram import MessageHandler, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from dbmodels import Tacos, Chats
from phrases import balance_phrase, balance_comment_medium, balance_comment_high, balance_comment_low,\
    taco_top_phrase, empty_top_phrase
from chattools import get_uid, store_name, get_cid, resolve_name, get_mid, clean_chat, ensure_no_at_sign


default_taco_amount = config('DEFAULT_TACOS', default=25, cast=int)
bot_username = ensure_no_at_sign(config('BOT_USERNAME', default='HeyTacoBot'))    #TODO


def my_tacos_callback(bot, message):
    """ shows users taco-balance """

    cid = get_cid(message)
    chat = Chats.get(Chats.cid == message.chat.id)

    clean_chat(chat.mids, chat.cid, bot, message)

    user_name = store_name(message.from_user)

    uid = str(get_uid(message))
    tacos = Tacos.get(Tacos.chat == cid)

    ok_button = InlineKeyboardButton('OK', callback_data='delete:{}'.format(message.from_user.id))
    ok_keyboard = InlineKeyboardMarkup([[ok_button]])

    balances = tacos.taco_balance

    if uid in balances.keys():
        balance = balances.get(uid)
    else:
        balances.update({uid: default_taco_amount})
        tacos.taco_balance = balances
        tacos.save()
        balance = default_taco_amount

    if chat.less is True:
        comment = ''
    else:
        if balance < 25:
            comment = balance_comment_low
        elif balance > 60:
            comment = balance_comment_high
        else:
            comment = balance_comment_medium

    mid = bot.send_message(chat_id=cid,
                           text=balance_phrase.format(user_name,
                                                      balance,
                                                      comment),
                           reply_to_message_id=get_mid(message),
                           reply_markup=ok_keyboard,
                           parse_mode='html').message_id

    chat.mids = [mid]
    chat.save()


my_tacos_handler = MessageHandler(
                                  callback=my_tacos_callback,
                                  filters=Filters.group & Filters.command(['mytacos', f'mytacos@{bot_username}']))


def taco_top_callback(bot, message):
    """ shows top-5(or less) taco-users in chat """

    cid = get_cid(message)
    mid = get_mid(message)

    store_name(message.from_user)

    chat = Chats.get(Chats.cid == message.chat.id)
    clean_chat(chat.mids, chat.cid, bot, message)

    ok_button = InlineKeyboardButton('OK', callback_data='delete:{}'.format(message.from_user.id))
    ok_keyboard = InlineKeyboardMarkup([[ok_button]])

    tacos = Tacos.get(Tacos.chat == cid)

    balances = tacos.taco_balance

    if len(balances) == 0:                                                                # in case tacos-table is empty
        bot.send_message(text=empty_top_phrase,
                         chat_id=cid,
                         reply_to_message_id=mid,
                         reply_markup=ok_keyboard,
                         parse_mode='html')
        return

    top = list()

    while len(balances) > 0 and len(top) < 5:
        top_uid = max(balances, key=balances.get)
        username = resolve_name(top_uid)
        top.append([username, balances.get(top_uid)])
        del balances[top_uid]

    formatted_top = ''
    for user in top:
        if "@" in user[0]:
            user_link = "https://t.me/{}".format(user[0][1:])
        else:
            user_link = "tg://user?id={}".format(user[0])

        formatted_top += '{}. <a href="{}">{}</a> - <code>{}</code> tacos!\n'.format(top.index(user) + 1,
                                                                                           user_link,
                                                                                           user[0][1:],
                                                                                           user[1])

    mid = bot.send_message(text=taco_top_phrase.format(len(top),
                                                       formatted_top),
                           chat_id=cid,
                           reply_to_message_id=mid,
                           reply_markup=ok_keyboard,
                           parse_mode='html',
                           disable_web_page_preview=True).message_id

    chat.mids = [mid]
    chat.save()


taco_top_handler = MessageHandler(callback=taco_top_callback,
                                  filters=Filters.group & Filters.command(['tacotop', f'tacotop@{bot_username}']))
